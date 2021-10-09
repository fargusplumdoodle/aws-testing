#!/usr/bin/python3
import time
import sys

import boto3
from botocore.exceptions import ClientError
import yaml

with open("./template.yaml", "r") as in_file:
    template = in_file.read()

with open("./stack.yaml", "r") as in_file:
    stack = yaml.load(in_file, Loader=yaml.Loader)

with open("./user_data.sh", "r") as in_file:
    user_data = in_file.read()

client = boto3.client("cloudformation", region_name=stack["region"])

stack["params"]["UserData"] = user_data
stack_call_args = {
    "StackName": stack["name"],
    "TemplateBody": template,
    "Parameters": [
        {"ParameterKey": k, "ParameterValue": str(v)}
        for k, v in stack["params"].items()
    ],
    "Capabilities": ["CAPABILITY_NAMED_IAM"],
}


arg = sys.argv[1]
if arg == "delete":
    response = client.delete_stack(StackName=stack["name"])
    print("deleted")
if arg == "update":
    response = client.update_stack(**stack_call_args)
    print(f"Updating stack {stack['name']}, ID {response['StackId']}")
if arg == "create":
    response = client.create_stack(**stack_call_args)
    print(f"Creating stack {stack['name']}, ID {response['StackId']}")
