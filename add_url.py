import os
import sys

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

path_str = os.environ["ENTRY_PATH"]
url = os.environ["ENTRY_URL"]
segments = path_str.split("/")

yaml = YAML()
yaml.preserve_quotes = True

with open("config.yml", "r") as config_file:
    data = yaml.load(config_file)

node = data["forwards"]

for seg in segments[:-1]:
    if seg not in node:
        node[seg] = CommentedMap()
    elif not hasattr(node[seg], 'items'):
        print(f"ERROR: segment {seg!r} exists but is a scalar URL, not a mapping", file=sys.stderr)
        sys.exit(1)
    node = node[seg]

final_key = segments[-1]
if final_key in node:
    print(f"ERROR: key {final_key!r} already exists at path {path_str!r}", file=sys.stderr)
    sys.exit(1)

node[final_key] = url

with open("config.yml", "w") as config_file:
    yaml.dump(data, config_file)

print(f"Added {path_str!r} -> {url!r}")
