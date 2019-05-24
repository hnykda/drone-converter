from ruamel.yaml import YAML

yaml = YAML()
yaml.default_flow_style = False


def convert_volumes(data):
    d = []
    to_append = []
    for ix, vol in enumerate(data):
        name = f"vol-{ix}"
        loc, cont = vol.split(":")
        d.append({"name": name, "path": cont})
        to_append.append({"name": name, "host": {"path": loc}})
    return d, to_append


def convert_secrets(data):
    d = {}
    for x in data:
        if isinstance(x, str):
            d[x] = {"from_secret": x}
        else:
            d[x["target"]] = {"from_secret": x["source"]}
    return d


def convert_environment(data):
    d = {}
    for x in data:
        target, value = x.split("=")
        d[target] = value
    return d


def convert_data(_data):
    d = {}
    volumes = []
    secrets = {}
    environment = {}
    for key, data in _data.items():
        if key == "volumes":
            present_vols, to_append = convert_volumes(data)
            d["volumes"] = present_vols
            volumes += to_append
        elif key == "secrets":
            secrets = convert_secrets(data)
        elif key == "environment":
            environment = convert_environment(data)
        elif key == "ports":
            d["settings"] = {"ports": data}
        else:
            d[key] = data

        if secrets:
            environment = {**environment, **secrets}
        if environment:
            d["environment"] = environment
    return d, volumes


def convert_to_steps(pipe):
    steps = []
    volumes = []
    for step_name, step_data in pipe.items():
        new_data, vols = convert_data(step_data)
        volumes += vols
        steps.append({"name": step_name, **new_data})
    return steps, volumes


def unique(d):
    uniques = {}
    for x in d:
        h = hash(str(x))
        if h not in uniques:
            uniques[h] = x
    return list(uniques.values())


def convert_drone(data):
    new_drone = {
        "kind": "pipeline",
        "name": "default",
        "platform": {"os": "linux", "arch": "amd64"},
    }

    new_drone["steps"], volumes = convert_to_steps(data["pipeline"])

    if "services" in data:
        new_drone["services"], service_volumes = convert_to_steps(data["services"])
        volumes += service_volumes

    if volumes:
        new_drone["volumes"] = unique(volumes)
    return new_drone


def main(input_file, output_file):
    with open(input_file, "r") as ifile:
        inpt = yaml.load(ifile)

    converted = convert_drone(inpt)

    with open(output_file, "w") as ofile:
        yaml.dump(converted, ofile)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input .drone.yaml file.")
    parser.add_argument(
        "--output",
        help="Output name for new drone. Default: .drone-new.yml",
        default=".drone-new.yml",
    )
    args = parser.parse_args()
    main(args.input, args.output)
