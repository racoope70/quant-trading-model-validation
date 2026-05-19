# Phase 1 Reliability Validation — Alpaca Paper Trading

**Status: PASSED**

This folder documents the first broker-side reliability validation for the PPO paper-trading workflow. The purpose of this phase was not to prove profitability. The purpose was to confirm that trained PPO artifacts could be loaded, connected to Alpaca paper trading, used for live predictions, translated into paper orders, flattened safely, and logged with enough evidence for review.

## Validation run

| Field | Value |
|---|---:|
| Run folder | `2026-05-18_13-36-06` |
| Run version | `ppo_alpaca_reliability_v2` |
| Alpaca mode | Paper trading |
| Dry run | `False` |
| Data feed | `iex` |
| Model timeframe | `1H` |
| Decision cooldown | 10 minutes |
| Symbols traded in run | `UNH`, `GE` |
| Artifacts detected | `CVX`, `GE`, `UNH` |

## Result

Phase 1 Reliability: **PASSED**

Confirmed:

- PPO artifacts loaded correctly.
- Alpaca paper credentials connected.
- Models predicted successfully.
- Orders submitted and filled.
- No duplicate-order failures were observed.
- No missing-bar or stale-prediction failures were observed.
- Strict flatten completed successfully.
- Logs and run summaries were created.

## Key diagnostics

| Metric | Value |
|---|---:|
| Run-summary rows | 28 |
| Start equity | `$93,990.44` |
| End equity | `$93,735.77` |
| Net equity change | `$-254.67` |
| Return | `-0.2710%` |
| Max drawdown | `-0.2801%` |
| Average gross exposure | `26.8393%` |
| Maximum gross exposure | `32.3489%` |
| Submitted orders | 6 |
| Filled-like orders | 5 |
| Aggregate fill rate | `83.3333%` |
| Rejected-like orders | 0 |
| Canceled-like orders | 0 |

## Included evidence

| File | Purpose |
|---|---|
| `true_alpaca_evaluation_report.txt` | Reliability report generated from the paper-trading run. |
| `run_summary_sample.csv` | Decision-level portfolio/equity/exposure/model-signal sample. |
| `symbol_order_fill_summary.csv` | Per-symbol order/fill reliability summary. |
| `artifact_symbol_summary.csv` | Artifact inventory confirming model, VecNormalize, feature, probability config, and model-info files. |

## Interpretation

This validation supports broker-side reliability, not strategy profitability. The run finished negative on account equity, so it should be treated as an operational reliability pass only.

The appropriate next step is to keep this folder as validation evidence, then implement a clean VS Code dry-run module under `src/paper_trading/`. That dry-run should load the PPO artifact set, fetch Alpaca bars, predict target weights, compare target versus actual broker positions, and write logs without submitting orders.

## Deployment repository handoff

Final paper-trading implementation will continue in the separate VS Code deployment repository rather than inside this validation repository.

This repository is intended to preserve validation evidence, reliability reports, sample logs, run diagnostics, and reproducibility notes. The deployment repository is responsible for the production-style paper-trading system, including broker-loop implementation, local configuration, runtime controls, order-submission logic, and operational monitoring.

The current `v1` naming is appropriate if it represents the first stable deployable paper-trading implementation. Additional versioning is only necessary if the architecture, execution logic, or risk-control framework materially changes.

Recommended repository boundary:

```text
validation repository = validation evidence, reliability reports, run diagnostics, and reproducibility notes
deployment repository = executable VS Code paper-trading system, broker loop, runtime controls, and operational monitoring
```

## Clean repo split

```text
validation/
  paper_trading/
    phase_1_reliability/
      README.md
      true_alpaca_evaluation_report.txt
      run_summary_sample.csv
      symbol_order_fill_summary.csv
      artifact_symbol_summary.csv

src/
  paper_trading/
    __init__.py
    artifact_manifest.py
    artifact_loader.py
    paper_trade_dry_run.py

config/
  paper_trading_six_ticker_manifest.json
```

## Dry-run command

From the repo root:

```bash
python -m src.paper_trading.paper_trade_dry_run
```

The dry-run module is intentionally configured as no-order execution. It should be used to verify local artifact loading, Alpaca bar retrieval, PPO prediction, target-weight calculation, and target-vs-actual position logging before any order-submission module is introduced.
