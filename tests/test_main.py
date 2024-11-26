import ast
import os

import pytest

from app.main import create_person_list
from app.main import Person


def path_to_main():
    base_path = os.path.join("app", "main.py")
    return (
        base_path if os.path.exists(base_path) else os.path.join(os.pardir, base_path)
    )


@pytest.fixture()
def people_data():
    return [
        {"name": "Ross", "age": 30, "wife": "Rachel"},
        {"name": "Joey", "age": 29, "wife": None},
        {"name": "Phoebe", "age": 31, "husband": None},
        {"name": "Chandler", "age": 30, "wife": "Monica"},
        {"name": "Monica", "age": 32, "husband": "Chandler"},
        {"name": "Rachel", "age": 28, "husband": "Ross"},
    ]


@pytest.fixture()
def created_person_list(people_data):
    return create_person_list(people_data)


def test_person_class_attribute_people_exists():
    assert hasattr(
        Person, "people"
    ), "Class Person should have class attribute 'people'"
    assert (
        len(Person.people) == 0
    ), "Initial length of 'Person.people' should equal to 0"


@pytest.mark.parametrize("name,age", [("Ross", 30), ("Joey", 29)])
def test_person_class_name_age(name, age):
    person_inst = Person(name, age)
    assert person_inst.name == name, "Person instance should have attribute 'name'"
    assert person_inst.age == age, "Person instance should have attribute 'age'"


def test_create_person_list_all_persons(people_data, created_person_list):
    assert all(isinstance(person, Person) for person in created_person_list), (
        "All elements in result of 'create_person_list' should be instance "
        "of Person class"
    )
    assert len(created_person_list) == len(
        people_data
    ), "Length of initial list should equal to length of function result"


def test_create_person_list_order(people_data, created_person_list):
    assert [person_dict["name"] for person_dict in people_data] == [
        person.name for person in created_person_list
    ], "Order in function result should be the same"


def test_create_person_list_has_no_wife(people_data, created_person_list):
    assert not hasattr(created_person_list[1], "wife"), (
        f"Person with 'name' {created_person_list[1].name} should not have "
        f"attribute 'wife'"
    )


def test_create_person_list_has_wife_and_wife_have_husband(
    people_data, created_person_list
):
    ross = created_person_list[0]  # Ross
    assert (
        hasattr(ross, "wife")
        and ross.wife.name == "Rachel"
        and ross.wife.husband == ross
    ), (
        f"Person with 'name' {ross.name} should have "
        f"attribute 'wife' with name 'Rachel' and "
        f"Ross's wife should point back to Ross"
    )


def test_person_instance_attribute_wife_and_husband_doesnt_exist():
    with open(path_to_main(), encoding="utf-8") as file:
        tree = ast.parse(file.read())

    assert (
        len(
            tree.__dict__["body"][0]
            .__dict__["body"][1]
            .__dict__["args"]
            .__dict__["args"]
        )
        == 3
    ), "'__init__' should takes only two arguments 'name' and 'age'!"


def test_removed_comment():
    with open(path_to_main(), "r", encoding="utf-8") as file:
        main_content = file.read()

        assert (
            "# write your code here" not in main_content
        ), "You have to remove the unnecessary comment '# write your code here'"


def test_double_quotes_instead_of_single():
    with open(path_to_main(), "r", encoding="utf-8") as file:
        main_content = file.read()

        assert (
            "'" not in main_content
        ), "You have to use double quotes \"\" instead of single ''"