from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from sqlalchemy.engine.base import Engine


def tsv_to_df(tsv_path: str, columns: list) -> pd.DataFrame:
    data_dict = dict()
    with open(tsv_path, "r") as f_open:
        for idx, line in enumerate(f_open):
            line = line.strip("\n")
            line_split = line.split("\t")
            data_dict[idx] = line_split
    df = pd.DataFrame.from_dict(data_dict, orient="index", columns=columns)
    return df


def run(
    job_uuid: str, metric_path: str, bam: str, input_state: str, engine: Engine
) -> None:
    columns = ["NAME", "LENGTH", "ALIGNED_READS", "UNALIGNED_READS"]
    df = tsv_to_df(metric_path, columns=columns)
    df["job_uuid"] = job_uuid
    df["bam"] = bam
    df["input_state"] = input_state
    table_name = "samtools_idxstats"
    df.to_sql(table_name, engine, if_exists="append")
    return
