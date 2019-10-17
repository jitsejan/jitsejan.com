Title: Moving from `unittest` to `pytest`
Date: 2019-10-17 17:00
Modified: 2019-10-17 17:00
Category: posts
Tags: Python, testing, unittest, pytest, mock
Slug: moving-from-unittest-to-pytest
Authors: Jitse-Jan
Summary: In my two previous articles [Unittesting in a Jupyter notebook](https://www.jitsejan.com/unittesting-in-jupyter-notebook.html) and [Mocking in unittests in Python](https://www.jitsejan.com/mocking-in-unittests-in-python.html) I have discussed the use of `unittest` and `mock` to run tests for a simple `Castle` and `Character` class. For the code behind this article please check [Github](https://github.com/jitsejan/blog-testing).

In my two previous articles [Unittesting in a Jupyter notebook](https://www.jitsejan.com/unittesting-in-jupyter-notebook.html) and [Mocking in unittests in Python](https://www.jitsejan.com/mocking-in-unittests-in-python.html) I have discussed the use of `unittest` and `mock` to run tests for a simple `Castle` and `Character` class. For the code behind this article please check [Github](https://github.com/jitsejan/blog-testing).

## The classes

Let's recap the classes first. 

### Castle class

The Castle class has a name, boss and world property and a simple method to determine if a character has access bases on his powerup. Note that the classes have been cleaned up since the last article.

```python
""" jj_classes/castle.py """


class Castle(object):
    """ Defines the Castle class """

    def __init__(self, name):
        """ Initialize the class """
        self._name = name
        self._boss = "Bowser"
        self._world = "Grass Land"

    def has_access(self, character):
        """ Check if character has access """
        return character.powerup == "Super Mushroom"

    def get_boss(self):
        """ Returns the boss """
        return self.boss

    def get_world(self):
        """ Returns the world """
        return self.world

    @property
    def name(self):
        """ Name of the castle """
        return self._name

    @property
    def boss(self):
        """ Boss of the castle """
        return self._boss

    @property
    def world(self):
        """ World of the castle """
        return self._world

```

### Character class

```python
""" jj_classes/character.py """


class Character(object):
    """ Defines the character class """

    def __init__(self, name):
        """ Initialize the class """
        self._name = name
        self._powerup = ""

    def get_powerup(self):
        """ Returns the powerup """
        return self.powerup

    @property
    def name(self):
        """ Name of the character """
        return self._name

    @property
    def powerup(self):
        """ Powerup of the character """
        return self._powerup

    @powerup.setter
    def powerup(self, powerup):
        """ Sets the powerup """
        self._powerup = powerup

```



## Unittests

In the previous articles, I've written two tests sets, one for Character and one for Character and Castle. Looking back at the tests now, I noticed that the Character/Castle testset is not very tidy so at the end I will simply have a set to test the `Character` class and one to test the `Castle` class.

```python
""" tests/charactertestclass.py """

import unittest
import unittest.mock as mock

try:
    from jj_classes.castle import Castle
except ModuleNotFoundError:
    import sys, os

    sys.path.insert(0, f"{os.path.dirname(os.path.abspath(__file__))}/../")
    from jj_classes.castle import Castle
from jj_classes.character import Character


class CharacterTestClass(unittest.TestCase):
    """ Defines the tests for the Character class """

    def setUp(self):
        """ Set the castle for the test cases """
        self.castle = Castle("Bowsers Castle")

    def test_mock_access_denied(self):
        """ Access denied for star powerup """
        mock_character = mock.Mock(powerup="Starman")
        self.assertFalse(self.castle.has_access(mock_character))

    def test_mock_access_granted(self):
        """ Access granted for mushroom powerup """
        mock_character = mock.Mock(powerup="Super Mushroom")
        self.assertTrue(self.castle.has_access(mock_character))

    def test_default_castle_boss(self):
        """ Verifty the default boss is Bowser """
        self.assertEqual(self.castle.get_boss(), "Bowser")

    def test_default_castle_world(self):
        """ Verify the default world is Grass Land """
        self.assertEqual(self.castle.get_world(), "Grass Land")

    # Mock a class method
    @mock.patch.object(Castle, "get_boss")
    def test_mock_castle_boss(self, mock_get_boss):
        mock_get_boss.return_value = "Hammer Bro"
        self.assertEqual(self.castle.get_boss(), "Hammer Bro")
        self.assertEqual(self.castle.get_world(), "Grass Land")

    # Mock an instance
    @mock.patch(__name__ + ".Castle")
    def test_mock_castle(self, MockCastle):
        instance = MockCastle
        instance.get_boss.return_value = "Toad"
        instance.get_world.return_value = "Desert Land"
        self.castle = Castle
        self.assertEqual(self.castle.get_boss(), "Toad")
        self.assertEqual(self.castle.get_world(), "Desert Land")

    # Mock an instance method
    def test_mock_castle_instance_method(self):
        # Boss is still Bowser
        self.assertNotEqual(self.castle.get_boss(), "Koopa Troopa")
        # Set a return_value for the get_boss method
        self.castle.get_boss = mock.Mock(return_value="Koopa Troopa")
        # Boss is Koopa Troopa now
        self.assertEqual(self.castle.get_boss(), "Koopa Troopa")

    def test_castle_with_more_bosses(self):
        multi_boss_castle = mock.Mock()
        # Set a list as side_effect for the get_boss method
        multi_boss_castle.get_boss.side_effect = ["Goomba", "Boo"]
        # First value is Goomba
        self.assertEqual(multi_boss_castle.get_boss(), "Goomba")
        # Second value is Boo
        self.assertEqual(multi_boss_castle.get_boss(), "Boo")
        # Third value does not exist and raises a StopIteration
        self.assertRaises(StopIteration, multi_boss_castle.get_boss)

    def test_calls_to_castle(self):
        self.castle.has_access = mock.Mock()
        self.castle.has_access.return_value = "No access"
        # We should retrieve no access for everybody
        self.assertEqual(self.castle.has_access("Let me in"), "No access")
        self.assertEqual(self.castle.has_access("Let me in, please"), "No access")
        self.assertEqual(self.castle.has_access("Let me in, please sir!"), "No access")
        # Verify the length of the arguments list
        self.assertEqual(len(self.castle.has_access.call_args_list), 3)


if __name__ == "__main__":
    unittest.main()

```

```python
""" tests/charactercastletestclass.py """

import unittest
import unittest.mock as mock

try:
    from jj_classes.castle import Castle
except ModuleNotFoundError:
    import sys, os

    sys.path.insert(0, f"{os.path.dirname(os.path.abspath(__file__))}/../")
    from jj_classes.castle import Castle
from jj_classes.character import Character


class CharacterCastleTestClass(unittest.TestCase):
    """ Defines the tests for the Character and Castle class together """

    @mock.patch(__name__ + ".Castle")
    @mock.patch(__name__ + ".Character")
    def test_mock_castle_and_character(self, MockCharacter, MockCastle):
        # Note the order of the arguments of this test
        MockCastle.name = "Mocked Castle"
        MockCharacter.name = "Mocked Character"
        self.assertEqual(Castle.name, "Mocked Castle")
        self.assertEqual(Character.name, "Mocked Character")

    def test_fake_powerup(self):
        character = Character("Sentinel Character")
        character.powerup = mock.Mock()
        character.powerup.return_value = mock.sentinel.fake_superpower
        self.assertEqual(character.powerup(), mock.sentinel.fake_superpower)

    def test_castle_with_more_powerups(self):
        self.castle = Castle("Beautiful Castle")
        multi_characters = mock.Mock()
        # Set a list as side_effect for the get_boss method
        multi_characters.get_powerup.side_effect = ["mushroom", "star"]
        # First value is mushroom
        self.assertEqual(multi_characters.get_powerup(), "mushroom")
        # Second value is star
        self.assertEqual(multi_characters.get_powerup(), "star")
        # Third value does not exist and raises a StopIteration
        self.assertRaises(StopIteration, multi_characters.get_powerup)


if __name__ == "__main__":
    unittest.main()

```

## Rewriting the tests to use `pytest`

In order to increase readability and reduce repetition, I favor `pytest` over `unittest`. PyTest offers some nice features to make writing tests faster and cleaner. 

### Main differences

#### Assert

With `unittest` we always use `self.assertEqual` and the other variations. With `pytest` only `assert` is used.

```python
# unittest
self.assertEqual(5, "five")
```

```python
# pytest
assert 5 == five
```

Capturing errors is easier with PyTest, you can even assert the raised message in the same go.

```python
# unittest
self.assertRaises(StopIteration, multi_boss_castle.get_boss)
```

```python
# pytest
with pytest.raises(StopIteration):
		multi_boss_castle.get_boss()
    
expected_error = r"__init__\(\) missing 1 required positional argument: \'name\'"
with pytest.raises(TypeError, match=expected_error):
		castle = Castle()
```

#### Mock

```python
# unittest
# Mock a class method
@mock.patch.object(Castle, "get_boss")
def test_mock_castle_boss(self, mock_get_boss):
  	mock_get_boss.return_value = "Hammer Bro"
  	self.assertEqual(self.castle.get_boss(), "Hammer Bro")
```

Make sure that for the mock functionality in PyTest the package `pytest-mock` is installed.

```python
# pytest
# Mock a class method
def test_mock_castle_boss(self, mocker, castle):
  	mock_get_boss = mocker.patch.object(Castle, "get_boss")
  	mock_get_boss.return_value = "Hammer Bro"
  	assert castle.get_boss(), "Hammer Bro"
```

#### Fixtures

PyTest has the functionality to add fixtures to your tests. They are normally placed in `conftest.py` in your tests folder where it will be automatically be picked up. For the sake of example, I have added the fixture to the same file as the test itself. In case of defining `castle` in each test like for `unittest`, we create a fixture for `castle` once and add it as an argument to the tests.

```python
# unittest

def test_get_boss_returns_bowser(self):
    """ Test that the get_boss returns Bowser """
    castle = Castle("My Fixture Castle")
    assert castle.get_boss() == 'Bowser'
    
def test_get_world_returns_grass_land(self):
    """ Test that the get_boss returns Grass Land """
    castle = Castle("My Fixture Castle")
    assert castle.get_world() == 'Grass Land'
```



```python
# pytest
@pytest.fixture(scope='session')
def castle():
    returns Castle("My Fixture Castle")

def test_get_boss_returns_bowser(self, castle):
    """ Test that the get_boss returns Bowser """
    assert castle.get_boss() == 'Bowser'
    
def test_get_world_returns_grass_land(self, castle):
    """ Test that the get_boss returns Grass Land """
    assert castle.get_world() == 'Grass Land'
```



## Conclusion

In the end I have cleaned up my tests to only use `pytest` and I have introduced the fixture file `conftest.py` to reduce the complexity of the test files.

```python
""" tests/conftest.py """
import pytest

CASTLE_NAME = "Castle Name"
CHARACTER_NAME = "Character Name"

from jj_classes.castle import Castle
from jj_classes.character import Character

@pytest.fixture(scope="class")
def castle():
    return Castle(CASTLE_NAME)

@pytest.fixture(scope="class")
def character():
    return Character(CHARACTER_NAME)
```

And the tests look like the following:

```python
""" tests/test_castle_class.py """
import pytest
from jj_classes.castle import Castle

class TestCastleClass:
    """ Defines the tests for the Castle class """

    def test_init_sets_name(self):
        """ Test that init sets the name """
        castle = Castle('Test name')
        assert castle.name == "Test name"

    def test_init_error_when_no_name(self):
        """ Test that init fails without the name """
        expected_error = r"__init__\(\) missing 1 required positional argument: \'name\'"
        with pytest.raises(TypeError, match=expected_error):
            castle = Castle()

    def test_has_access_true_with_super_mushroom(self, castle, character):
        """ Test that has_access returns True for Super Mushroom """
        character.powerup = 'Super Mushroom'
        assert castle.has_access(character)

    def test_has_access_false_without_super_mushroom(self, castle, character):
        """ Test that has_access returns False for other powerups """
        character.powerup = 'Not a mushroom'
        assert castle.has_access(character) is False
    
    def test_get_boss_returns_bowser(self, castle):
        """ Test that the get_boss returns Bowser """
        assert castle.get_boss() == 'Bowser'

    def test_get_world_returns_grass_land(self, castle):
        """ Test that the get_boss returns Grass Land """
        assert castle.get_world() == 'Grass Land'

    # Mock a class method
    def test_mock_castle_boss(self, mocker, castle):
        """ Test that the mocked get_boss returns overwritten value """
        mock_get_boss = mocker.patch.object(Castle, "get_boss")
        mock_get_boss.return_value = "Hammer Bro"
        assert castle.get_boss(), "Hammer Bro"

    # Mock an instance
    def test_mock_castle(self, mocker):
        """ Test that the mocked instance returns overwritten values """
        instance = mocker.patch(__name__ + ".Castle")
        instance.get_boss.return_value = "Toad"
        instance.get_world.return_value = "Desert Land"
        castle = Castle
        assert castle.get_boss() == "Toad"
        assert castle.get_world() == "Desert Land"

    # Mock an instance method
    def test_mock_castle_instance_method(self, mocker, castle):
        """ Test that overwriting the instance method worked """
        assert castle.get_boss() != "Koopa Troopa"
        castle.get_boss = mocker.Mock(return_value="Koopa Troopa")
        assert castle.get_boss() == "Koopa Troopa"

    def test_castle_with_more_bosses(self, mocker):
        """ Test that get_boss gets overwritten several times """
        multi_boss_castle = mocker.Mock()
        multi_boss_castle.get_boss.side_effect = ["Goomba", "Boo"]
        assert multi_boss_castle.get_boss() == "Goomba"
        assert multi_boss_castle.get_boss() == "Boo"
        with pytest.raises(StopIteration):
            multi_boss_castle.get_boss()

    def test_calls_to_castle(self, mocker, castle):
        """ Test that has_access gets called 3 times """
        castle.has_access = mocker.Mock()
        castle.has_access.return_value = "No access"
        assert castle.has_access("Let me in") == "No access"
        assert castle.has_access("Let me in, please") == "No access"
        assert castle.has_access("Let me in, please sir!") == "No access"
        assert len(castle.has_access.call_args_list) == 3

```



```python
""" tests/test_character_class.py """
import pytest
from jj_classes.character import Character

class TestCharacterClass:
    """ Defines the tests for the Character class """

    def test_init_sets_name(self):
        """ Test that init sets the name """
        character = Character('Test name')
        assert character.name == "Test name"

    def test_init_error_when_no_name(self):
        """ Test that init fails without the name """
        expected_error = r"__init__\(\) missing 1 required positional argument: \'name\'"
        with pytest.raises(TypeError, match=expected_error):
            character = Character()

    def test_get_powerup_returns_correct_value_when_not_set(self, character):
        """ Test that the get_powerup returns the right value when not set """
        assert character.get_powerup() == ""

    def test_get_powerup_returns_correct_value_when_set(self, character):
        """ Test that the get_powerup returns the right value when set """
        character.powerup = "Fire Flower"
        assert character.get_powerup() == "Fire Flower"

    def test_fake_powerup(self, mocker, character):
        """ Test that the powerup can be mocked """
        character.powerup = mocker.Mock()
        character.powerup.return_value = mocker.sentinel.fake_superpower
        assert character.powerup() == mocker.sentinel.fake_superpower

    def test_characters_with_more_powerups(self, mocker, castle):
        """ Test that get_powerup gets overwritten several times """
        multi_characters = mocker.Mock()
        multi_characters.get_powerup.side_effect = ["mushroom", "star"]
        assert multi_characters.get_powerup() == "mushroom"
        assert multi_characters.get_powerup() == "star"
        with pytest.raises(StopIteration):
            multi_characters.get_powerup()

```



```bash
$ pytest -v
================================================================================================= test session starts ==================================================================================================
platform darwin -- Python 3.7.3, pytest-5.2.1, py-1.8.0, pluggy-0.13.0 -- /Users/jitsejan/.local/share/virtualenvs/blog-testing-KMgUXSdn/bin/python3.7m
cachedir: .pytest_cache
rootdir: /Users/jitsejan/code/blog-testing
plugins: mock-1.11.1
collected 17 items                                                                                                                                                                                                     

tests/test_castle_class.py::TestCastleClass::test_init_sets_name PASSED                                                                                                                                          [  5%]
tests/test_castle_class.py::TestCastleClass::test_init_error_when_no_name PASSED                                                                                                                                 [ 11%]
tests/test_castle_class.py::TestCastleClass::test_has_access_true_with_super_mushroom PASSED                                                                                                                     [ 17%]
tests/test_castle_class.py::TestCastleClass::test_has_access_false_without_super_mushroom PASSED                                                                                                                 [ 23%]
tests/test_castle_class.py::TestCastleClass::test_get_boss_returns_bowser PASSED                                                                                                                                 [ 29%]
tests/test_castle_class.py::TestCastleClass::test_get_world_returns_grass_land PASSED                                                                                                                            [ 35%]
tests/test_castle_class.py::TestCastleClass::test_mock_castle_boss PASSED                                                                                                                                        [ 41%]
tests/test_castle_class.py::TestCastleClass::test_mock_castle PASSED                                                                                                                                             [ 47%]
tests/test_castle_class.py::TestCastleClass::test_mock_castle_instance_method PASSED                                                                                                                             [ 52%]
tests/test_castle_class.py::TestCastleClass::test_castle_with_more_bosses PASSED                                                                                                                                 [ 58%]
tests/test_castle_class.py::TestCastleClass::test_calls_to_castle PASSED                                                                                                                                         [ 64%]
tests/test_character_class.py::TestCharacterClass::test_init_sets_name PASSED                                                                                                                                    [ 70%]
tests/test_character_class.py::TestCharacterClass::test_init_error_when_no_name PASSED                                                                                                                           [ 76%]
tests/test_character_class.py::TestCharacterClass::test_get_powerup_returns_correct_value_when_not_set PASSED                                                                                                    [ 82%]
tests/test_character_class.py::TestCharacterClass::test_get_powerup_returns_correct_value_when_set PASSED                                                                                                        [ 88%]
tests/test_character_class.py::TestCharacterClass::test_fake_powerup PASSED                                                                                                                                      [ 94%]
tests/test_character_class.py::TestCharacterClass::test_characters_with_more_powerups PASSED                                                                                                                     [100%]

================================================================================================== 17 passed in 0.10s ==================================================================================================
```

