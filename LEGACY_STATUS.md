# Historical Model Validation Evidence and Status

## Current classification

This repository preserves legacy PPO research and validation evidence. The original PPO work remains valuable as a research baseline and as a historical foundation for later modular implementation and research architecture. However, it was developed under an earlier validation standard and should not be treated as production-grade or as current authorization for paper-trading order submission.

```text
Historical validation repository = legacy PPO research validation evidence
Later implementation repository = historical modular PPO implementation, execution research, and model-quality review
Current canonical repository = quantitative-trading-research-platform (research platform in development)
Future work = model development under stricter validation standards
```

These roles describe the research lineage and do not imply automatic promotion from historical validation to profitable or production deployment.

## Historical promotion decision

The following dispositions were reached at that stage of the project and are preserved as historical decisions rather than current authorization:

```text
Promote to no-submit deployment infrastructure: YES
Promote to controlled paper submit: NO
Promote to PPO-only trading readiness: NO
Promote to PPO + RF / PPO + XGBoost deployment: NO
Retrain legacy PPO immediately: NO
Run baseline model-quality audit first: YES
```

## Why the legacy evidence is insufficient

The original PPO training and validation pipeline evaluated PPO against buy-and-hold and recorded portfolio, Sharpe, and drawdown-style metrics. The saved model-info files appear to preserve mainly:

```text
final_portfolio
buy_hold
sharpe
```

Those fields are useful research evidence, but they are not enough for the current trading-readiness standard. The original process appears to have favored top windows by Sharpe ranking, which is not sufficient by itself for controlled paper submission or deployment. The preserved standalone PPO GE and UNH metrics came from rolling historical windows in which PPO was trained and then evaluated across the same `df_window`; those saved window metrics therefore should not be interpreted as independent out-of-sample validation results.

The later PPO + Random Forest research materially strengthened the historical methodology. It introduced chronological per-window train/evaluation separation, `OOS_ONLY` evaluation, backward temporal context alignment, explicit future-context/no-lookahead checks, and Random Forest participation gating. The repository also preserves gate thresholds, feature metadata, train/evaluation gate metrics, model-selector outputs, and PPO, RF-gate, VecNormalize, feature, and model-info artifacts. Even with those improvements, the evidence did not constitute an untouched final holdout or establish a stable trading edge or current trading readiness.

## Mixed PPO evidence examples

UNH showed a strong portfolio result in the saved window:

```text
final_portfolio = 209370.65
buy_hold = 82202.95
sharpe = 0.723
```

That is research-promising because PPO beat buy-and-hold in that saved window. However, the Sharpe value and saved evidence set are not strong enough by themselves to justify controlled submit under the newer standard.

GE showed the opposite benchmark-relative pattern:

```text
final_portfolio = 138399.56
buy_hold = 428005.8
sharpe = 0.926
```

PPO made money, but it dramatically underperformed buy-and-hold. That confirms mixed performance versus the benchmark and supports the legacy-baseline classification.

## Alpaca paper-trading reliability interpretation

The first Alpaca paper-trading reliability run passed operationally, but it did not prove trading edge:

```text
Start Equity = 93990.44
End Equity = 93735.77
Net Equity Change = -254.67
Return = -0.2710%
Estimated wins = 1
Estimated losses = 3
Estimated win rate = 25%
Estimated profit factor = about 0.31
```

Correct interpretation:

```text
Reliability pass, not edge pass.
Infrastructure proof, not profitability proof.
```

## Modern validation gaps before any future promotion

A future PPO v2 candidate should require stronger evidence, including:

- explicit embargo and stronger leakage controls
- untouched final holdout
- statistical confidence
- formal stability qualification across adjacent windows
- systematic benchmark-relative qualification
- transaction-cost and slippage sensitivity stress beyond fixed assumptions
- formal drawdown and turnover qualification
- candidate persistence
- preserved no-submit observation evidence
- clear final promotion / rejection gates

## Guardrails

Do not delete the original work. Do not describe the legacy model as useless. Do not claim controlled submit readiness. Do not claim PPO + RF or PPO + XGBoost readiness. Do not use feature importance, gate behavior, threshold sweeps, Sharpe, successful fills, or infrastructure behavior as proof of trading edge.

This repository should be read as historical PPO research-validation evidence and a historical source of validation and infrastructure-audit evidence, not as the current canonical project or a production system.
