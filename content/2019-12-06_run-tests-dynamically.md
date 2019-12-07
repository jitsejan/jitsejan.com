Title: Run tests dynamically
Date: 2019-12-06 01:56
Modified: 2019-12-07 04:13
Category: posts
Tags: Python, pytest, dynamic, testing, availability, AWS, boto3, API
Slug: run-tests-dynamically
Authors: Jitse-Jan
Summary: In this project I want to verify the availability of the APIs that we use to ingest data into our data platform. In the example I will use Jira, Workable and HiBob, since they offer clean APIs without too much configuration. First I will create a test suite to verify the availability and once this works move it to a Lambda function that could be scheduled with CloudWatch on a fixed schedule.

In this project I want to verify the availability of the APIs that we use to ingest data into our data platform. In the example I will use Jira, Workable and HiBob since they offer clean APIs without too much configuration. First I will create a test suite to verify the availability and once this works move it to a Lambda function that could be scheduled with CloudWatch on a fixed schedule.

## Prerequisites

Make sure the following environment variables are set. Change it to the correct profile and region for the AWS account you want to run the tests for. The profile should be available in `~/.aws/credentials`.

- `AWS_PROFILE=prod`
- `AWS_DEFAULT_REGION=eu-west-1`
- `ENV=prod`

## Testing

One of the main reasons I switched from `unittest` to `pytest` is the ease of use of *fixtures*. You can define the functions or variables that you will need throughout the whole test set. 

### Fixture class

In this case I define a `FixtureClass` that contains a function to retrieve the parameters from AWS *SSM*, a key-value store where we store our API keys and other secrets. Note that in the following function I only retrieve the parameters for the base path `/`. The class has a Boto3 `session` and `ssm_client`.

```python
class FixtureClass:
    """ Defines the FixtureClass """

    def get_ssm_parameters(self):
        """ Returns the SSM parameters """
        paginator = self.ssm_client.get_paginator("get_parameters_by_path")
        iterator = paginator.paginate(Path="/", WithDecryption=True)
        params = {}
        for page in iterator:
            for param in page.get("Parameters", []):
                params[param.get("Name")] = param.get("Value")
        return params
    
    @property
    def session(self):
        return boto3.session.Session()
    
    @property
    def ssm_client(self):
        return self.session.client("ssm")
```

### Set the fixture

Now I can create an instance of the FixtureClass and add the `ssm_parameters` as fixture for my tests. Define them either on `conftest.py` next to your test files, or add them on top of the file where you will write the tests.

```Python
fc = FixtureClass()

@pytest.fixture(scope="session")
def ssm_parameters():
    return fc.get_ssm_parameters()
```

### Add fixture to test class

In order to make the fixture available for all the tests I add the fixture as attribute to the test class. By using `autouse=True` the fixtures become available in the `setup_class` method. This method is only called once per execution of the tests.

```python
""" testsourceavailability.py """
class TestSourceAvailability:
    """ Defines the tests to verify the source availability """

    @pytest.fixture(autouse=True)
    def setup_class(self, ssm_parameters):
        """ Setup the test class """
        self.ssm_parameters = ssm_parameters
        self.session = requests.Session()

    def _get_param(self, key):
        return self.ssm_parameters.get(key)

```

### Create the tests

Below I have defined five different tests to validate the availability of three different sources. Three of the tests are to verify the availability (good weather) and two of them ensure that the API does not work with the wrong parameters (bad weather).

- HiBob (tool used by HR)
- Jira (tool used by Tech)
- Workable (tool used by Recruiting)

Every tests consists of the following steps:

1. Retrieve the parameters from SSM
2. Set the arguments for the API call
3. Assert the status code of the API call

```python
# Append to previous TestSourceAvailability file.
		def test_hibob_is_available(self):
        """ Test that the HiBob API is available """
        api_key = self._get_param("HIBOB_API_KEY")
        api_url = self._get_param("HIBOB_API_URL")

        kwargs = {
            'method': 'get',
            'url': api_url,
            'headers': {
                "Authorization": api_key
            }
        }
        assert self.session.request(**kwargs).status_code == 200

    def test_jira_is_available(self):
        """ Test that the Jira API is available """
        api_key = self._get_param("JIRA_API_KEY")
        api_url = self._get_param("JIRA_URL")
        jira_user = self._get_param("JIRA_USER")

        kwargs = {
            'method': 'get',
            'url': f"{api_url}/rest/api/2/project",
            'auth': (jira_user, api_key)
        }
        assert self.session.request(**kwargs).status_code == 200

    def test_jira_is_unavailable_without_api_key(self):
        """ Test that the Jira API is unavailable without API key """
        api_key = None
        api_url = self._get_param("JIRA_URL")
        jira_user = self._get_param("JIRA_USER")

        kwargs = {
            'method': 'get',
            'url': f"{api_url}/rest/api/2/project",
            'auth': (jira_user, "")
        }
        assert self.session.request(**kwargs).status_code == 401

    def test_workable_api_is_available(self):
        """ Test that the Workable API is available """
        api_key = self._get_param("WORKABLE_API_KEY")
        api_url = self._get_param("WORKABLE_API_URL")

        kwargs = {
            'method': 'get',
            'url': f"{api_url}jobs",
            'headers': {"Authorization": "Bearer {}".format(api_key)},
            'params': {"limit": 1, "include_fields": "description"}
        }
        assert self.session.request(**kwargs).status_code == 200

    def test_workable_api_is_not_available_for_wrong_credentials(self):
        """ Test that the Workable API is not available for wrong credentials """
        api_key = "fake_key"
        api_url = self._get_param("WORKABLE_API_URL")

        kwargs = {
            'method': 'get',
            'url': f"{api_url}jobs",
            'headers': {"Authorization": "Bearer {}".format(api_key)},
            'params': {"limit": 1, "include_fields": "description"}
        }
        assert self.session.request(**kwargs).status_code == 401
```

