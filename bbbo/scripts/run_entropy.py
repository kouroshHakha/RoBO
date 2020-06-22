import argparse

from utils.file import read_yaml
from utils.pdb import register_pdb_hook
register_pdb_hook()

import logging
logging.basicConfig(level=logging.INFO)

from bbbo.explorer.entropy import EntropyExplorer

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('spec', type=str, help='input yaml file.')

    _args = parser.parse_args()
    return _args


if __name__ == '__main__':

    _args = _parse_args()

    spec = read_yaml(_args.spec)
    explorer = EntropyExplorer(spec)
    res = explorer.start()