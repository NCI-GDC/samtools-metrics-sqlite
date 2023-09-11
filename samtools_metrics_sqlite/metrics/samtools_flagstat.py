import re
import sys
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


def samtools_flagstat_to_df(metric_path: str) -> pd.DataFrame:
    columns = ['value_1', 'value_2', 'stat']
    df = pd.DataFrame(columns=columns)
    flagstat_re = re.compile("(^[\d]+) [\+] ([\d]+) (.*)$")
    with open(metric_path, 'r') as f_open:
        for line in f_open:
            line = line.strip()
            flagstat_match = flagstat_re.match(line)
            if flagstat_match is None:
                sys.exit('bad match on line: %s' % line)
            else:
                value_1 = flagstat_match.groups()[0]
                value_2 = flagstat_match.groups()[1]
                stat = flagstat_match.groups()[2]
                df.loc[len(df)] = [value_1, value_2, stat]
    return df


def run(
    job_uuid: str, metric_path: str, bam: str, input_state: str, engine: 'Engine'
) -> None:
    df = samtools_flagstat_to_df(metric_path)
    df['job_uuid'] = job_uuid
    df['bam'] = bam
    df['input_state'] = input_state
    table_name = 'samtools_flagstat'
    df.to_sql(table_name, engine, if_exists='append')
    return
