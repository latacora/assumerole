import argparse
import botocore.session
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--role-arn", required=True, help="The role ARN to assume. Mandatory.")
parser.add_argument("--role-session-name", default="tempsession", help="A name for this session.")
parser.add_argument("--duration-seconds", default=3600, type=int, help="Credential lifetime in seconds.")
parser.add_argument("--empty-environ", action="store_true", help="Pass empty environment to child.")
parser.add_argument("argv", nargs="+", help="Argv for the subcommand to run")

def main():
    args = parser.parse_args()
    res = botocore.session.get_session().create_client("sts").assume_role(
        RoleArn=args.role_arn,
        RoleSessionName=args.role_session_name,
        DurationSeconds=args.duration_seconds
    )

    env = dict(
        AWS_ACCESS_KEY_ID=res["Credentials"]["AccessKeyId"],
        AWS_SECRET_ACCESS_KEY=res["Credentials"]["SecretAccessKey"],
        AWS_SESSION_TOKEN=res["Credentials"]["SessionToken"]
    )
    if not args.empty_environ:
        env = dict(os.environ, **env)
        env.pop("AWS_SECURITY_TOKEN", None)

    return subprocess.call(args.argv, env=env)

if __name__ == "__main__":
    sys.exit(main())
