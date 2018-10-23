Title: AWS Lambda development - Python & SAM
Date: 2018-10-23 10:40
Modified: 2018-10-23 10:40
Category: posts
Tags: DevOps, data architecture, serverless, AWS, data engineer, Lambda, SAM
Slug: aws-lambda-development-with-sam
Authors: Jitse-Jan
Summary: This tutorial explains how to write a lambda functions in Python, test it locally, deploy it to AWS and test it in the cloud using Amazon's SAM. The `README.md` inside the [`cookiecutter`](https://github.com/aws-samples/cookiecutter-aws-sam-python) template folder is used as the base of this tutorial.

## Requirements

* AWS CLI already configured with at least PowerUser permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Pipenv installed](https://github.com/pypa/pipenv)
    - `pip install pipenv`
* [Docker installed](https://www.docker.com/community-edition)
* [SAM Local installed](https://github.com/awslabs/aws-sam-local) 

## Preparation

Make sure **Python 3** is installed on the machine, either as default version or alongside Python 2. Check the available downloads on [Python.org](https://www.python.org/downloads/).

```bash
~/c/python-lambda-tutorial $ python --version
Python 2.7.15
~/c/python-lambda-tutorial $ python3 --version
Python 3.6.6
```

By installing Python, `pip` should be available on the machine. In case Python 3 is not the default Python interpreter, `pip` should be called with `pip3`. 

```bash
~/c/python-lambda-tutorial $ pip --version
pip 18.1 from /usr/local/lib/python2.7/site-packages/pip (python 2.7)
~/c/python-lambda-tutorial $ pip3 --version
pip 18.1 from /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pip (python 3.6)
```

Create the Python **virtual environment** using `pipenv`. `pipenv` is the recommended way to create virtual environments for Python. The same can be achieved using `conda` or `virtualenv` or other tools, but the preferred way for Python 3 is `pipenv`. ([Source](https://docs.python-guide.org/dev/virtualenvs/))

Install `pipenv`:

```bash
~/c/python-lambda-tutorial $ pip3 install pipenv
Collecting pipenv
...
Installing collected packages: pipenv
Successfully installed pipenv-2018.10.13
```

Create an environment for Python 3.6:

```bash
~/c/python-lambda-tutorial $ pipenv --python 3.6
Creating a virtualenv for this project…
Pipfile: /Users/jitsejan/code/python-lambda-tutorial/Pipfile
Using /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6m (3.6.6) to create virtualenv…
⠦Running virtualenv with interpreter /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6m
Using base prefix '/Library/Frameworks/Python.framework/Versions/3.6'
New python executable in /Users/jitsejan/.local/share/virtualenvs/python-lambda-tutorial-mfatrPYM/bin/python3.6m
Also creating executable in /Users/jitsejan/.local/share/virtualenvs/python-lambda-tutorial-mfatrPYM/bin/python
Installing setuptools, pip, wheel...done.

Virtualenv location: /Users/jitsejan/.local/share/virtualenvs/python-lambda-tutorial-mfatrPYM
```

Activate the environment:

```bash
~/c/python-lambda-tutorial $ pipenv shell
Launching subshell in virtual environment…
```

Install [AWS CLI](https://aws.amazon.com/cli/):

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ pipenv install awscli
Installing awscli…
...
Installing collected packages: urllib3, docutils, six, python-dateutil, jmespath, botocore, s3transfer, PyYAML, pyasn1, rsa, colorama, awscli
Successfully installed PyYAML-3.13 awscli-1.16.35 botocore-1.12.25 colorama-0.3.9 docutils-0.14 jmespath-0.9.3 pyasn1-0.4.4 python-dateutil-2.7.3 rsa-3.4.2 s3transfer-0.1.13 six-1.11.0 urllib3-1.23

Adding awscli to Pipfile's [packages]…
Pipfile.lock not found, creating…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
Updated Pipfile.lock (94bc2a)!
Installing dependencies from Pipfile.lock (94bc2a)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 12/12 — 00:00:03
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ aws --version
aws-cli/1.16.35 Python/3.6.6 Darwin/18.0.0 botocore/1.12.25

```

Install [AWS SAM CLI](https://github.com/awslabs/aws-sam-local):

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ pipenv install aws-sam-cli 
Installing aws-sam-cli…
...
Requirement already satisfied, skipping upgrade: docutils>=0.10 in /Users/jitsejan/.local/share/virtualenvs/python-lambda-tutorial-mfatrPYM/lib/python3.6/site-packages (from botocore<1.13.0,>=1.12.25->boto3~=1.5->aws-sam-cli) (0.14)
Collecting arrow (from jinja2-time>=0.1.0->cookiecutter~=1.6.0->aws-sam-cli)
Installing collected packages: enum34, click, itsdangerous, Werkzeug, MarkupSafe, Jinja2, Flask, docker-pycreds, websocket-client, certifi, chardet, idna, requests, docker, jsonschema, boto3, aws-sam-translator, arrow, jinja2-time, binaryornot, poyo, future, whichcraft, cookiecutter, pytz, tzlocal, regex, dateparser, pystache, aws-sam-cli
Successfully installed Flask-1.0.2 Jinja2-2.10 MarkupSafe-1.0 Werkzeug-0.14.1 arrow-0.12.1 aws-sam-cli-0.6.0 aws-sam-translator-1.6.0 binaryornot-0.4.4 boto3-1.9.25 certifi-2018.10.15 chardet-3.0.4 click-6.7 cookiecutter-1.6.0 dateparser-0.7.0 docker-3.5.0 docker-pycreds-0.3.0 enum34-1.1.6 future-0.16.0 idna-2.7 itsdangerous-0.24 jinja2-time-0.2.0 jsonschema-2.6.0 poyo-0.4.2 pystache-0.5.4 pytz-2018.5 regex-2018.8.29 requests-2.19.1 tzlocal-1.5.1 websocket-client-0.53.0 whichcraft-0.5.2

Adding aws-sam-cli to Pipfile's [packages]…
Pipfile.lock (a1782d) out of date, updating to (94bc2a)…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
Updated Pipfile.lock (a1782d)!
Installing dependencies from Pipfile.lock (a1782d)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 42/42 — 00:00:10
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ sam --version
SAM CLI, version 0.6.0
```

Install the template tool [`cookiecutter`](https://github.com/audreyr/cookiecutter):

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ pipenv install cookiecutter
Installing cookiecutter…
...

Adding cookiecutter to Pipfile's [packages]…
Pipfile.lock (23abb4) out of date, updating to (a1782d)…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
Updated Pipfile.lock (23abb4)!
Installing dependencies from Pipfile.lock (23abb4)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 42/42 — 00:00:11
```


Verify the environment:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ tree
.
├── Pipfile
└── Pipfile.lock

0 directories, 2 files
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ cat Pipfile 
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[dev-packages]

[packages]
awscli = "*"
aws-sam-cli = "*"
cookiecutter = "*"

[requires]
python_version = "3.6"
```

**Important**

Make sure the AWS credentials are saved in `~/.aws/credentials` with the following content and the ID and key replaced with the correct values.

```
[default]
aws_access_key_id=AAAAAAAAAAAAAAAAAAAA
aws_secret_access_key=aAaAaAaAaAaAaAaAaAaAaAaAaAaAaAaAaAaAaAaA
```

## Local development

Install the template with the minimal option set:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ cookiecutter gh:aws-samples/cookiecutter-aws-sam-python
project_name [Name of the project]: python-lambda-tutorial-project
project_short_description [A short description of the project]:
include_apigw [y]: n
include_xray [y]: n
include_safe_deployment [y]: n
include_experimental_make [n]: n
 [INFO]: Removing Makefile from project due to chosen options...
 [SUCCESS]: Project initialized successfully! You can now jump to python-lambda-tutorial-project folder
 [INFO]: python-lambda-tutorial-project/README.md contains instructions on how to proceed.
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ tree
.
├── Pipfile
├── Pipfile.lock
└── python-lambda-tutorial-project
    ├── Pipfile
    ├── Pipfile.lock
    ├── README.md
    ├── first_function
    │   ├── __init__.py
    │   └── app.py
    ├── requirements.txt
    ├── template.yaml
    └── tests
        └── unit
            ├── __init__.py
            └── test_handler.py

4 directories, 11 files
```

Navigate inside the `python-lambda-tutorial-project` folder and install the application and development dependencies. Note that this creates a different virtual environment, namely the one with the dependencies for the lambda function.

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ cd python-lambda-tutorial-project/
python-lambda-tutorial-mfatrPYM ~/c/p/python-lambda-tutorial-project $ pipenv install
Creating a virtualenv for this project…
Pipfile: /Users/jitsejan/code/python-lambda-tutorial/python-lambda-tutorial-project/Pipfile
Using /Users/jitsejan/.local/share/virtualenvs/python-lambda-tutorial-mfatrPYM/bin/python3.6m (3.6.6) to create virtualenv…
⠹Running virtualenv with interpreter /Users/jitsejan/.local/share/virtualenvs/python-lambda-tutorial-mfatrPYM/bin/python3.6m
Using real prefix '/Library/Frameworks/Python.framework/Versions/3.6'
New python executable in /Users/jitsejan/.local/share/virtualenvs/python-lambda-tutorial-project-scMbNPxZ/bin/python3.6m
Also creating executable in /Users/jitsejan/.local/share/virtualenvs/python-lambda-tutorial-project-scMbNPxZ/bin/python
Installing setuptools, pip, wheel...done.

Virtualenv location: /Users/jitsejan/.local/share/virtualenvs/python-lambda-tutorial-project-scMbNPxZ
Pipfile.lock (26f9f9) out of date, updating to (49fffa)…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
Updated Pipfile.lock (26f9f9)!
Installing dependencies from Pipfile.lock (26f9f9)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 8/8 — 00:00:03
python-lambda-tutorial-mfatrPYM ~/c/p/python-lambda-tutorial-project $ pipenv install -d
Installing dependencies from Pipfile.lock (26f9f9)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 17/17 — 00:00:04
```

The `cookiecutter` template will create a `first_function`. The function code is located in `first_function/app.py`, while the function itself is defined in the `template.yaml` as `FirstFunction`. Before we can test the function, we need to prepare the function for deployment. If we run the test without creating the deployment package, the tests will fail. Note that the first time the function is invoked, the `lambda:python3.6` image will be downloaded first.

Start the local lambda server:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial sam local start-lambda                                          
2018-10-17 12:54:38 Starting the Local Lambda Service. You can now invoke your Lambda Functions defined in your template through the endpoint.
2018-10-17 12:54:38  * Running on http://127.0.0.1:3001/ (Press CTRL+C to quit)
```

Call the `FirstFunction` with a simple JSON payload:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ echo '{"lambda": "payload"}' | sam local invoke FirstFunction
2018-10-17 12:55:37 Reading invoke payload from stdin (you can also pass it from file with --event)
2018-10-17 12:55:37 Invoking app.lambda_handler (python3.6)
2018-10-17 12:55:37 Found credentials in shared credentials file: ~/.aws/credentials

Fetching lambci/lambda:python3.6 Docker container image..............................................................................................
2018-10-17 12:55:48 Mounting /Users/jitsejan/code/python-lambda-tutorial/python-lambda-tutorial-project/first_function/build as /var/task:ro inside runtime container
START RequestId: 6928ee1b-e1df-4b0c-bd36-c181102fd447 Version: $LATEST
Unable to import module 'app': No module named 'app'
END RequestId: 6928ee1b-e1df-4b0c-bd36-c181102fd447
REPORT RequestId: 6928ee1b-e1df-4b0c-bd36-c181102fd447 Duration: 4 ms Billed Duration: 100 ms Memory Size: 128 MB Max Memory Used: 19 MB

{"errorMessage": "Unable to import module 'app'"}
```

To create the deployment, we first create a hashed `requirements.txt` from the `Pipfile`:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ pipenv lock -r > requirements.txt
/usr/local/lib/python2.7/site-packages/pipenv/vendor/vistir/compat.py:109: ResourceWarning: Implicitly cleaning up <TemporaryDirectory '/var/folders/06/61h5ywpd0936tr9cvk_gc38r0rr60q/T/pipenv-tjo3nI-requirements'>
  warnings.warn(warn_message, ResourceWarning)
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ cat requirements.txt                                           -i https://pypi.python.org/simple
boto3==1.9.25
botocore==1.12.25
docutils==0.14
jmespath==0.9.3
python-dateutil==2.7.3 ; python_version >= '2.7'
s3transfer==0.1.13
six==1.11.0
urllib3==1.23
```

Install the dependencies directly to the `build` folder of the function:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ pip install -r requirements.txt -t first_function/build/
Looking in indexes: https://pypi.python.org/simple
...
Installing collected packages: jmespath, docutils, urllib3, six, python-dateutil, botocore, s3transfer, boto3
Successfully installed boto3-1.9.25 botocore-1.12.25 docutils-0.14 jmespath-0.9.3 python-dateutil-2.7.3 s3transfer-0.1.13 six-1.11.0 urllib3-1.23
```

Finally, copy the `app.py` for the function to the `build` folder:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ cp -R first_function/app.py first_function/build/
```

We can test the function again and see that in this case we get the expected result as defined in `first_function/app.py`.

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ echo '{"lambda": "payload"}' | sam local invoke FirstFunction
2018-10-17 13:04:10 Reading invoke payload from stdin (you can also pass it from file with --event)
2018-10-17 13:04:10 Invoking app.lambda_handler (python3.6)
2018-10-17 13:04:10 Found credentials in shared credentials file: ~/.aws/credentials

Fetching lambci/lambda:python3.6 Docker container image......
2018-10-17 13:04:12 Mounting /Users/jitsejan/code/python-lambda-tutorial/python-lambda-tutorial-project/first_function/build as /var/task:ro inside runtime container
START RequestId: 8b3f19d2-9fd9-41bd-9842-c6347e18259f Version: $LATEST
END RequestId: 8b3f19d2-9fd9-41bd-9842-c6347e18259f
REPORT RequestId: 8b3f19d2-9fd9-41bd-9842-c6347e18259f Duration: 1149 ms Billed Duration: 1200 ms Memory Size: 128 MB Max Memory Used: 25 MB

{"hello": "world"}
```

To make testing simpler, we can write the JSON payload the `event.json` and call the function with the event file as an argument. 

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ echo '{"lambda": "payload"}' > event.json
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ sam local invoke -e event.json FirstFunction
2018-10-17 13:10:03 Invoking app.lambda_handler (python3.6)
2018-10-17 13:10:03 Found credentials in shared credentials file: ~/.aws/credentials

Fetching lambci/lambda:python3.6 Docker container image......
2018-10-17 13:10:04 Mounting /Users/jitsejan/code/python-lambda-tutorial/python-lambda-tutorial-project/first_function/build as /var/task:ro inside runtime container
START RequestId: ea8c34a0-c44f-4719-a20a-fdf6613d75d4 Version: $LATEST
END RequestId: ea8c34a0-c44f-4719-a20a-fdf6613d75d4
REPORT RequestId: ea8c34a0-c44f-4719-a20a-fdf6613d75d4 Duration: 1161 ms Billed Duration: 1200 ms Memory Size: 128 MB Max Memory Used: 25 MB

{"hello": "world"}
```

As we can see in the generated `app.py`, there is an `event` and `context` parameter. Simplify the `app.py` to the following to test the two parameters:

```python
import boto3
import json
import os


def runs_on_aws_lambda():
    """
        Returns True if this function is executed on AWS Lambda service.
    """
    return 'AWS_SAM_LOCAL' not in os.environ and 'LAMBDA_TASK_ROOT' in os.environ

session = boto3.Session()


def lambda_handler(event, context):
    """
        AWS Lambda handler
        
    """
    message = get_message(event, context)

    return message


def get_message(event, context):
    return { 
        "event": event,
        "function_name": context.function_name,
    }
```

Copy the `app.py` in the `build` folder and invoke the function again. We can see the output has changed and shows us more content.

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ cp -R first_function/app.py first_function/build/   
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ sam local invoke -e event.json FirstFunction
2018-10-17 13:18:11 Invoking app.lambda_handler (python3.6)
2018-10-17 13:18:11 Found credentials in shared credentials file: ~/.aws/credentials

Fetching lambci/lambda:python3.6 Docker container image......
2018-10-17 13:18:13 Mounting /Users/jitsejan/code/python-lambda-tutorial/python-lambda-tutorial-project/first_function/build as /var/task:ro inside runtime container
START RequestId: 7160a23c-f8db-4c22-bc95-34d8822b2427 Version: $LATEST
END RequestId: 7160a23c-f8db-4c22-bc95-34d8822b2427
REPORT RequestId: 7160a23c-f8db-4c22-bc95-34d8822b2427 Duration: 1003 ms Billed Duration: 1100 ms Memory Size: 128 MB Max Memory Used: 25 MB

{"event": {"lambda": "payload"}, "function_name": "test"}
```

## Deployment

First and foremost, we need a S3 bucket where we can upload our Lambda functions packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ aws s3 mb s3://lambda-artifacts
make_bucket: lambda-artifacts
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ aws s3 ls | grep lambda-artifacts
2018-10-17 13:25:24 lambda-artifacts
```

Run the following command to package our Lambda function to S3:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket lambda-artifacts
Uploading to dbafe95d37cbdd0d76a83e2c289f2536  7395857 / 7395857.0  (100.00%)
Successfully packaged artifacts and wrote output template to file packaged.yaml.
Execute the following command to deploy the packaged template
aws cloudformation deploy --template-file /Users/jitsejan/code/python-lambda-tutorial/python-lambda-tutorial-project/packaged.yaml --stack-name <YOUR STACK NAME>
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ sam deploy --template-file packaged.yaml --stack-name python-lambda-tutorial --capabilities CAPABILITY_IAM
Waiting for changeset to be created..
Waiting for stack create/update to complete
Successfully created/updated stack - python-lambda-tutorial
```

The deployment stack can be checked with CloudFormation too:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ aws cloudformation describe-stacks --stack-name python-lambda-tutorial --query 'Stacks[].Outputs'
[
    [
        {
            "OutputKey": "FirstFunction",
            "OutputValue": "arn:aws:lambda:eu-west-1:848373817713:function:python-lambda-tutorial-FirstFunction-10Z13KCZEJ575",
            "Description": "First Lambda Function ARN"
        }
    ]
]
```
We can list the available functions on AWS Lambda and search for `FirstFunction`:

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ aws lambda list-functions | grep FirstFunction
            "FunctionName": "python-lambda-tutorial-FirstFunction-10Z13KCZEJ575",
            "FunctionArn": "arn:aws:lambda:eu-west-1:848373817713:function:python-lambda-tutorial-FirstFunction-10Z13KCZEJ575",
            "Role": "arn:aws:iam::848373817713:role/python-lambda-tutorial-FirstFunctionRole-6V7HKJLXSE52",
```

## Running 
We can invoke the function on AWS Lambda with the following command, where the function name is copied from the output of the previous command. 

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ aws lambda invoke --invocation-type RequestResponse --function-name python-lambda-tutorial-FirstFunction-10Z13KCZEJ575 outputfile.txt
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
```

The result is written to `output.txt` and should contain the event and the function name.

```bash
python-lambda-tutorial-mfatrPYM ~/c/python-lambda-tutorial $ cat outputfile.txt                                                                                                      
{"event": {}, "function_name": "python-lambda-tutorial-FirstFunction-10Z13KCZEJ575"}
```