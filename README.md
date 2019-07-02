# Drone 0.8 -> 1.0 converter
This converts old 0.8 `.drone.yml` to a version 1.0 variant (or close to it).

According to [this](https://discourse.drone.io/t/conversion-of-drone-yml-from-0-8-to-1-0/4670?u=kotrfa)
you should use `drone convert`. Unfortunately, that tool can't handle some of the yaml's
features such as `<<: *anchor` or escaping in commands. This tool can be used as a complementary
to the original one. I had to do some manual adjustments by hand anyway. 

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
* (todo) plugins are not converted correctly (keys should go under `settings`)
* anchors of elements which get converted are lost 
* volumes are named by `vol-{0..}`. Rename to your liking.
* after the conversion, it's recommended to run, run `drone fmt` and `drone lint`
