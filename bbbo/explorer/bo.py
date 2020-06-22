from robo.fmin import bayesian_optimization

from .explorer import Explorer

class BOExplorer(Explorer):

    def get_res(self):
        lower = self.space.bound[0]
        upper = self.space.bound[1]

        res = bayesian_optimization(
            self.fn,
            lower,
            upper,
            maximizer=self.params.get('maximizer', 'scipy'),
            acquisition_func=self.params.get('acquisition_func', 'log_ei'),
            model_type=self.params.get('model_type', 'bohamiann'),
            num_iterations=self.params['niter'],
            output_path=str(self.output_path),
            rng=self.rng,
        )

        return res
