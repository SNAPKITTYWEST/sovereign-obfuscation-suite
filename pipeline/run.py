"""Pipeline runner — executes the full 20-stage transformation.

Usage:
    python -m pipeline.run
    python -m pipeline.run --with-activations
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core.pipeline import Pipeline
from .core.types import PipelineArtifact, Provenance
from .stages import ALL_STAGES


def build_pipeline(with_activations: bool = False) -> Pipeline:
    """Register all 20 stages in order."""
    pipe = Pipeline()

    for stage_num in sorted(ALL_STAGES.keys()):
        pipe.register(stage_num, ALL_STAGES[stage_num])

    return pipe


def create_initial_artifact(with_activations: bool = False) -> PipelineArtifact:
    """Create the initial pipeline input."""
    data = {
        "observed_input": "test_model_execution",
        "observed_tokens": [101, 2023, 3012, 102],
    }

    if with_activations:
        data["activations"] = [
            [0.1, 0.2, 0.3, 0.4],
            [0.5, 0.6, 0.7, 0.8],
            [0.9, 1.0, 1.1, 1.2],
        ]
    else:
        data["activations"] = None

    return PipelineArtifact(
        stage=0,
        name="initial_input",
        data=data,
        provenance=Provenance.OBSERVED,
    )


def main():
    parser = argparse.ArgumentParser(description="Run the 20-stage formal verification pipeline")
    parser.add_argument("--with-activations", action="store_true", help="Provide latent activations")
    parser.add_argument("--output", type=str, default=None, help="Output JSON file")
    args = parser.parse_args()

    pipe = build_pipeline(with_activations=args.with_activations)
    initial = create_initial_artifact(with_activations=args.with_activations)

    print("=" * 60)
    print("SOVEREIGN FORMAL VERIFICATION PIPELINE")
    print("20-Stage Transformation: Observable → Agda")
    print("=" * 60)
    print()

    report = pipe.execute(initial)

    print(f"Completed {len(report.stages)} stages in {report.total_duration_ms:.1f}ms")
    print()

    for sr in report.stages:
        status = "OK" if sr.success else "FAIL"
        print(f"  [{sr.stage:2d}] {sr.name:30s} {status:4s} ({sr.duration_ms:.1f}ms)")

    print()
    print("PROVENANCE CLASSIFICATION:")
    for cls, items in [
        ("OBSERVED", report.observed),
        ("DERIVED", report.derived),
        ("MEASURED", report.measured),
        ("INFERRED", report.inferred),
        ("UNKNOWN", report.unknown),
        ("REJECTED", report.rejected),
    ]:
        if items:
            print(f"  {cls:12s}: {', '.join(items)}")

    output_path = args.output or "pipeline_report.json"
    with open(output_path, "w") as f:
        f.write(pipe.to_json())
    print(f"\nReport written to {output_path}")


if __name__ == "__main__":
    main()
