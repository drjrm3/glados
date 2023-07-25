[![build](https://github.com/drjrm3/glados/actions/workflows/build.yml/badge.svg)](https://github.com/drjrm3/glados/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/drjrm3/glados/branch/master/graph/badge.svg?token=XU0C1QE1J2)](https://codecov.io/gh/drjrm3/glados)

# GLADOS
Glados (**G**eneric **L**oad **A**u**d**iting **o**f **S**ervers) is a wrapper for [Prometheus](https://prometheus.io) allowing simple python functions to be fed into [Prometheus](https://prometheus.io) / [Grafana](https://grafana.com).
The aim is to allow those who wish to write `Turret`s which monitor specific metrics and feed them into Prometheus.
This allows for simple, uncommon, metrics to be pulled from the `Turret` and can include a simple JSON file (with time).

## Goals

Several goals on the horizon for this project include:

* Ability to write `Turret` plugins and "point" glados to those plugins to allow for non-native `Turret`s.
* Create a `Turret` from a JSON file, thuse allowing simple on-server JSON input.
* Ability to write a looping script which emits JSON output every N seconds and point glados to a directory of these scripts to create `Turrets` out of.

## License

Glados is released under the [MIT License.](LICENSE).
