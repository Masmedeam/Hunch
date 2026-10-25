"""Domino statistical core: latent 'tension' world state + regime-mixture next-day forecasts, with honest backtests.

World model (RPWM, applied to real data)
  L0  observations: attention index A_t (Wikipedia crisis pageviews, z-scored on trailing windows), returns r_t
  L1  latent state: s_t in {calm, tense}, a 2-state Gaussian HMM on A_t, filtered forward only (no look-ahead)
  L2  next-day market law: r_{t+1} ~ (1-w) t5(0, c0*sigma) + w t5(mu1, k*sigma), w = P(s_{t+1} = tense | A_1..t),
      sigma = EWMA volatility (RiskMetrics, lambda 0.94). Baseline = same t5 with w = 0 and c0 = 1.
Surprise (free energy of the day) = -log p(r_actual | model). Every number here is computed, not asserted.
"""
import math

import numpy as np
import pandas as pd
from scipy import optimize, stats

NU = 5.0
T_SCALE = math.sqrt((NU - 2) / NU)  # unit-variance Student-t
BIG = 2.5  # "big move": |next-day log return| > 2.5 %


# ---------------------------------------------------------------------------------------------- HMM
def hmm_fit(x, iters=60, seed=0):
    x = np.asarray(x, float)
    mu = np.array([np.quantile(x, 0.3), np.quantile(x, 0.92)])
    var = np.array([np.var(x) * 0.5, np.var(x) * 2.0]) + 1e-3
    A = np.array([[0.95, 0.05], [0.15, 0.85]])
    pi = np.array([0.9, 0.1])
    for _ in range(iters):
        B = np.stack([stats.norm.pdf(x, mu[k], math.sqrt(var[k])) for k in range(2)], axis=1) + 1e-300
        n = len(x)
        alpha, c = np.zeros((n, 2)), np.zeros(n)
        alpha[0] = pi * B[0]
        c[0] = alpha[0].sum()
        alpha[0] /= c[0]
        for t in range(1, n):
            alpha[t] = (alpha[t - 1] @ A) * B[t]
            c[t] = alpha[t].sum()
            alpha[t] /= c[t]
        beta = np.ones((n, 2))
        for t in range(n - 2, -1, -1):
            beta[t] = (A @ (B[t + 1] * beta[t + 1])) / c[t + 1]
        gamma = alpha * beta
        gamma /= gamma.sum(axis=1, keepdims=True)
        xi = np.zeros((2, 2))
        for t in range(n - 1):
            m = np.outer(alpha[t], B[t + 1] * beta[t + 1]) * A / c[t + 1]
            xi += m / m.sum()
        pi = gamma[0]
        A = xi / xi.sum(axis=1, keepdims=True)
        mu = (gamma * x[:, None]).sum(0) / gamma.sum(0)
        var = (gamma * (x[:, None] - mu) ** 2).sum(0) / gamma.sum(0) + 1e-3
    if mu[0] > mu[1]:  # state 1 = tense (higher attention)
        mu, var, pi, A = mu[::-1], var[::-1], pi[::-1], A[::-1, ::-1]
    return {"mu": mu, "var": var, "A": A, "pi": pi}


def hmm_filter(x, p):
    """Forward filtering only: P(s_t | x_1..t) for every t, plus one-step-ahead P(s_{t+1} | x_1..t)."""
    x = np.asarray(x, float)
    B = np.stack([stats.norm.pdf(x, p["mu"][k], math.sqrt(p["var"][k])) for k in range(2)], axis=1) + 1e-300
    a = np.zeros((len(x), 2))
    prev = p["pi"]
    for t in range(len(x)):
        a[t] = (prev @ p["A"] if t else prev) * B[t]
        a[t] /= a[t].sum()
        prev = a[t]
    ahead = a @ p["A"]
    return a[:, 1], ahead[:, 1]


# ---------------------------------------------------------------------------------------------- forecast law
def ewma_sigma(r, lam=0.94, warm=20):
    r = np.asarray(r, float)
    s2 = np.empty(len(r) + 1)
    s2[0] = np.nanvar(r[:warm]) if len(r) >= warm else np.nanvar(r) or 1.0
    for t in range(len(r)):
        s2[t + 1] = lam * s2[t] + (1 - lam) * (r[t] if np.isfinite(r[t]) else 0.0) ** 2
    return np.sqrt(s2)  # s[t] = sigma forecast for r[t] made after observing r[:t]


