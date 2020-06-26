"""
Post Mortem Analysis Plot (pmap)
"""

import sys
from pathlib import Path
import seaborn as sns
sns.set_style('dark')

import numpy as np
import matplotlib.pyplot as plt
import shutil

from utils.file import read_pickle, read_yaml
from mpl_toolkits.axes_grid1 import make_axes_locatable

from bb_eval_engine.util.importlib import import_bb_env

from torch.utils.tensorboard import SummaryWriter

from utils.pdb import register_pdb_hook
register_pdb_hook()

def plot_evo_vec(time_vec, xvec, cvec,  xrange, name='', vmax=None, vmin=None):

    plt.close()
    fig = plt.figure()
    ax = plt.gca()
    cmap = ax.scatter(time_vec, xvec, c=cvec, s=5, cmap='viridis', vmax=vmax, vmin=vmin)
    ax.set_ylim(xrange)
    cbar = fig.colorbar(cmap, ax=[ax], location='left')
    cbar.set_label('value')
    ax.tick_params(bottom=True, left=True, direction='in')

    divider = make_axes_locatable(ax)
    ax_hist = divider.new_horizontal(size="50%", pad=0.05)
    fig.add_axes(ax_hist)

    sns.distplot(Xs[:, i], ax=ax_hist, hist=True, kde=False, vertical=True,
                 hist_kws={'range': xrange})
    ax_hist.tick_params(labelleft=False, labelbottom=False)

    if name:
        ax.set_title(name)

    return fig


def plot_with_lower_bnd(time_vec, yvec, name=''):

    plt.close()
    fig = plt.figure()
    ax = plt.gca()
    ax.scatter(time_vec, yvec, s=5)
    min_vec = np.minimum.accumulate(yvec)
    ax.plot(time_vec, min_vec, 'b--', alpha=0.5)
    ax.grid()
    ax.tick_params(bottom=True, left=True)
    if name:
        ax.set_title(name)
    return fig

if __name__ == '__main__':

    exper_path = Path(sys.argv[1])

    seed_paths = [x for x in exper_path.iterdir() if x.is_dir()]
    for seed_path in seed_paths:

        seed_name = seed_path.name
        output_path = seed_path / 'pmap_output'
        output_path.mkdir(exist_ok=True)

        writer_path = output_path / 'writer'
        if writer_path.exists():
            shutil.rmtree(writer_path)
        writer = SummaryWriter(log_dir=str(writer_path))

        res = read_pickle(seed_path / 'res.pkl')
        yaml_specs = read_yaml(seed_path / 'spec.yaml')
        env = import_bb_env(yaml_specs['env'])

        Xs = np.array(res['X'])
        costs = np.array(res['y'])
        vmax = 3
        values = -np.log(costs + 10 ** (-vmax))

        nsamples, xdim = Xs.shape
        time_cnt = np.arange(nsamples)

        params_names = list(env.params_vec.keys())

        prefix = f'{seed_path}/{seed_name}'
        for i in range(xdim):
            xmin = env.input_bounds[0][i] * 0.9
            if xmin == 0:
                xmin = -0.1
            xmax = env.input_bounds[1][i] * 1.1
            name = params_names[i]
            fig = plot_evo_vec(time_cnt, Xs[:, i], cvec=values, xrange=[xmin, xmax],
                               name=name, vmax=vmax, vmin=0)
            fig.savefig(output_path / f'{name}_vs_time.png', bbox_inches='tight')
            tag = f'{prefix}/params/{name}'
            writer.add_figure(tag, fig)

        fig = plot_with_lower_bnd(time_cnt, costs, name='cost')
        fig.savefig(output_path / f'cost_vs_time.png', bbox_inches='tight')
        writer.add_figure(f'{prefix}/optim/cost', fig)
        writer.flush()


