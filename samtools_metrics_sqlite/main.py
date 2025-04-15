#!/usr/bin/env python

import argparse
import sys

import sqlalchemy

from samtools_metrics_sqlite import __version__
from samtools_metrics_sqlite.metrics import (
    samtools_flagstat,
    samtools_idxstats,
    samtools_stats,
)


def main() -> int:
    parser = argparse.ArgumentParser("samtools metrics to sqlite tool")

    # Required flags.
    parser.add_argument("--bam", required=True)
    parser.add_argument("--input_state", required=True)
    parser.add_argument(
        "--metric_name", required=True, choices=("flagstat", "idxstats", "stats")
    )
    parser.add_argument("--metric_path", required=True)
    parser.add_argument("--job_uuid", required=True)

    # Tool flags
    parser.add_argument("--vcf", required=False)
    parser.add_argument("--fasta", required=False)
    parser.add_argument("--version", action="version", version=__version__)

    # setup required parameters
    args = parser.parse_args()
    bam = args.bam
    input_state = args.input_state
    metric_name = args.metric_name
    metric_path = args.metric_path
    job_uuid = args.job_uuid

    sqlite_name = f"{job_uuid}.db"
    engine_path = f"sqlite:///{sqlite_name}"
    engine = sqlalchemy.create_engine(engine_path, isolation_level="SERIALIZABLE")

    if metric_name == "flagstat":
        samtools_flagstat.run(job_uuid, metric_path, bam, input_state, engine)
    elif metric_name == "idxstats":
        samtools_idxstats.run(job_uuid, metric_path, bam, input_state, engine)
    elif metric_name == "stats":
        samtools_stats.run(job_uuid, metric_path, bam, input_state, engine)
    else:
        sys.exit("No recognized tool was selected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
