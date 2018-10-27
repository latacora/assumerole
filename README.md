# assumerole

A tiny Python script that runs a subcommand, specified by its argv, with an
assume role, specified by environment variables.

It's weird to me that this needs to exist. There are a lot of tools that sort-of
do this? But all of them want to look at an AWS configuration profile for some
reason: they're all aimed at _humans_ temporarily assuming roles. Most of them
are basically aws-vault without the keychain functionality.

This is intended for services that need to temporarily assume a particular role
for a subprocess. There's no caching, no magic, no nothing: just some
environment variables that get set following an `aws sts assume-role` call (via
boto3).

```
usage: assumerole.py [-h] --role-arn ROLE_ARN
                     [--role-session-name ROLE_SESSION_NAME]
                     [--keep-environ KEEP_ENVIRON]
                     argv [argv ...]

positional arguments:
  argv                  Argv for the subcommand to run

optional arguments:
  -h, --help            show this help message and exit
  --role-arn ROLE_ARN   The role ARN to assume. Mandatory.
  --role-session-name ROLE_SESSION_NAME
                        A name for this session.
  --keep-environ KEEP_ENVIRON
                        Pass parent environment variables to child
```
