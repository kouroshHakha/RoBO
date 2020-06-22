from robo.fmin import random_search

from .explorer import Explorer

class RandomExplorer(Explorer):

    def get_res(self):
        lower = self.space.bound[0]
        upper = self.space.bound[1]

        res = random_search(
            self.fn,
            lower,
            upper,
            num_iterations=self.params['niter'],
            output_path=str(self.output_path),
            rng=self.rng,
        )

        return res
