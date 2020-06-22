from typing import Mapping, Any

import numpy as np
from pathlib import Path

from bb_eval_engine.util.importlib import import_bb_env
from bb_eval_engine.base import EvaluationEngineBase
from bb_eval_engine.data.design import Design

from utils.data.database import Database
from utils.file import write_pickle, read_pickle

from .space import Discrete, Space

from robo.fmin import bayesian_optimization

class BlackBoxExplorer:

    def __init__(self, params: Mapping[str, Any]):
        self.params = params
        self.env: EvaluationEngineBase = import_bb_env(params['env'])
        self.db: Database[Design] = Database(keep_sorted_list_of=['cost'])
        self.rng = np.random.RandomState(seed=self.params.get('seed', 10))

        space_dict = {}
        for param_key, param_item in self.env.params.items():
            lo, hi, step = param_item
            space_dict[param_key] = Discrete(lo, hi, step)
        self.space = Space(space_dict)

    def convert_designs(self, dsns: np.ndarray):
        # convert q x d np.array designs back to their design object
        converted_dsns = [Design(dsn.tolist(), self.env.spec_range.keys()) for dsn in dsns]
        return converted_dsns

    def fn(self, x): # minimize
        # NOTE: by default env assumes designs are given as index values of some design vector
        # in BO this is not true, they are just plain parameter values.
        x = self.space.snap_to_grid(x[None, :])
        dsn_objs = self.convert_designs(x)
        # we have to make sure designs have their value_dict setup before they are passed in
        for dsn in dsn_objs:
            for param_val, key in zip(dsn, self.env.params_vec.keys()):
                dsn.value_dict[key] = param_val

        dsn_objs = self.env.evaluate(dsn_objs, do_interpret=False)

        self.db.extend(dsn_objs)
        res = dsn_objs[0]['cost']
        return res

    def start(self):
        lower = self.space.bound[0]
        upper = self.space.bound[1]

        output_path = Path(self.params['output_path'])
        if not output_path.exists():
            output_path.mkdir(parents=True)

        res = bayesian_optimization(
            self.fn,
            lower,
            upper,
            maximizer=self.params.get('maximizer', 'scipy'),
            acquisition_func=self.params.get('acquisition_func', 'log_ei'),
            model_type=self.params.get('model_type', 'bohamiann'),
            num_iterations=self.params['niter'],
            output_path=self.params['output_path'],
            rng=self.rng,
        )
        write_pickle(Path(self.params['output_path']) / 'res.pkl', res, mkdir=True)
        return res

    def save(self, fname: Path) -> None:
        db_pickl = self.db.picklable()
        state = dict(db=db_pickl)
        fname.parent.mkdir(parents=True, exist_ok=True)
        write_pickle(fname, state)

    def load(self, fname: Path) -> None:
        state = read_pickle(fname)
        self.db = state['db'].convert_to_database()
        self.trials = state['trials']

