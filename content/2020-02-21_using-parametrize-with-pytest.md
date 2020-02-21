Title: Using parametrize with PyTest
Date: 2020-02-21 15:54
Modified: 2020-02-21 15:54
Category: posts
Tags: Python, pytest, testing, parametrize
Slug: using-parametrize-with-pytest
Authors: Jitse-Jan
Summary: Using [parametrize](https://docs.pytest.org/en/latest/parametrize.html) writing tests becomes significantly easier. Instead of writing a test for each combination of parameters I can write one test with a list of different sets of parameters. A short example..

## Recap

In my previous post I showed the function to test the access to the `castle` based on the `powerup` of the `character`. It takes a test for the case that the character `has_access` and a test to verify the character does not have access without the Super Mushroom. Both the `castle` and `character` are set as a *fixture* in the `conftest.py`. 


*Snippet - Fixtures for castle and character*

```Python
import pytest
...

@pytest.fixture(scope="class")
def castle():
    return Castle(CASTLE_NAME)

@pytest.fixture(scope="class")
def character():
    return Character(CHARACTER_NAME)

...
```

*Snippet - Tests to validate access to castle.*

```Python
...

class TestCastleClass:
    """ Defines the tests for the Castle class """
    
    ...
    
    def test_has_access_true_with_super_mushroom(self, castle, character):
				""" Test that has_access returns True for Super Mushroom """
				character.powerup = 'Super Mushroom'
				assert castle.has_access(character)

    def test_has_access_false_without_super_mushroom(self, castle, character):
				""" Test that has_access returns False for other powerups """
			  character.powerup = 'Not a mushroom'
				assert not castle.has_access(character)
        
    ...
```

Running this in the console looks like this:

```bash
$ pytest -k has_access -v
============================================================ test session starts =============================================================
platform darwin -- Python 3.7.3, pytest-5.2.1, py-1.8.0, pluggy-0.13.0 -- /Users/jitsejan/.local/share/virtualenvs/blog-testing-KMgUXSdn/bin/python3.7m
cachedir: .pytest_cache
rootdir: /Users/jitsejan/code/blog-testing
plugins: mock-1.11.1
collected 17 items / 15 deselected / 2 selected

tests/test_castle_class.py::TestCastleClass::test_has_access_true_with_super_mushroom PASSED                                           [ 50%]
tests/test_castle_class.py::TestCastleClass::test_has_access_false_without_super_mushroom PASSED                                       [100%]
```

## Introducing parametrize

Using [parametrize](https://docs.pytest.org/en/latest/parametrize.html) writing tests becomes significantly easier. Instead of writing a test for each combination of parameters I can write one test with a list of different sets of parameters. For each set of parameters the same test case will be executed, hence the two test cases above can be replaced by:

```python
		@pytest.mark.parametrize('powerup,has_access', [
        ("Super Mushroom", True),
        ("Not a mushroom", False),
    ], ids=['successful', 'failure-without-super-mushroom'])
    def test_has_access_true_with_super_mushroom(self, castle, character, powerup, has_access):
        """ Test that has_access returns True for Super Mushroom """
        character.powerup = powerup
        assert castle.has_access(character) == has_access
```

Running the same selection of tests again still returns two results but now it is indicated by the ID provided as argument for the `parametrize`.

```bash
$ pytest -k has_access -v
============================================================ test session starts =============================================================
platform darwin -- Python 3.7.3, pytest-5.2.1, py-1.8.0, pluggy-0.13.0 -- /Users/jitsejan/.local/share/virtualenvs/blog-testing-KMgUXSdn/bin/python3.7m
cachedir: .pytest_cache
rootdir: /Users/jitsejan/code/blog-testing
plugins: mock-1.11.1
collected 17 items / 15 deselected / 2 selected

tests/test_castle_class.py::TestCastleClass::test_has_access_true_with_super_mushroom[successful] PASSED                               [ 50%]
tests/test_castle_class.py::TestCastleClass::test_has_access_true_with_super_mushroom[failure-without-super-mushroom] PASSED           [100%]
```

The other test cases in the [repo](https://github.com/jitsejan/blog-testing) don't lend themselves to be used for parametrization, but it has helped me to reduce the number of test cases in our data platform repo by half. Give it a try :) 