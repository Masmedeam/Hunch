"""Exact discrete active-inference math for RPWM-Lite.

Each block has a joint hidden state s = (z, h):
  z in Z   = (kept, moved)        is the block still where the agent believes it is?
  h in HYP = (LN, LS, HN, HS)     weight Light/Heavy x surface Normal/Slippery
Beliefs are categorical arrays q[z, h] (shape 2x4). Observations are discrete action outcomes.
Every quantity shown in the UI (surprise, F, complexity, accuracy, information gain, G) is computed
exactly here; Gemini 4 Argon supplies the likelihood tables P(o | a, h), never the numbers below.
"""
import numpy as np

HYP = ("LN", "LS", "HN", "HS")
Z = ("kept", "moved")
OUTCOMES = {
    "pick": ("success", "fail"),
    "place": ("success", "fail"),
    "push": ("moved_1", "slid", "no_move"),
    "probe": ("rocks", "solid", "nothing"),
}
# If the block is not where the agent believes (z = moved), acting on the believed cell mostly finds nothing.
MOVED_LIKELIHOOD = {
    "pick": (0.05, 0.95),
    "place": (0.5, 0.5),
    "push": (0.05, 0.05, 0.90),
    "probe": (0.03, 0.02, 0.95),
}
EPS = 1e-9


def prior_h(p_heavy, p_slippery):
    ph, ps = float(p_heavy), float(p_slippery)
    return np.array([(1 - ph) * (1 - ps), (1 - ph) * ps, ph * (1 - ps), ph * ps])


def joint_prior(p_heavy, p_slippery, p_moved=0.0):
    h = prior_h(p_heavy, p_slippery)
    return np.vstack([(1 - p_moved) * h, p_moved * h])


def marginals(q):
    qh = q.sum(axis=0)
    return {"p_heavy": float(qh[2] + qh[3]), "p_slippery": float(qh[1] + qh[3]), "p_moved": float(q[1].sum())}


def hazard(q, rho):
    """Per-step chance that the world moved the block without the agent acting (perturbations)."""
    out = q.copy()
    out[1] = q[1] + rho * q[0]
    out[0] = (1 - rho) * q[0]
    return out


def likelihood_tensor(action_type, L_kept):
    """L_kept: (n_outcomes, 4) rows=outcomes, cols=HYP. Returns Lj[o, z, h]."""
    L_kept = np.asarray(L_kept, dtype=float)
    n_o = L_kept.shape[0]
    moved = np.asarray(MOVED_LIKELIHOOD[action_type], dtype=float)[:n_o]
    Lj = np.zeros((n_o, 2, 4))
    Lj[:, 0, :] = L_kept
    Lj[:, 1, :] = moved[:, None]
    Lj = np.clip(Lj, EPS, None)
    return Lj / Lj.sum(axis=0, keepdims=True)


def predictive(q, Lj):
    return np.einsum("ozh,zh->o", Lj, q)


def entropy(p, axis=None):
    p = np.clip(p, EPS, 1.0)
    return -(p * np.log(p)).sum(axis=axis)


def update(q, Lj, o_idx):
    """Exact Bayesian update. Returns posterior, surprise, and F split into complexity - accuracy."""
    lik = Lj[o_idx]
    evidence = float((q * lik).sum())
    post = q * lik / max(evidence, EPS)
    surprise = -np.log(max(evidence, EPS))
    complexity = float((post * (np.log(np.clip(post, EPS, 1)) - np.log(np.clip(q, EPS, 1)))).sum())
    accuracy = float((post * np.log(np.clip(lik, EPS, 1))).sum())
    F = complexity - accuracy  # equals surprise for the exact posterior (Decomposition 1 of the paper)
    return post, {"surprise": float(surprise), "F": float(F), "complexity": complexity, "accuracy": accuracy,
                  "evidence": evidence}


def info_gain(q, Lj):
    """Mutual information I(S; O) under the current belief: H[p(o)] - E_q H[P(o|s)]."""
    p_o = predictive(q, Lj)
    cond = entropy(Lj, axis=0)  # (z, h)
    return float(entropy(p_o) - (q * cond).sum())


def expected_free_energy(q, Lj, utility, cost, beta=1.0, lam=1.0):
    """G = -(information gain) - beta * E[utility] + lam * cost.

    utility[o, z, h] is the log-preference ln P~(o | C) up to a constant, here minus the cost-to-go of the
    sub-goal after outcome o in state (z, h): an explicit preference prior C, which the draft omits.
    """
    ig = info_gain(q, Lj)
    p_joint = Lj * q[None, :, :]
    pv = float(beta * (p_joint * utility).sum())
    G = -ig - pv + lam * cost
    return {"ig": ig, "pv": pv, "cost": float(lam * cost), "G": float(G), "p_outcomes": predictive(q, Lj)}


def relative_drop(F_prev, F_new):
    return (F_prev - F_new) / max(1.0, abs(F_prev))


class StopRule:
    """Scale-invariant stopping: stop when the relative free-energy drop falls below delta for `patience`
    consecutive steps, when F rises (divergence, reported as such, best iterate kept), or at r_max."""

    def __init__(self, delta=0.05, patience=1, r_max=3):
        self.delta, self.patience, self.r_max = delta, patience, r_max
        self.reset()

    def reset(self):
        self.r, self.small, self.best, self.history = 0, 0, None, []

    def step(self, F_prev, F_new):
        self.r += 1
        d = relative_drop(F_prev, F_new)
        self.history.append({"r": self.r, "F_prev": F_prev, "F_new": F_new, "dF_rel": d})
        if self.best is None or F_new < self.best[1]:
            self.best = (self.r, F_new)
        if d < -self.delta:
            return True, "diverged", d
        self.small = self.small + 1 if d < self.delta else 0
        if self.small >= self.patience:
            return True, "converged", d
        if self.r >= self.r_max:
            return True, "r_max", d
        return False, "continue", d


def bootstrap_ci(values, n_boot=4000, alpha=0.05, seed=0):
    v = np.asarray(values, dtype=float)
    if v.size == 0:
        return {"mean": None, "lo": None, "hi": None, "n": 0}
    rng = np.random.default_rng(seed)
    means = rng.choice(v, size=(n_boot, v.size), replace=True).mean(axis=1)
    return {"mean": float(v.mean()), "lo": float(np.quantile(means, alpha / 2)),
            "hi": float(np.quantile(means, 1 - alpha / 2)), "n": int(v.size)}


def brier(p_vec, o_idx):
    y = np.zeros(len(p_vec))
    y[o_idx] = 1.0
    return float(((np.asarray(p_vec) - y) ** 2).sum())
