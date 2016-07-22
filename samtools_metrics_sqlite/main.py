#!/usr/bin/env python

import argparse
import logging
import os
import sys

import sqlalchemy

from .metrics import samtools_flagstat
from .metrics import samtools_idxstats
from .metrics import samtools_stats

def get_param(args, param_name):
    if vars(args)[param_name] == None:
        sys.exit('--'+ param_name + ' is required')
    else:
        return vars(args)[param_name]
    return

def setup_logging(tool_name, args, uuid):
    logging.basicConfig(
        filename=os.path.join(uuid + '_' + tool_name + '.log'),
        level=args.level,
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S_%Z',
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

def main():
    parser = argparse.ArgumentParser('samtools metrics to sqlite tool')

    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)

    # Required flags.
    parser.add_argument('--bam',
                        required = True
    )
    parser.add_argument('--input_state',
                        required = True
    )
    parser.add_argument('--metric_name',
                        required = True
    )
    parser.add_argument('--metric_path',
                        required = True
    )
    parser.add_argument('--uuid',
                        required = True
    )

    # Tool flags
    parser.add_argument('--vcf',
                        required = False
    )
    parser.add_argument('--fasta',
                        required = False
    )

    # setup required parameters
    args = parser.parse_args()
    bam = args.input_state
    input_state = args.input_state
    metric_name = args.metric_name
    metric_path = args.metric_path
    uuid = args.uuid

    logger = setup_logging('picard_' + metric_name, args, uuid)

    sqlite_name = uuid + '.db'
    engine_path = 'sqlite:///' + sqlite_name
    engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')

    if metric_name == 'flagstat':
        bam = get_param(args, 'bam')
        fasta = get_param(args, 'fasta')
        samtools_flagstat.run(uuid, metric_path, bam, input_state, engine, logger)
    elif metric_name == 'idxstats':
        bam = get_param(args, 'bam')
        fasta = get_param(args, 'fasta')
        input_state = get_param(args, 'input_state')
        vcf = get_param(args, 'vcf')
        samtools_idxstats.run(uuid, metric_path, bam, input_state, engine, logger)
    elif metric_name == 'stats':
        bam = get_param(args, 'bam')
        fasta = get_param(args, 'fasta')
        input_state = get_param(args, 'input_state')
        vcf = get_param(args, 'vcf')
        samtools_stats.run(uuid, metric_path, bam, input_state, engine, logger)
    else:
        sys.exit('No recognized tool was selected')
    return

if __name__ == '__main__':
    main()