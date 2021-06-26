import argparse
import subprocess
from itertools import chain

target_paths = {
    "flask": "packages/flask",
    "grpc": "packages/grpc"
}

target_choices = list(target_paths.keys())

parser = argparse.ArgumentParser()
parser.add_argument("target", help="the target package to build",
                    choices=target_choices)
parser.add_argument("--platform", help="platform option which will be passed to buildx",
                    type=str, default="linux/arm64")
parser.add_argument("--tag", "-t", nargs='+',
                    help="the tags to attach", type=str, default=[])

args = parser.parse_args()

path = target_paths[args.target]
tags = chain.from_iterable([
    ["-t", "jensdll/google-coral-ml:latest"],
    *[("-t", f"jensdll/google-coral-ml:{tag}") for tag in args.tag]
])

subprocess.run(["docker", "buildx", "build", "--push",
                "-f", "Dockerfile.Flask",
                "--build-arg", f"path={path}",
                "--platform", args.platform, *tags, "."])
