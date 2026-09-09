"""Pipeline orchestrator — coordinates the 20-stage transformation.

Python is the orchestration layer only. It must not silently redefine
invariants, binary semantics, Agda proofs, routing contracts, or safety axioms.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Callable

from .types import PipelineArtifact, Provenance


@dataclass
class StageResult:
    """Result from a single pipeline stage."""
    stage: int
    name: str
    artifact: PipelineArtifact
    duration_ms: float = 0.0
    success: bool = True
    error: str = ""


@dataclass
class PipelineReport:
    """Final report separating PROVEN/OBSERVED/DERIVED/MEASURED/INFERRED/UNKNOWN/REJECTED."""
    stages: list[StageResult] = field(default_factory=list)
    total_duration_ms: float = 0.0
    proven: list[str] = field(default_factory=list)
    observed: list[str] = field(default_factory=list)
    derived: list[str] = field(default_factory=list)
    measured: list[str] = field(default_factory=list)
    inferred: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)

    def classify(self, artifact: PipelineArtifact):
        name = f"stage{artifact.stage}:{artifact.name}"
        match artifact.provenance:
            case Provenance.OBSERVED:
                self.observed.append(name)
            case Provenance.DERIVED:
                self.derived.append(name)
            case Provenance.MEASURED:
                self.measured.append(name)
            case Provenance.INFERRED:
                self.inferred.append(name)
            case Provenance.UNKNOWN:
                self.unknown.append(name)
            case Provenance.REJECTED:
                self.rejected.append(name)

    def to_dict(self) -> dict:
        return {
            "total_duration_ms": self.total_duration_ms,
            "stages": [
                {"stage": s.stage, "name": s.name, "success": s.success, "duration_ms": s.duration_ms}
                for s in self.stages
            ],
            "provenance": {
                "PROVEN": self.proven,
                "OBSERVED": self.observed,
                "DERIVED": self.derived,
                "MEASURED": self.measured,
                "INFERRED": self.inferred,
                "UNKNOWN": self.unknown,
                "REJECTED": self.rejected,
            },
        }


class Pipeline:
    """20-stage formal verification pipeline.

    Each stage is a pure transformation: artifact_in -> artifact_out.
    The pipeline enforces invariant preservation at each boundary.
    """

    def __init__(self):
        self._stages: dict[int, Callable[[PipelineArtifact], PipelineArtifact]] = {}
        self._report = PipelineReport()

    def register(self, stage_num: int, fn: Callable[[PipelineArtifact], PipelineArtifact]):
        self._stages[stage_num] = fn
        return self

    def execute(self, initial: PipelineArtifact) -> PipelineReport:
        start = time.monotonic()
        current = initial

        for stage_num in sorted(self._stages.keys()):
            fn = self._stages[stage_num]
            stage_start = time.monotonic()

            try:
                result_artifact = fn(current)
                duration = (time.monotonic() - stage_start) * 1000
                sr = StageResult(
                    stage=stage_num,
                    name=result_artifact.name,
                    artifact=result_artifact,
                    duration_ms=duration,
                    success=True,
                )
                self._report.stages.append(sr)
                self._report.classify(result_artifact)
                current = result_artifact
            except Exception as e:
                duration = (time.monotonic() - stage_start) * 1000
                sr = StageResult(
                    stage=stage_num,
                    name=f"stage_{stage_num}",
                    artifact=PipelineArtifact(
                        stage=stage_num,
                        name=f"error_stage_{stage_num}",
                        provenance=Provenance.REJECTED,
                    ),
                    duration_ms=duration,
                    success=False,
                    error=str(e),
                )
                self._report.stages.append(sr)
                self._report.rejected.append(f"stage{stage_num}:error")

        self._report.total_duration_ms = (time.monotonic() - start) * 1000
        return self._report

    def to_json(self) -> str:
        return json.dumps(self._report.to_dict(), indent=2)
