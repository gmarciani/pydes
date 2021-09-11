# PyDES

*A pythonic discrete-event simulation suite*

*Coursework in Performance Modeling of Computer Systems and Networks*


## Requirements
* Python 3.8


## Build
Install all required packages with PIP, running:

    $> pip3 install -r requirements.txt


## Simulations
PyDES provides the user with the following simulation models:

* cloud: a simulation about Cloud computing

Launch a simulation, running:

    $> python simulation.py [MY_SIMULATION] --config [MY_CONFIGURATION]

where
*[MY_SIMULATION]* is the name of the simulation to launch, i.e. the package name contained in pydes.simulations, and
*[MY_CONFIGURATION]* is the relative path to the YAML configuration file for the simulation.

For example, to launch the cloud simulation, run:

    $> python simulation.py cloud --config simulations/cloud/sample.yaml


### Configuration
We state here a sample configuration, that is the one specified by *experiments/cloud/simulation.yaml*:

```yaml
general:
  t_stop: 50000
  replica: 3
  random:
    generator: "MarcianiMultiStream"
    seed: 123456789
cloudlet:
  n_servers: 20
cloud:
  t_service_rate_1: 0.75
  t_service_rate_2: 0.85
  t_setup: 95
```


## Experiments
The package provides experiment on randomness and simulations.
In package 'exp/rnd' you can find experiments on multi-stream Lehmer pseudo-random generator.
In package 'exp/simulation' you can find experiments on the simulated system.

Run the experiments and visualize results through the MATLAB Live Script `pmcsn.mlx`.

* `exp/rnd/modulus`: Find a suitable modulus for a multi-stream Lehmer pseudo-random generator, given the number of bits.
* `exp/rnd/mulfind`: Find suitable FP, MC, FP/MC multipliers for a multi-stream Lehmer pseudo-random generator, given a modulus.
* `exp/rnd/mulcheck`: Check FP, MC, FP/MC constraints for multipliers for a multi-stream Lehmer pseudo-random generator, given a modulus and a multiplier.
* `exp/rnd/jmpfind`: Find a suitable jumper for a multi-stream Lehmer pseudo-random generator, given a modulus, a multiplier and a number of streams.
* `exp/rnd/extremes`: Find a suitable jumper for a multi-stream Lehmer pseudo-random generator, given a modulus, a multiplier and a number of streams.
* `exp/rnd/kolmogorov-smirnov`: Find a suitable jumper for a multi-stream Lehmer pseudo-random generator, given a modulus, a multiplier and a number of streams.

To run an experiment:

    $> python3 pydes.py [EXPERIMENT_NAME] [EXPERIMENT_OPTIONS]

## Results

| Bits | Streams | Modulus    | Multiplier | Jumper | Jump Size | Spectral Test | Test of Extremes               | Test of Kolmogorov-Smirnov |
|------|---------|------------|------------|--------|-----------|---------------|--------------------------------|----------------------------|
| 32   | 128     | 2147483647 | 16807      | 188756 | 16776028  | Failed        | Failed (91.406% confidence)    | Succeeded                  |
| 32   | 128     | 2147483647 | 48271      | 40509  | 16775552  | Succeeded     | Succeeded (96.875% confidence) | Succeeded                  |
| 32   | 128     | 2147483647 | 50812      | 15707  | 16769483  | Succeeded     | Succeeded (97.656% confidence) | Failed                     |
| 32   | 256     | 2147483647 | 16807      | 36563  | 8335476   | Failed        | Succeeded (95.312% confidence) | Succeeded                  |
| 32   | 256     | 2147483647 | 48271      | 22925  | 8367782   | Succeeded     | Failed (92.969% confidence)    | Succeeded                  |
| 32   | 256     | 2147483647 | 50812      | 29872  | 8362647   | Succeeded     | Failed (94.531% confidence)    | Succeeded                  |


## Sample Simulations

### Performance Analysis (batchdim)
```
ALGORITHMS=(1 2)
BATCHDIMS=(10 20 30 40 50)

for algorithm in $ALGORITHMS; do
    for batchdim in $BATCHDIMS; do
        CONFIG="config/performance_analysis_${algorithm}.yaml"
        OUTDIR="out/performance_analysis/algorithm_${algorithm}/batchdim_${batchdim}"
        PARAMETERS="'{\"general\":{\"batchdim\": ${batchdim}}}'"
        ./pydes.py simulation-performance --config $CONFIG --outdir $OUTDIR --parameters '{"general":{"batchdim": ${batchdim}}}'
    done;
done;
```

### Performance Analysis (thresholds)
```
ALGORITHMS=("2")
THRESHOLDS=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20)

for algorithm in $ALGORITHMS; do
    for threshold in THRESHOLDS; do
        CONFIG="config/performance_analysis_${algorithm}.yaml"
        OUTDIR="out/performance_analysis/algorithm_${algorithm}/threshold_${threshold}"
        PARAMETERS='{"system":{"cloudlet":{"threshold": ${threshold}}}}'
        echo "./pydes.py simulation-performance --config $CONFIG --outdir $OUTDIR --parameters $PARAMETERS"
    done;
done;
```

#### Algorithm 1

```
./pydes.py simulate-performance --config config/performance_analysis_1.yaml --outdir out/performance_analysis/algorithm_1 --parameters '{"general": {"batches": 64, "batchdim": 128}, "system":{"cloudlet": {"n_servers": 20}}}'
```

#### Algorithm 2

```
./pydes.py simulate-performance --config config/performance_analysis_2.yaml --outdir out/performance_analysis/algorithm_2/threshold_20 --parameters '{"general": {"batches": 64, "batchdim": 128}, "system":{"cloudlet": {"n_servers": 20, "threshold": 20}}}'
```

### Analytical Solution

#### Algorithm 1

```
./pydes.py solve-cloud-cloudlet --config config/analytical_solution_1.yaml --outdir out/analytical_solution/algorithm_1
```

#### Algorithm 2

```
./pydes.py solve-cloud-cloudlet --config config/analytical_solution_2.yaml --outdir out/analytical_solution/algorithm_2/threshold_20
./pydes.py solve-cloud-cloudlet --config config/analytical_solution_2.yaml --outdir out/analytical_solution/algorithm_2/threshold_2 --parameters '{"system":{"cloudlet":{"n_servers": 2, "threshold": 2}}}'
```

### Validation

#### Algorithm 1

```
./pydes.py validate-cloud-cloudlet --analytical-result out/analytical_solution/algorithm_1/result.csv --simulation-result out/performance_analysis/algorithm_1/result.csv --outdir out/validation/algorithm_1
```

#### Algorithm 2

```
./pydes.py validate-cloud-cloudlet --analytical-result out/analytical_solution/algorithm_2/threshold_20/result.csv --simulation-result out/performance_analysis/algorithm_2/threshold_20/result.csv --outdir out/validation/algorithm_2/threshold_20
```

## Contributing
Install pre-commit
```
pip install pre-commit
```

Install pre-commit hook for the local repo:
```
pre-commit install
```

For the first time, run pre-commit checks on the whole codebase:
```
pre-commit run --all-files
```

## Authors
Giacomo Marciani, [mgiacomo@amazon.com](mailto:mgiacomo@amazon.com)


## References
* "Discrete-Event Simulation", 2006, L.M. Leemis, S.K. Park
* "Performance Modeling and Design of Computer Systems, 2013, M. Harchol-Balter


## License
The project is released under the [MIT License](https://opensource.org/licenses/MIT).
