RoBO - a Robust Bayesian Optimization framework.
================================================

Master Branch
------------------
[![Build Status](https://travis-ci.org/automl/RoBO.svg?branch=master)](https://travis-ci.org/automl/RoBO)
[![Coverage Status](https://coveralls.io/repos/github/automl/RoBO/badge.svg?branch=master)](https://coveralls.io/github/automl/RoBO?branch=master)
[![Code Health](https://landscape.io/github/automl/RoBO/master/landscape.svg?style=flat)](https://landscape.io/github/automl/RoBO/master)


Installation
------------

RoBO uses the Gaussian processes library [george](https://github.com/automl/george.git) and the random forests library [pyrfr](https://github.com/automl/random_forest_run). In order to use these libraries make sure that libeigen and swig are installed:

```
sudo apt-get install libeigen3-dev swig 
```

Download RoBO and then change into the new directory:

```
git clone https://github.com/automl/RoBO
cd RoBO/
```

Install the required dependencies.
```
for req in $(cat requirements.txt); do pip install $req; done
```

Finally install RoBO by:

```
python setup.py install
```



Documentation
-------------
You can find the documentation for RoBO here http://automl.github.io/RoBO/


Citing RoBO
-----------

To cite RoBO please reference our BayesOpt paper:
```
@INPROCEEDINGS{klein-bayesopt17,
author    = {A. Klein and S. Falkner and N. Mansur and F. Hutter},
title     = {RoBO: A Flexible and Robust Bayesian Optimization Framework in Python},
booktitle = {NIPS 2017 Bayesian Optimization Workshop},
year      = {2017},
month     = dec,
}
```

Using RoBo on ngspice Circuit Design
------------------------------------

example code:

```
./run.sh bbbo/scripts/run_bo specs/opamp.yaml
./run.sh bbbo/scripts/run_pmap $RUNDIR
```

Content of yaml file:
```yaml
env: bb_envs/src/bb_envs/ngspice/envs/two_stage_opamp_1.yaml
seed: 20                          // seed number 
niter: 1000                       // number of iterations
maximizer: random                 // optional parameter for bo Explorer
acquisition_func: lcb             // optional parameter for bo Explorer
model_type: bohamiann             // optional parameter for bo Explorer
output_path: runs/opamp/tpe/s20   // output path (very important to pick a descriptive name)
```