# Drone 0.8 -> 1.0 converter
This converts old 0.8 `.drone.yml` to a version 1.0 variant (or close to it).

# usage
Install deps by:
```
pip install ruamel.yaml
```
and then
```
python convert.py .drone.yml --output .drone-new.yaml
```

# Help
```
$ python convert.py --help
usage: convert.py [-h] [--output OUTPUT] input

positional arguments:
  input            Input .drone.yaml file.

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  Output name for new drone. Default: .drone-new.yml
```

# Notes
* anchors of elements which get converted are lost :-( . 
* if you use `ports` (e.g. in services for DB), you need to remove it as it's
 not supported by drone anymore (at least I didn't find it in the docs) and the same ports
 as the default service is exposed is assumed (e.g. 5432:5432 for Postgre).
* volumes are named by `vol-{0..}`. Rename to your liking.
* after the conversion, it's recommended to run, run `drone fmt` and `drone lint`
