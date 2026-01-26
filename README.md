# Market ML Signals (Production)

Production-ready market ML signals platform with a PPO-based walk-forward reference implementation, designed to support additional reinforcement learning and supervised models through a uniform feature, training, and signal-serving pipeline. Signals are exported via JSON and consumed by downstream execution platforms, including QuantConnect (LEAN) and Alpaca (paper/live).

---

## Status
PPO is the primary fully implemented and validated model. Additional models are under active development in a separate research repository and are being incrementally integrated into this architecture.

---

## What’s inside

- **Feature pipeline** — robust OHLCV normalization, wavelet denoising, technical + regime features, optional FinBERT sentiment.
- **Model zoo** — interchangeable learners behind a standard inference adapter.
- **Walk-forward training (PPO reference)** — rolling windows, confidence-based reward shaping, whipsaw penalty, regime filter.
- **Artifacts for production** — saved models, `VecNormalize`/scalers, feature lists, probability config.
- **Signal serving** — JSON schema for downstream consumers; QuantConnect strategy polls and trades.
- **Reporting** — summary metrics, daily risk plots (Sharpe, PSR, Win Rate), and run logs.

---

## Repo layout
## Repo layout

```text
quant-trading-model-zoo/
├── README.md
├── src/
│   ├── features/                # feature engineering, regimes, denoise
│   ├── models/                  # model wrappers (PPO, XGB, LGBM, etc.)
│   ├── adapters/                # one-line predict() adapters
│   └── serving/                 # JSON signal writer, web handler
├── training/
│   ├── walkforward_ppo.py       # reference walkforward trainer
│   └── configs/                 # hyperparams per symbol/bucket
├── artifacts/
│   ├── models/                  # *.zip / *.pkl / feature lists
│   └── signals/                 # latest live_signals.json
├── platforms/
│   └── quantconnect/
│       └── main.py              # ExternalSignalConsumer (polls JSON)
├── notebooks/                   # exploratory notebooks (optional)
├── scripts/                     # CLI helpers (train, serve, export)
├── reports/                     # backtest summaries/plots
└── .env.example                 # example secrets (no real keys)

```
---

## Models

### Reference implementation
- **PPO** — walk-forward training, reward shaping, and production signal serving

### Planned / scaffolded
- **Reinforcement Learning:** A2C, SAC, TD3, DDPG, Deep SARSA
- **Tree / Boosting:** XGBoost, LightGBM
- **Clustering:** KMeans (regime and feature bucketing)


## Platforms

- **QuantConnect:** consumer strategy polls your JSON (live_signals.json) and trades long-only with confidence sizing and freshness guard.**

- **Alpaca (paper/live):** adapters provided for live testing and execution; supports simple latency simulation and a pluggable broker router.**
