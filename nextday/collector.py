"""Durable, bounded one-off batch execution with idempotent resume."""
import fcntl
import json
import time
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from jsonschema.validators import validator_for

from .client import APIError, Glasser, save_json

TERMINAL = {"COMPLETED", "FAILED", "STOPPED"}


def validate_input(value, schema):
    error = next(validator_for(schema)(schema).iter_errors(value), None)
    if error:
        # Never dump a provider cursor, payload or credential into an exception.
        raise ValueError(f"Endpoint input schema failed at {list(error.path)} ({error.validator}).")


def utcnow():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def contract_path(root, provider, endpoint):
    return Path(root) / "contracts" / (provider + "__" + endpoint.strip("/").replace("/", "__") + ".json")


def maximum_charge(contract):
    price = contract["price"]
    rule = price["rule"]
    if rule["type"] == "flat":
        normal = Decimal(rule["amount_usd"])
    elif "cap_usd" in rule:
        normal = Decimal(rule["cap_usd"])
    else:
        raise ValueError("Unsupported uncapped price rule; refusing a paid Run.")
    return max([normal] + [Decimal(x) for x in price["charges"].values()])


def check_total_approval(root, manifest, own_path):
    approval_path = Path(root) / "approval.json"
    if not approval_path.exists():
        return
    limit = Decimal(json.loads(approval_path.read_text())["total_max_usd"])
    if not limit.is_finite() or limit < 0:
        raise ValueError("Invalid total spending approval.")
    total = Decimal(manifest["reserved_usd"])
    for path in (Path(root) / "batches").glob("*/manifest.json"):
        if path != own_path:
            total += Decimal(json.loads(path.read_text())["reserved_usd"])
    if total > limit:
        raise ValueError(f"Combined batch reservations ${total} exceed total approval ${limit}.")


def prepare(client, plan, root, batch, budget):
    path = Path(root) / "batches" / batch / "manifest.json"
    if path.exists():
        manifest = json.loads(path.read_text())
        if manifest["plan"] != plan or Decimal(manifest["budget_usd"]) != Decimal(budget):
            raise ValueError("Existing batch has different input/budget; use its original plan or a new batch name.")
        check_total_approval(root, manifest, path)
        return manifest, path
    cache = {}
    jobs = []
    for spec in plan["jobs"]:
        pair = spec["provider"], spec["endpoint"]
        if pair not in cache:
            contract = client.inspect(*pair)
            cache[pair] = contract
            save_json(contract_path(root, *pair), contract)
        contract = cache[pair]
        validate_input(spec["input"], contract["input_schema"])
        jobs.append({"spec": spec, "idempotency_key": str(uuid.uuid4()),
                     "endpoint_version": contract["endpoint_version"],
                     "reserved_usd": str(maximum_charge(contract)), "status": "PLANNED"})
    reserved = sum((Decimal(j["reserved_usd"]) for j in jobs), Decimal(0))
    if reserved > Decimal(budget):
        raise ValueError(f"Maximum reservation ${reserved} exceeds approved batch cap ${budget}.")
    manifest = {"schema_version": 1, "batch": batch, "created_at": utcnow(), "plan": plan,
                "budget_usd": str(budget), "reserved_usd": str(reserved), "jobs": jobs}
    check_total_approval(root, manifest, path)
    save_json(path, manifest)
    return manifest, path


def run_batch(plan_file, batch, budget="1.00", execute=False, root="data", client=None):
    if not batch or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in batch):
        raise ValueError("Batch names may contain only letters, digits, hyphens and underscores.")
    amount = Decimal(budget)
    if not amount.is_finite() or amount < 0:
        raise ValueError("Budget must be a finite nonnegative decimal.")
    Path(root).mkdir(parents=True, exist_ok=True)
    client = client or Glasser()
    plan = json.loads(Path(plan_file).read_text())
    # Serialize collectors sharing a data directory, including concurrent resumes.
    with (Path(root) / ".collector.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        manifest, path = prepare(client, plan, root, batch, budget)
        print(f"{batch}: {len(manifest['jobs'])} calls; maximum inspected reservation ${manifest['reserved_usd']}; cap ${budget}")
        if not execute:
            return manifest
        for index, job in enumerate(manifest["jobs"]):
            if job["status"] in TERMINAL:
                continue
            spec = job["spec"]
            if "run_id" not in job:
                current = client.inspect(spec["provider"], spec["endpoint"])
                validate_input(spec["input"], current["input_schema"])
                if maximum_charge(current) > Decimal(job["reserved_usd"]):
                    raise ValueError("Endpoint price increased beyond its approved reservation; stopping.")
                if current["endpoint_version"] != job["endpoint_version"]:
                    raise ValueError("Endpoint contract version changed; prepare a new batch.")
                job["status"] = "SUBMITTING"
                save_json(path, manifest)  # Persist BEFORE any paid network call.
                payload = {"provider": spec["provider"], "endpoint": spec["endpoint"],
                           "input": spec["input"], "endpoint_version": job["endpoint_version"],
                           "task_id": "nextday-ingestion", "metadata": {"batch": batch, "source": spec["source"]}}
                run = client.request("POST", "/v1/runs", payload, job["idempotency_key"],
                                     timeout=max(180, (current.get("timeout_ms") or 0) / 1000 + 30))
            else:
                run = client.request("GET", "/v1/runs/" + job["run_id"])
            deadline = time.monotonic() + 300
            while True:
                captured = utcnow()
                # Preserve every received response, including intermediate async states.
                raw_path = path.parent / "raw" / f"{index:04d}_{run['id']}_{time.time_ns()}.json"
                save_json(raw_path, {"captured_at": captured, "spec": spec, "run": run})
                job.update(status=run["status"], run_id=run["id"], run_url=run.get("run_url"),
                           charge_usd=run.get("charge_usd"), raw_file=str(raw_path), captured_at=captured)
                save_json(path, manifest)
                if run["status"] in TERMINAL:
                    break
                if time.monotonic() > deadline:
                    raise APIError("Run still pending; resume this batch later without a new charge.")
                time.sleep(2)
                run = client.request("GET", "/v1/runs/" + job["run_id"])
            provider_status = (run.get("provider_response") or {}).get("http_status")
            print(f"[{index + 1}/{len(manifest['jobs'])}] {spec['source']}: {run['status']}, provider HTTP {provider_status}, charge ${run.get('charge_usd')}")
            charged = sum((Decimal(j.get("charge_usd") or "0") for j in manifest["jobs"]), Decimal(0))
            if charged > amount:
                raise ValueError("Actual charges exceeded inspected budget (possible price race); no further calls.")
        manifest["finished_at"] = utcnow()
        manifest["charge_usd"] = str(sum((Decimal(j.get("charge_usd") or "0") for j in manifest["jobs"]), Decimal(0)))
        save_json(path, manifest)
        print(f"Batch charge: ${manifest['charge_usd']}")
        return manifest
