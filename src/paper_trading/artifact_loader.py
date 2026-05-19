"""Load PPO artifacts and produce no-order target-weight predictions."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd

try:
    import gymnasium as gym
    from gymnasium import spaces
    from stable_baselines3 import PPO
    from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
except Exception as exc:  # pragma: no cover
    gym = None
    spaces = None
    PPO = None
    DummyVecEnv = None
    VecNormalize = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None

from .artifact_manifest import ArtifactEntry


@dataclass
class ArtifactBundle:
    entry: ArtifactEntry
    model: Any
    features: list[str]
    vecnormalize: Optional[Any]
    probability_config: dict[str, Any]
    model_info: dict[str, Any]


class SingleStepInferenceEnv(gym.Env if gym is not None else object):
    """Minimal env used only to attach VecNormalize statistics."""

    metadata = {"render_modes": []}

    def __init__(self, n_features: int):
        if spaces is None:
            raise RuntimeError("gymnasium is required for VecNormalize loading")
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(n_features,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
        self._obs = np.zeros((n_features,), dtype=np.float32)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        return self._obs.copy(), {}

    def step(self, action):
        return self._obs.copy(), 0.0, False, False, {}


def _read_json(path: Optional[Path], default: Any) -> Any:
    if path is None or not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _feature_list(raw: Any) -> list[str]:
    if isinstance(raw, list):
        return [str(x) for x in raw]
    if isinstance(raw, dict):
        for key in ("features", "feature_names", "columns", "feature_columns"):
            if isinstance(raw.get(key), list):
                return [str(x) for x in raw[key]]
    raise ValueError("Feature artifact must be a list or a dict containing a feature list")


def load_artifact_bundle(entry: ArtifactEntry) -> ArtifactBundle:
    if IMPORT_ERROR is not None:
        raise RuntimeError("PPO dry-run dependencies are missing. Run `pip install -r requirements.txt`.") from IMPORT_ERROR
    if not entry.model_path.exists():
        raise FileNotFoundError(f"Missing PPO model: {entry.model_path}")
    if not entry.features_path.exists():
        raise FileNotFoundError(f"Missing feature artifact: {entry.features_path}")

    features = _feature_list(_read_json(entry.features_path, []))
    model = PPO.load(str(entry.model_path), device="cpu")

    vecnormalize = None
    if entry.vecnormalize_path and entry.vecnormalize_path.exists():
        env = DummyVecEnv([lambda: SingleStepInferenceEnv(len(features))])
        vecnormalize = VecNormalize.load(str(entry.vecnormalize_path), env)
        vecnormalize.training = False
        vecnormalize.norm_reward = False

    return ArtifactBundle(
        entry=entry,
        model=model,
        features=features,
        vecnormalize=vecnormalize,
        probability_config=_read_json(entry.probability_config_path, {}),
        model_info=_read_json(entry.model_info_path, {}),
    )


def latest_observation(frame: pd.DataFrame, features: list[str], fill_policy: str) -> tuple[np.ndarray, list[str]]:
    if frame.empty:
        raise ValueError("Feature frame is empty")
    work = frame.copy()
    missing = [col for col in features if col not in work.columns]
    if missing and fill_policy == "strict":
        raise ValueError(f"Missing required model features: {missing}")
    for col in missing:
        work[col] = 0.0
    obs = (
        work[features]
        .replace([np.inf, -np.inf], np.nan)
        .ffill()
        .bfill()
        .fillna(0.0)
        .iloc[-1]
        .astype("float32")
        .to_numpy()
        .reshape(1, -1)
    )
    return obs, missing


def predict_target_weight(bundle: ArtifactBundle, frame: pd.DataFrame, weight_cap: float, deterministic: bool, fill_policy: str) -> dict[str, Any]:
    obs, missing = latest_observation(frame, bundle.features, fill_policy)
    if bundle.vecnormalize is not None:
        obs = bundle.vecnormalize.normalize_obs(obs)
    action, _ = bundle.model.predict(obs, deterministic=deterministic)
    raw_action = float(np.asarray(action).reshape(-1)[0])
    clipped_action = float(np.clip(raw_action, -1.0, 1.0))
    return {
        "symbol": bundle.entry.symbol,
        "raw_action": raw_action,
        "clipped_action": clipped_action,
        "target_weight": clipped_action * float(weight_cap),
        "feature_count": len(bundle.features),
        "missing_features_filled": missing,
    }
