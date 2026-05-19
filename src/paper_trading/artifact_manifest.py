"""Resolve PPO artifact paths from a manifest.

The manifest keeps deployable paper-trading code separate from validation
reports.  It supports either explicit artifact paths or symbol-level glob
patterns under an artifacts directory.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any, Mapping, Optional


DEFAULT_PATTERNS = {
    "model": ["ppo_{symbol}_window*_model.zip", "*{symbol}*model.zip"],
    "vecnormalize": [
        "ppo_{symbol}_window*_vecnorm.pkl",
        "ppo_{symbol}_window*_vecnormalize.pkl",
        "*{symbol}*vecnorm*.pkl",
        "*{symbol}*vecnormalize*.pkl",
    ],
    "features": ["ppo_{symbol}_window*_features.json", "*{symbol}*features.json"],
    "probability_config": [
        "ppo_{symbol}_window*_probability_config.json",
        "*{symbol}*probability_config.json",
    ],
    "model_info": ["ppo_{symbol}_window*_model_info.json", "*{symbol}*model_info.json"],
}


@dataclass(frozen=True)
class ArtifactEntry:
    symbol: str
    model_path: Path
    features_path: Path
    vecnormalize_path: Optional[Path] = None
    probability_config_path: Optional[Path] = None
    model_info_path: Optional[Path] = None
    window: Optional[int] = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "window": self.window,
            "model_path": str(self.model_path),
            "features_path": str(self.features_path),
            "vecnormalize_path": str(self.vecnormalize_path) if self.vecnormalize_path else None,
            "probability_config_path": str(self.probability_config_path) if self.probability_config_path else None,
            "model_info_path": str(self.model_info_path) if self.model_info_path else None,
        }


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_path(value: str | Path, root: Path | None = None) -> Path:
    p = Path(value).expanduser()
    return p if p.is_absolute() else ((root or repo_root()) / p).resolve()


def read_manifest(path: str | Path) -> dict[str, Any]:
    with resolve_path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def _window(path: Path) -> int:
    m = re.search(r"window(\d+)", path.name, flags=re.I)
    return int(m.group(1)) if m else -1


def _best(paths: list[Path]) -> Optional[Path]:
    existing = sorted({p.resolve() for p in paths if p.exists()})
    if not existing:
        return None
    return sorted(existing, key=lambda p: (_window(p), p.stat().st_mtime, p.name))[-1]


def _glob(artifacts_dir: Path, symbol: str, kind: str, patterns: Mapping[str, list[str]]) -> Optional[Path]:
    matches: list[Path] = []
    for pattern in patterns.get(kind, []):
        matches.extend(artifacts_dir.glob(pattern.format(symbol=symbol)))
    return _best(matches)


def _explicit(row: Mapping[str, Any], root: Path) -> ArtifactEntry:
    return ArtifactEntry(
        symbol=str(row["symbol"]).upper(),
        model_path=resolve_path(row["model_path"], root),
        features_path=resolve_path(row["features_path"], root),
        vecnormalize_path=resolve_path(row["vecnormalize_path"], root) if row.get("vecnormalize_path") else None,
        probability_config_path=resolve_path(row["probability_config_path"], root) if row.get("probability_config_path") else None,
        model_info_path=resolve_path(row["model_info_path"], root) if row.get("model_info_path") else None,
        window=row.get("window"),
    )


def resolve_entries(manifest: Mapping[str, Any], root: Path | None = None) -> list[ArtifactEntry]:
    root = (root or repo_root()).resolve()
    if manifest.get("artifacts"):
        return [_explicit(row, root) for row in manifest["artifacts"]]

    artifacts_dir = resolve_path(manifest.get("artifacts_dir", "artifacts"), root)
    symbols = [str(s).upper() for s in manifest.get("symbols", [])]
    user_patterns = manifest.get("artifact_patterns") or {}
    patterns = {k: list(user_patterns.get(k, v)) for k, v in DEFAULT_PATTERNS.items()}

    entries: list[ArtifactEntry] = []
    missing: list[str] = []
    for symbol in symbols:
        model = _glob(artifacts_dir, symbol, "model", patterns)
        features = _glob(artifacts_dir, symbol, "features", patterns)
        if model is None or features is None:
            missing.append(symbol)
            continue
        entries.append(
            ArtifactEntry(
                symbol=symbol,
                model_path=model,
                features_path=features,
                vecnormalize_path=_glob(artifacts_dir, symbol, "vecnormalize", patterns),
                probability_config_path=_glob(artifacts_dir, symbol, "probability_config", patterns),
                model_info_path=_glob(artifacts_dir, symbol, "model_info", patterns),
                window=_window(model),
            )
        )
    if missing:
        print("[artifact_manifest] Missing required model/features artifacts for: " + ", ".join(missing))
    return entries


def load_manifest_entries(manifest_path: str | Path) -> tuple[dict[str, Any], list[ArtifactEntry]]:
    manifest = read_manifest(manifest_path)
    return manifest, resolve_entries(manifest, repo_root())