def mix_pdf(y, w, sigma, prm):
    c0, k, mu1 = prm
    p0 = stats.t.pdf(y, NU, loc=0.0, scale=c0 * sigma * T_SCALE)
    p1 = stats.t.pdf(y, NU, loc=mu1, scale=k * sigma * T_SCALE)
    return (1 - w) * p0 + w * p1


def mix_cdf(y, w, sigma, prm):
    c0, k, mu1 = prm
    return (1 - w) * stats.t.cdf(y, NU, 0.0, c0 * sigma * T_SCALE) + w * stats.t.cdf(y, NU, mu1, k * sigma * T_SCALE)


def mix_quantile(q, w, sigma, prm):
    lo, hi = -50 * sigma - 50, 50 * sigma + 50
    return optimize.brentq(lambda y: mix_cdf(y, w, sigma, prm) - q, lo, hi)


def fit_mixture(y, w, sigma):
    def nll(th):
        prm = (math.exp(th[0]), math.exp(th[1]), th[2])
        return -np.sum(np.log(mix_pdf(y, w, sigma, prm) + 1e-300))
    res = optimize.minimize(nll, x0=[0.0, math.log(1.6), 0.3], method="Nelder-Mead", options={"maxiter": 600})
    th = res.x
    return (float(math.exp(th[0])), float(math.exp(th[1])), float(th[2]))


def crps_samples(samples, y):
    s = np.sort(samples)
    n = len(s)
    term1 = np.mean(np.abs(s - y))
    term2 = np.sum((2 * np.arange(1, n + 1) - n - 1) * s) / (n * n)  # = 0.5 E|X - X'|
    return float(term1 - term2)


def sample_mix(w, sigma, prm, n, rng):
    c0, k, mu1 = prm
    z = rng.standard_t(NU, size=n) * T_SCALE
    tense = rng.random(n) < w
    return np.where(tense, mu1 + k * sigma * z, c0 * sigma * z)


# ---------------------------------------------------------------------------------------------- data assembly
def assemble(markets, attention_idx, target="brent"):
    px = markets[target].dropna()
    r = (100 * np.log(px).diff()).rename("r")
    a = attention_idx.reindex(r.index, method="ffill")  # attention of the trading day (pageviews of that UTC day)
    df = pd.concat([r, a], axis=1).dropna()
    return df


def predictive(df, train_end, prm=None, hmm=None):
    """Fit on rows < train_end, return params. Forecasts for row t use only rows < t."""
    tr = df.iloc[:train_end]
    hmm = hmm or hmm_fit(tr["attention"].values)
    _, ahead = hmm_filter(df["attention"].values, hmm)
    sig = ewma_sigma(df["r"].values)
    w = np.concatenate([[hmm["pi"][1]], ahead[:-1]])  # w[t] = P(tense on day t | attention up to t-1)
    if prm is None:
        prm = fit_mixture(tr["r"].values[20:], w[20:train_end], sig[20:train_end])
    return hmm, prm, w, sig


