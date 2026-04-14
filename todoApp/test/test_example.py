import pytest

def test_equal_or_not_equal():
    assert 3 == 3

def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("this is a number", int)

def test_boolean():
    validated = True
    assert validated is True
    assert ("hello" == "world") is False

def test_type():
    assert type("hello" is str)
    assert type("world" is not int)

def test_greater_and_less_than():
    assert 7 >3
    assert 10 > 5

def test_list():
    num_list = [2,4,6,7,8]
    any_list = [False, False]
    assert 2 in num_list
    assert 7 in num_list
    assert all (num_list)
    assert not any (any_list)


class Student:
    def __init__(self, first_name: str, last_name: str, major:str, years: int):
        self.first_name = first_name
        self .last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student('Labanya', 'roy', 'cse', 4)


def test_person_initialization(default_employee):
    # p = Student('Labanya', 'roy', 'cse', 4)
    assert default_employee.first_name == 'Labanya', 'First name should be Labanya'
    assert default_employee.last_name =='roy', 'last name should be roy'
    assert default_employee.major == 'cse', 'major should be cse'
    assert default_employee.years == 4
