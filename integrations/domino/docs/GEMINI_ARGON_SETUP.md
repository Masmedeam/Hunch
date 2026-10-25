# Using a Google AI Studio API key with Gemini 4 Argon

Checked against Google's docs on 2026-10-25: `ai.google.dev/gemini-api/docs/api-key`, `/models/gemini-4-argon` (updated 2026-10-14), `/quickstart`, `/thinking`, `/function-calling`, `/image-understanding`, `/agents`, `/pricing`.

**Tags:**
- **[docs]** = taken from those pages today.
- **[reported]** = found by our research agent, not re-checked line by line.
- **[legacy]** = from SDK knowledge, not re-checked today.

## 1. Get a key that works

1. Open Google AI Studio and go to **API Keys**. Click **Create API key**. [docs]
   - Since 2026-05-28, new keys are **auth keys**: bound to a service account and restricted to the Gemini API by default. [docs]
2. **Restrict older keys or the request fails.** The Gemini API rejects requests from *unrestricted standard keys* with HTTP 403. [docs]
   - Fix: on the API Keys page, hover the **Unrestricted** label, click **Add restrictions**, choose **Restrict to Gemini API only**, then **Restrict key**.
   - This needs the `apikeys.keys.update` permission, for example the API Keys Admin or Editor role.
   - A key restricted to *other* Google APIs without the Generative Language API also fails.
3. **Credits.** Our key in `.env` is **hackathon-provided with free Argon credits**, so no billing setup is needed. Outside the event, Argon has no free tier: you would link billing to the key's project, and Tier 1 activates as soon as billing is linked. [reported]
   - Team rule: develop on Argon too. Short calls cost $0.0001–0.004 at list price.

| Model | Price per 1M tokens (input / output) | Notes |
|---|---|---|
| `gemini-4-argon` | $2 / $10 until 2026-11-30, then $4 / $20 | Thinking tokens bill as output tokens. [docs] |

## 2. Store the key safely on this Mac

Do not paste the key into chat or terminal transcripts, into code, or into a file that might be committed.

**Option A (recommended): macOS Keychain.** Run this in your own terminal. It prompts for the key without echoing it:

```bash
security add-generic-password -a "$USER" -s GEMINI_API_KEY -w
```

Load the key per shell, or add this line to `~/.zshrc`:

```bash
export GEMINI_API_KEY="$(security find-generic-password -a "$USER" -s GEMINI_API_KEY -w)"
```

`tools/gemini_smoke.py` also reads the Keychain directly if the variable is not set.

**Option B: a git-ignored `.env` file.**

```bash
cd ~/ArgonHackathon
printf 'GEMINI_API_KEY=%s\n' "PASTE_KEY_HERE" > .env   # edit in your editor instead if you prefer
chmod 600 .env
grep -qx '.env' .gitignore 2>/dev/null || echo '.env' >> .gitignore
```

**Variable precedence.** The SDK reads `GEMINI_API_KEY` or `GOOGLE_API_KEY`. If both are set, `GOOGLE_API_KEY` wins. [docs] So `unset GOOGLE_API_KEY` if it holds an unrelated key.

**Sharing with teammates.** Each teammate should create their own key in the shared billing project, rather than passing one key around.

## 3. Install the SDK

Python 3.14 is this Mac's default, and some libraries we may need (MuJoCo, JAX) ship wheels for 3.12 first. Use a 3.12 virtual environment:

```bash
cd ~/ArgonHackathon
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install -U google-genai pydantic numpy
python tools/gemini_smoke.py            # checks the key, lists models, makes one tiny Flash call
python tools/gemini_smoke.py --argon    # adds one tiny paid Argon call (well under $0.01)
```

## 4. Code you will need (Interactions API, the SDK default)

### Basic call [docs]

```python
from google import genai

client = genai.Client()  # reads GEMINI_API_KEY
interaction = client.interactions.create(
    model="gemini-4-argon",
    input="In one sentence: what is expected free energy?",
)
print(interaction.output_text)
```

### Thinking level [docs]

Argon and 3.8 Flash both default to medium. Allowed values are low, medium, and high.

