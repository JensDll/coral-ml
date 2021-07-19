import argparse
import subprocess
from itertools import chain

REPOSITORY = "jensdll/coral-ml"

paths = {
    "socket": {
        "path": "packages/socket",
        "tag": "iot2050"
    }
}

parser = argparse.ArgumentParser()
parser.add_argument("--platform", help="platform option which will be passed to buildx",
                    type=str, default="linux/arm64")
parser.add_argument("--push", action="store_true")
parser.add_argument("target", help="the target package to build",
                    choices=list(paths.keys()))
parser.add_argument("versions", nargs='+',
                    help="the tags to attach", type=str, default=[])

args = parser.parse_args()

path = paths[args.target]["path"]
tag = paths[args.target]["tag"]

tags = chain.from_iterable([
    *[("-t", f"{REPOSITORY}:{tag}-{v}") for v in args.versions]
])

build_context = f"../{path}"

if args.push:
    subprocess.run(["docker", "buildx", "build", "--push",
                    "--platform", args.platform, *tags, build_context])
else:
    subprocess.run(["docker", "buildx", "build",
                    "--platform", args.platform, *tags, "--no-cache",
                    "--progress", "plain",
                    "-o", "type=docker",
                    "--no-cache", "--load", "."])
