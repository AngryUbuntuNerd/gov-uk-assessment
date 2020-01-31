import pytest

from api.models import Coordinate, User


def test_coordinate_init_throws_exception():
    with pytest.raises(ValueError):
        Coordinate("hi", "there")


def test_coordinate_bool_returns_false_if_incomplete():
    coordinate = Coordinate(10, None)
    assert not coordinate


def test_coordinate_bool_returns_true_if_complete():
    coordinate = Coordinate(10, 10)
    assert coordinate


def test_coordinate_is_valid_returns_false_if_incomplete_or_invalid():
    coordinate = Coordinate(10, None)
    assert not coordinate.is_valid()

    coordinate = Coordinate(100, 90)
    assert not coordinate.is_valid()

    coordinate = Coordinate(50, 200)
    assert not coordinate.is_valid()


def test_coordinate_is_valid_returns_true_if_complete_and_valid():
    coordinate = Coordinate(10, 20)
    assert coordinate.is_valid()


def test_coordinate_to_tuple_works():
    coordinate = Coordinate(10, 20)
    assert coordinate.to_tuple() == (10, 20)


def test_user_is_in_range_returns_false_if_invalid():
    user = User(id=1)
    coordinate = Coordinate(10, None)
    assert not user.is_in_range(coordinate, 10)


def test_user_is_in_range_returns_false_if_not_in_range():
    user = User(id=1, latitude=10, longitude=10)
    coordinate = Coordinate(0, 0)
    assert not user.is_in_range(coordinate, 100)


def test_user_is_in_range_returns_true_if_in_range():
    user = User(id=1, latitude=1, longitude=1)
    coordinate = Coordinate(0, 0)
    assert user.is_in_range(coordinate, 100)


def test_user_hash_uses_id():
    user = User(id=1)
    assert hash(user) == hash(1)


def test_user_equals_not_other_class():
    user = User(id=1)
    coordinate = Coordinate(1, 1)
    assert not user == coordinate


def test_user_equals_other_user_with_same_id():
    user1 = User(id=1)
    user2 = User(id=1)
    assert user1 == user2