```python
interaction = client.interactions.create(
    model="gemini-4-argon",
    input="Plan the next sub-goal.",
    generation_config={"thinking_level": "low", "thinking_summaries": "auto"},
)
for step in interaction.steps:
    if step.type == "thought" and getattr(step, "summary", None):
        print("thought:", step.summary)
print(interaction.output_text)
```

### Structured output [docs]

This is how RPWM gets explicit probability distributions, since logprobs are not available.

```python
from pydantic import BaseModel

class OutcomeDist(BaseModel):
    outcomes: list[str]
    probs: list[float]

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Predict the outcome distribution of pushing the red block east.",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": OutcomeDist.model_json_schema(),
    },
)
dist = OutcomeDist.model_validate_json(interaction.output_text)
```

### Image input [docs]

Inline bytes count toward the 20 MB request limit. Images of 384 px or less cost 258 tokens.

```python
import base64

with open("frame.png", "rb") as f:
    img = base64.b64encode(f.read()).decode("utf-8")

interaction = client.interactions.create(
    model="gemini-robotics-er-2-preview",
    input=[
        {"type": "text", "text": "Point to every block. Return JSON [{point:[y,x], label}] with coordinates on a 0-1000 grid."},
        {"type": "image", "data": img, "mime_type": "image/png"},
    ],
)
```

### Function calling and multi-turn state [docs]

```python
import json

tool = {
    "type": "function",
    "name": "recurse",
    "description": "Solve a sub-goal with a child RPWM call.",
    "parameters": {"type": "object", "properties": {"subgoal": {"type": "string"}}, "required": ["subgoal"]},
}

first = client.interactions.create(model="gemini-4-argon", input="Stack red on blue.", tools=[tool])
for step in first.steps:
    if step.type == "function_call":
        result = {"outcome": "done", "free_energy": 1.7}   # run the child call here
        follow = client.interactions.create(
            model="gemini-4-argon",
            input=[{"type": "function_result", "name": step.name, "call_id": step.id,
                    "result": [{"type": "text", "text": json.dumps(result)}]}],
            tools=[tool],
            previous_interaction_id=first.id,   # server-side conversation state
        )
```

### Legacy `generate_content` fallback [legacy]

Use only if the Interactions API misbehaves.

```python
from google.genai import types

resp = client.models.generate_content(
    model="gemini-4-argon",
    contents="...",
    config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level="low")),
)
print(resp.text)
```

## 5. Managed Agents with Argon (for the $5K "Best use of Managed Agents" prize) [reported]

```python
agent = client.agents.create(
    id="rpwm",
    base_agent="antigravity-preview-09-2026",
    agent_config={"type": "antigravity", "model": "gemini-4-argon", "max_total_tokens": "500000"},
    system_instruction="You are the slow (Level 2) planner of an RPWM agent ...",
    tools=[{"type": "code_execution"}],
)
run = client.interactions.create(agent="rpwm", environment="remote", input="...", background=True)
run = client.interactions.get(id=run.id)   # poll until status == "completed"; or stream=True for step events
```

**Recursion.** Managed agents cannot spawn sub-agents yet.
- Give the agent a `function` tool, such as `recurse` above.
- Your client runs the child interaction and returns a `function_result`.
- Alternatively, code inside the sandbox can call the Gemini REST API itself, which gives an RLM-style REPL.

**MCP tools (treg / Glasser).** Register the token once, so it never appears in payloads or in the sandbox:

```python
client.credentials.create(id="treg", type="bearer_token", token=TREG_TOKEN, header_name="X-Treg-Token", prefix="")
tools = [{"type": "mcp_server", "name": "treg", "url": "https://treg.to/mcp/", "credential": "treg"}]
```

MCP over Streamable HTTP only, lowercase names, and no `-` in names. Docs do not confirm Argon support for `mcp_server`, so test it.

**Limits.**
- One run can use 100k to 3M tokens and take minutes. Cap it with `max_total_tokens`.
- Sandbox compute is free during the preview.
- Setting temperature, top_p, top_k, or max_output_tokens on agents returns HTTP 400.

## 6. Best way to use our key: Argon only, measured 2026-10-25

**Team rule: every model call uses `gemini-4-argon`.**

### Status

