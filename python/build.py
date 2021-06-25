from posixpath import join
import subprocess
import argparse
import os

target_paths = {
    "flask": os.path.join("packages", "flask"),
    "grpc": os.path.join("packages", "grpc")
}

parser = argparse.ArgumentParser()
parser.add_argument("target", help=f"the target package to build, possible values are: " +
                    ', '.join(target_paths.keys()))
group = parser.add_argument_group()
group.add_argument("--push", help="push the image to docker hub using buildx",
                   action="store_true")
group.add_argument("--platform", help="platform option which will be passed to buildx",
                   type=str, default="linux/amd64,linux/arm64")

args = parser.parse_args()

if args.target in target_paths:
    path = target_paths[args.target]
    if args.push:
        subprocess.run(["docker", "buildx", "build", "--push",
                        "-f", f"{path}/Dockerfile",
                        "--build-arg", f"path={path}",
                        "--platform", args.platform,
                        "-t", "jensdll/google-coral-ml:latest", "."])
    else:
        subprocess.run(["docker", "build",
                        "-f", f"{path}/Dockerfile",
                        "--build-arg", f"path={path}",
                        "-t", "flask",  "."])
else:
    print(f"'{args.target}' is not a valid target: {', '.join(target_paths.keys())}")
