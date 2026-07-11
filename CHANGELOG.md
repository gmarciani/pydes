# CHANGELOG

Unreleased
----------

- Raise unit-test coverage to 92% (tests for rnd generators/variates, analytical/Markov-chain
  solving, simulation engine and model, utils, metrics, the CLI, and the exp/* experiment scripts)
- Add tox-based linting (flake8, black) and type-checking (mypy), mirroring cli-wizard's tox setup
- Fix several bugs surfaced while writing tests (composite rnd variates reusing a single draw,
  a missed seed assignment in MarcianiSingleStream.put_seed, a stale "random"/"rnd" config key,
  a broken __getitem__ on MarkovState, an Enum-vs-string comparison in result_validator, a
  crashing test-kolmogorov-smirnov CLI subcommand, swapped atan2 arguments in
  linear_regression_line, and missing parent-directory creation in file_utils csv writers)

0.0.1
-----

- Release on GitHub and PyPi