| Check | Result |
|---|---|
| Key | `GOOGLE_API_KEY` in `.env`, permissions set to 600 |
| Restriction and billing | OK: Argon answers. 10 probes cost about $0.014 in total. |
| Logs | `runs/argon_probe_*.json`, `runs/managed_agent_probe_*.json` |

### Measured performance

| Capability | Result | How RPWM uses it |
|---|---|---|
| Text, thinking low / medium / high | 3.0 / 4.5 / 6.2 s; 0 / 60 / 376 thought tokens; $0.0001 / $0.0009 / $0.004 | The **compute dial** for free-energy-gated recursion |
| Structured output (JSON schema) | OK, 3.5 s; returned a calibrated 0.6 / 0.3 / 0.1 outcome distribution | Explicit P(o\|s,a) and Q(s), so F and G are exact (no logprobs needed) |
| Function calling round trip | OK, 6.5 s | The `recurse(subgoal)` tool: RLM-style recursion |
| Vision on a 320 px rendered frame | Typically 3–5 s; spikes of 15 s and 67 s; about 1.2k input tokens | Perception checks at sub-goal boundaries; 10 s timeout with simulator ground truth as fallback. State "0-indexed" in prompts. |
| Managed Agent (`antigravity-preview-09-2026` on Argon) | OK: sandbox code ran, the custom tool round-tripped, completed; about 5.8k tokens (about $0.01); about 40 s | The slow Level-2 planner, and the $5K Managed Agents prize |
| `mcp_server` to treg / Glasser | Not tested (no vendor tokens yet) | Tool-world actions (D3 / D9 / D10) |

### Usage pattern

1. **Spend nothing when nothing is surprising.** Routine steps follow numpy rules with no model call. This is the adaptive-computation baseline.
2. **Escalate as surprise persists.** Use the thinking-level ladder `low` → `medium` → `high` → `recurse()` (a child call), keyed on relative ΔF. Log level, seconds, and thought tokens for every call; that log is the demo's evidence for the paper's claim (i).
3. **Make every prediction a distribution.** Outcome predictions, hypothesis sets, and sub-goal success probabilities come back as JSON-schema distributions, and numpy computes F, G, and surprise exactly.
4. **Long-context memory instead of embeddings.** Argon has 1M tokens of context. On escalation, pass the whole compact episode log, RLM-style, rather than building a vector index.
5. **The slowest level runs as a Managed Agent.** Recursion uses the custom-tool round trip; MCP tools go through the Credentials API. Pre-warm the agent before the demo and stream its steps on screen.
6. **Show the thinking.** Set `thinking_summaries: "auto"` on escalations and display the summaries as the "why it recursed" narrative.
7. **Evaluations are cheap.** About 20 calls per episode × $0.001–0.004 gives roughly $0.02–0.08 per episode. 20 episodes × 4 arms ≈ $2–6. Use the Batch / Flex options Argon supports for offline sweeps.
8. **Guards.** Credits are hackathon-provided, so cost is not the constraint. These guards catch bugs and protect the stage demo:
   - a loose runaway-loop cap, for example 500 calls per episode;
   - 20 s timeout per call, with retry and backoff on 429, since rate limits are unpublished;
   - a record/replay cache keyed by prompt hash for the stage demo.
9. **Spend the credits where they buy quality.** Run `thinking_level: high` for planning and judging, more ablation seeds (50+ instead of 20), and an Argon judge panel (`tools/argon_judges.py`).

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| HTTP 403 | Unrestricted standard key, or a key restricted to the wrong API | Restrict it to the Gemini API (§1) |
| Argon call fails while Flash works | No billing on the project (Argon has no free tier) | Link billing / Tier 1 |
| HTTP 429 | Rate limit; RPM and RPD are not published, only shown in the AI Studio console | Back off and retry; send the bulk of calls to Flash |
| Status "incomplete" | Thinking tokens consumed `max_output_tokens` | Raise the limit or lower `thinking_level` |
| HTTP 400 on a managed agent | Sampling parameters set | Remove temperature, top_p, top_k, max_output_tokens |
| Wrong key used | `GOOGLE_API_KEY` overrides `GEMINI_API_KEY` | `unset GOOGLE_API_KEY` |
| Wheels fail to install | Python 3.14 | Use the 3.12 virtual environment (§3) |
