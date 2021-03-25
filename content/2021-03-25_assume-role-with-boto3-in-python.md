Title: Assume a role with boto3 in Python
Date: 2021-03-25 01:17
Modified: 2021-03-25 01:17
Category: posts
Tags: Python, boto3, AWS, IAM
Slug: assume-role-with-boto3-in-python
Authors: Jitse-Jan
Summary:

The following script will use the `jjmain` profile defined in `~/.aws/credentials` and retrieve a session token after a MFA token is provided. With the session token the `admin-role` can be assumed and data from the AWS Cost Explorer is retrieved.

```
from datetime import datetime, timedelta

import boto3

ACCOUNT_NUMBER = 123456789
MAX_DURATION = 129600
NUM_DAYS = 30
USER = "jitse-jan"

# Prompt user for the MFA token
token = input("MFA token: ")
# Get the credentials to assume the role
session = boto3.session.Session(profile_name="jjmain")
sts_client = session.client("sts")
assumed_role_object = sts_client.get_session_token(
    DurationSeconds=MAX_DURATION,
    SerialNumber=f"arn:aws:iam::{ACCOUNT_NUMBER}:mfa/{USER}",
    TokenCode=token,
)
credentials = assumed_role_object["Credentials"]
# Setup the Cost Explorer client
ce_client = session.client(
    "ce",
    aws_access_key_id=credentials["AccessKeyId"],
    aws_secret_access_key=credentials["SecretAccessKey"],
    aws_session_token=credentials["SessionToken"],
)
# Get the cost and usage for the provided time period
now = datetime.utcnow().now()
start = (now - timedelta(days=NUM_DAYS)).strftime("%Y-%m-%d")
end = now.strftime("%Y-%m-%d")
data = ce_client.get_cost_and_usage(
    TimePeriod={"Start": start, "End": end},
    Granularity="MONTHLY",
    Metrics=["UnblendedCost"],
)
# Get the total unblended cost
total_cost = 0
for timeperiod in data["ResultsByTime"]:
    total_cost += float((timeperiod["Total"]["UnblendedCost"]["Amount"]))
print(f"Total unblended cost in the past {NUM_DAYS} days is {total_cost:.2f} USD")
```