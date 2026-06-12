
import argparse
import os


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Run direct generation for various datasets and models.")

    parser.add_argument(
        '--subset-num',
        type=int,
        default=os.getenv('EVAL_SUBSET_NUM', '-1'),
        help=(
            "Number of examples to process. Defaults to EVAL_SUBSET_NUM, "
            "or all examples when neither is specified."
        )
    )


    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help="Enable debug mode. Defaults to False."
    )
    parsed_args = parser.parse_args() if args is None else parser.parse_args(args)
    
    return parsed_args