def backtest(markets, attention_idx, target="brent", start_train=250, refit_every=21, seed=7, n_samp=1500):
    df = assemble(markets, attention_idx, target)
    rng = np.random.default_rng(seed)
    rows = []
    hmm = prm = None
    for t in range(start_train, len(df)):
        if hmm is None or (t - start_train) % refit_every == 0:
            hmm, prm, w, sig = predictive(df, t)
        else:
            _, ahead = hmm_filter(df["attention"].values[: t + 1], hmm)
            w_t = ahead[t - 1]
            w = np.concatenate([w[:t], [w_t], w[t + 1:]])
        y = df["r"].values[t]
        s = sig[t]
        wt = w[t]
        dom = sample_mix(wt, s, prm, n_samp, rng)
        base = rng.standard_t(NU, size=n_samp) * T_SCALE * s
        p_big = 1 - (mix_cdf(BIG, wt, s, prm) - mix_cdf(-BIG, wt, s, prm))
        p_big_b = 2 * stats.t.sf(BIG / (s * T_SCALE), NU)
        rows.append({
            "date": df.index[t].strftime("%Y-%m-%d"), "actual": float(y), "sigma": float(s), "tension": float(wt),
            "median": float(np.median(dom)), "p10": float(np.quantile(dom, 0.1)), "p90": float(np.quantile(dom, 0.9)),
            "b_p10": float(np.quantile(base, 0.1)), "b_p90": float(np.quantile(base, 0.9)),
            "crps": crps_samples(dom, y), "crps_base": crps_samples(base, y),
            "logs": float(np.log(mix_pdf(y, wt, s, prm) + 1e-300)),
            "logs_base": float(stats.t.logpdf(y, NU, 0, s * T_SCALE)),
            "p_big": float(p_big), "p_big_base": float(p_big_b), "big": int(abs(y) > BIG),
            "surprise": float(-np.log(mix_pdf(y, wt, s, prm) + 1e-300)),
        })
    return pd.DataFrame(rows), {"hmm": {k: np.asarray(v).tolist() for k, v in hmm.items()}, "mixture": prm}


# ---------------------------------------------------------------------------------------------- statistics
def block_bootstrap_mean(x, block=10, n_boot=3000, seed=0):
    x = np.asarray(x, float)
    n = len(x)
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(n / block))
    means = np.empty(n_boot)
    for b in range(n_boot):
        starts = rng.integers(0, n - block + 1, size=nb)
        idx = (starts[:, None] + np.arange(block)[None, :]).ravel()[:n]
        means[b] = x[idx].mean()
    return {"mean": float(x.mean()), "lo": float(np.quantile(means, 0.025)), "hi": float(np.quantile(means, 0.975))}


def dm_test(loss_a, loss_b, lag=5):
    """Diebold-Mariano with Newey-West variance. Negative stat = model a better (lower loss)."""
    d = np.asarray(loss_a) - np.asarray(loss_b)
    n, dbar = len(d), d.mean()
    gamma = [np.mean((d[k:] - dbar) * (d[: n - k] - dbar)) for k in range(lag + 1)]
    var = gamma[0] + 2 * sum((1 - k / (lag + 1)) * gamma[k] for k in range(1, lag + 1))
    stat = dbar / math.sqrt(max(var, 1e-12) / n)
    return {"stat": float(stat), "p": float(2 * stats.norm.sf(abs(stat))), "mean_diff": float(dbar)}


def reliability(p, y, bins=(0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0)):
    out = []
    p, y = np.asarray(p), np.asarray(y)
    for lo, hi in zip(bins[:-1], bins[1:]):
        m = (p >= lo) & (p < hi)
        if m.sum():
            out.append({"bin": f"{lo:.2f}-{hi:.2f}", "pred": float(p[m].mean()), "obs": float(y[m].mean()), "n": int(m.sum())})
    return out


def summarize(bt):
    met = {}
    for name, a, b in (("crps", "crps", "crps_base"), ("log_score", "logs", "logs_base")):
        met[name] = {"domino": block_bootstrap_mean(bt[a]), "ewma_t": block_bootstrap_mean(bt[b]),
                     "diff": block_bootstrap_mean(bt[a] - bt[b])}
    cov = ((bt["actual"] >= bt["p10"]) & (bt["actual"] <= bt["p90"])).astype(float)
    cov_b = ((bt["actual"] >= bt["b_p10"]) & (bt["actual"] <= bt["b_p90"])).astype(float)
    met["coverage80"] = {"domino": block_bootstrap_mean(cov), "ewma_t": block_bootstrap_mean(cov_b)}
    br = (bt["p_big"] - bt["big"]) ** 2
    br_b = (bt["p_big_base"] - bt["big"]) ** 2
    met["brier_big_move"] = {"domino": block_bootstrap_mean(br), "ewma_t": block_bootstrap_mean(br_b),
                             "diff": block_bootstrap_mean(br - br_b), "base_rate": float(bt["big"].mean())}
    return met, {"crps": dm_test(bt["crps"], bt["crps_base"]), "brier": dm_test(br, br_b)}
