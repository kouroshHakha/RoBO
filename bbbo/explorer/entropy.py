from robo.fmin import entropy_search

from .explorer import Explorer

class EntropyExplorer(Explorer):

    def get_res(self):
        lower = self.space.bound[0]
        upper = self.space.bound[1]

        res = entropy_search(
            self.fn,
            lower,
            upper,
            maximizer=self.params.get('maximizer', 'scipy'),
            num_iterations=self.params['niter'],
            output_path=str(self.output_path),
            rng=self.rng,
        )

        return res