# Legacy PPO Validation Status

## Current classification

This repository preserves legacy PPO research validation evidence. The original PPO work was not useless. It was research-promising and infrastructure-worthy, but it is not production-paper-submit-ready under the current standard.

```text
Old validation repo = legacy PPO research validation evidence
Current deployment repo = governed no-submit infrastructure and audit pipeline
Future work = PPO v2 retraining under stricter validation standards
```

## Promotion decision

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

Those fields are useful research evidence, but they are not enough for the current trading-readiness standard. The older process appears to have favored top windows by Sharpe ranking, which is not sufficient by itself for controlled paper submission or deployment.

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
Win rate = 25%
Estimated profit factor = about 0.31
```

Correct interpretation:

```text
Reliability pass, not edge pass.
Infrastructure proof, not profitability proof.
```

## Modern validation gaps before any future promotion

A future PPO v2 candidate should require stronger evidence, including:

- embargo / leakage controls
- untouched holdout
- statistical confidence
- stability across adjacent windows
- benchmark-relative performance
- transaction-cost and slippage stress
- drawdown and turnover review
- candidate persistence
- live no-submit observation behavior
- clear promotion / rejection gates

## Guardrails

Do not delete the old work. Do not describe the old model as useless. Do not claim controlled submit readiness. Do not claim PPO + RF or PPO + XGBoost readiness. Do not use feature importance, gate behavior, or threshold sweeps as proof of trading edge.

This repository should be read as legacy PPO research validation evidence and an infrastructure audit fixture.
