import pytest


@pytest.mark.parametrize("a, expected", [
    ([1, 2, 3], "2.00"),
    ([1, 2, 3, 4], "2.50"),
    ([5, 5, 5, 5], "5.00"),
    ([1, 2, 1, 2], "1.50")
])
def test_average(a, expected):
    from mainprogram import average
    answer = average(a)
    assert answer == expected
