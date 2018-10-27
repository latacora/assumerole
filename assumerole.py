import argparse
import boto3
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--role-arn", required=True, help="The role ARN to assume. Mandatory.")
parser.add_argument("--role-session-name", default="tempsession", help="A name for this session.")
parser.add_argument("--keep-environ", default=True, help="Pass parent environment variables to child")
parser.add_argument("argv", nargs="+", help="Argv for the subcommand to run")

def main():
    args = parser.parse_args()
    res = boto3.client("sts").assume_role(
        RoleArn=args.role_arn,
        RoleSessionName=args.role_session_name
    )
    return subprocess.call(
        args.argv,
        env=dict(
            os.environ if args.keep_environ else {},
            AWS_ACCESS_KEY_ID=res["Credentials"]["AccessKeyId"],
            AWS_SECRET_ACCESS_KEY=res["Credentials"]["SecretAccessKey"],
            AWS_SESSION_TOKEN=res["Credentials"]["SessionToken"]
        )
    )

if __name__ == "__main__":
    sys.exit(main())