### Execution of the tests

Make sure`pytest` is installed on your machine. Run the file we've created before and add verbosity if you wish. Note that I use Python 3.7 and pytest 5.3.1. In my case all tests are green, so we can continue!

```bash
$ pytest testsourceavailability.py -v
============================= test session starts ==============================
platform darwin -- Python 3.7.4, pytest-5.3.1, py-1.8.0, pluggy-0.13.1 -- /Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7
cachedir: .pytest_cache
rootdir: /Users/jitsejan/Documents
collected 5 items

testsourceavailability.py::TestSourceAvailability::test_hibob_is_available PASSED [ 20%]
testsourceavailability.py::TestSourceAvailability::test_jira_is_available PASSED [ 40%]
testsourceavailability.py::TestSourceAvailability::test_jira_is_unavailable_without_api_key PASSED [ 60%]
testsourceavailability.py::TestSourceAvailability::test_workable_api_is_available PASSED [ 80%]
testsourceavailability.py::TestSourceAvailability::test_workable_api_is_not_available_for_wrong_credentials PASSED [100%]
```

## Lambda function

Because I do not only want to verify availability at the test stage, I will create a Lambda function that I can schedule to periodically check that the APIs are still available. 

### AvailabilityChecker class

The class is initialized with the `ssm_client` to access the parameters stored in SSM and again the `requests.Session` that is used to call the API. The function to get the parameter by key has the same name, but the underlying logic is of course different compared to the one I used in the tests before with a fixture. By keeping the function name the same it is slightly easier to copy the tests to this Lambda function.

```python
""" availabilitychecker.py """
class AvailabilityChecker:

    def __init__(self):
        self.ssm_client = boto3.client("ssm")
        self.session = requests.Session()

    def _get_param(self, key):
        """ Return the SSM parameter """
        return self.ssm_client.get_parameter(Name=key, WithDecryption=True)["Parameter"]["Value"]
```

#### Verify functions

I will only add the good weather tests from the previous test set, hence I will verify HiBob, Jira and Workable, but I don't check for the negative cases.

```python
# continue availabilitychecker.py
		def verify_hibob_is_available(self):
        """ Verify that the HiBob API is available """
        api_key = self._get_param("HIBOB_API_KEY")
        api_url = self._get_param("HIBOB_API_URL")

        arguments = {
            'method': 'get',
            'url': api_url,
            'headers': {
                "Authorization": api_key
            }
        }
        return self.session.request(**arguments).status_code == 200

    def verify_jira_is_available(self):
        """ Verify that the Jira API is available """
        api_key = self._get_param("JIRA_API_KEY")
        api_url = self._get_param("JIRA_URL")
        jira_user = self._get_param("JIRA_USER")

        arguments = {
            'method': 'get',
            'url': f"{api_url}/rest/api/2/project",
            'auth': (jira_user, api_key)
        }
        return self.session.request(**arguments).status_code == 200

    def verify_workable_api_is_available(self):
        """ Verify that the Workable API is available """
        api_key = self._get_param("WORKABLE_API_KEY")
        api_url = self._get_param("WORKABLE_API_URL")

        arguments = {
            'method': 'get',
            'url': f"{api_url}jobs",
            'headers': {
                "Authorization": "Bearer {}".format(api_key)
            },
            'params': {
                "limit": 1,
                "include_fields": "description"
            }
        }
        return self.session.request(**arguments).status_code == 200
```

#### Retrieve verify methods automatically

Because in reality this file is way larger since I need to test way more sources, I do not want to write out all the verify functions explicitly in my Lambda function like below.

```python
def lambda_handler(event, context):
  	avc = AvailabilityChecker()
    avc.verify_hibob_is_available()
    avc.verify_jira_is_available()
    avc.verify_workable_is_available()
```

Instead, I want to dynamically retrieve these functions by iterating through the methods of the class.

```python
def _get_verify_functions(self):
		""" Return verify functions inside this class """
    return [func for func in dir(self) if callable(getattr(self, func)) and func.startswith("verify")]
```

This method will loop through the callable functions, check if it starts with `verify` and return a list of functions. 

#### Final Lambda

I have updated the `lambda_handler` to retrieve the functions, iterate through them and execute the method to validate for the different sources if the API is available. Of course this code is a bit longer, but when I add more `verify` functions to the class, I do not have to change any other code!

```python
def lambda_handler(event, context):
    avc = AvailabilityChecker()
    for method in avc._get_verify_functions():
        is_available = getattr(avc, method)()
        source = ' '.join(method.split('_')[1:-2]).title()
        if not is_available:
            print(f"[NOK] Please check availability for `{source}`.")            
        else:
            print(f"[OK] `{source}`")
```

Running it will give the results for the three sources.

```bash
$ python availabilitychecker.py
[OK] `Hibob`
[OK] `Jira`
[OK] `Workable Api`
```

Check the [Gist](https://gist.github.com/jitsejan/c12a076f3950c0e1be4b55831d291f91) for the final code. Hope it helps :) 

