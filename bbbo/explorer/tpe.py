from hyperopt import hp, fmin, tpe, space_eval, Trials

from .explorer import Explorer
import numpy as np

class TPEExplorer(Explorer):

    def fn(self, *x):
        x = np.array(list(*x))
        return super().fn(x)

    def get_res(self):

        hp_space = []
        for dim, space_spec in self.space.space_info.items():
            hp_space.append(hp.uniform(dim, space_spec.lo, space_spec.hi))

        trials = Trials()
        best = fmin(
            self.fn,
            hp_space,
            algo=tpe.suggest,
            max_evals=self.params['niter'],
            rstate=self.rng,
            trials=trials,
        )

        x_list = [trials.vals[key] for key in self.space.space_info]
        y_list = trials.losses()

        return dict(
            X=np.array(x_list).T,
            y=np.array(y_list),
        )