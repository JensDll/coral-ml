import argparse
import subprocess
from itertools import chain

REPOSITORY = "jensdll/google-coral-ml"

targets = {
    "flask_video": {
        "path": "packages/flask_video",
        "dockerfile": "Dockerfile.Flask.Video"
    },
    "grpc": {
        "path": "packages/grpc",
        "dockerfile": "nan"
    }
}

parser = argparse.ArgumentParser()
parser.add_argument("target", help="the target package to build",
                    choices=list(targets.keys()))
parser.add_argument("--platform", help="platform option which will be passed to buildx",
                    type=str, default="linux/arm64")
parser.add_argument("--tag", "-t", nargs='+',
                    help="the tags to attach", type=str, default=[])
args = parser.parse_args()

path = targets[args.target]["path"]
dockerfile = targets[args.target]["dockerfile"]

tags = chain.from_iterable([
    ["-t", f"{REPOSITORY}:latest"],
    *[("-t", f"{REPOSITORY}:{tag}") for tag in args.tag]
])

subprocess.run(["docker", "buildx", "build", "--push",
                "-f", dockerfile,
                "--build-arg", f"path={path}",
                "--platform", args.platform, *tags, "."])
