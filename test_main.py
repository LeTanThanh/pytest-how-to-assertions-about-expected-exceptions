import pytest


def zero_division():
    return 1 / 0


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        zero_division()


def recursion_depth():
    recursion_depth()


def test_recursion_depth():
    with pytest.raises(RuntimeError) as exc_info:
        recursion_depth()

    assert "maximum recursion" in str(exc_info.value)


def not_implemented():
    raise NotImplementedError


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc_info:
        not_implemented()

    assert exc_info.type is NotImplementedError


def value():
    raise ValueError("Expection 123 raised")


def test_value():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        value()


def exception_group():
    raise ExceptionGroup(
        "Group message",
        [
            RuntimeError("Exception 123 raised.")
        ]
    )


def test_exception_group():
    with pytest.raises(ExceptionGroup) as exc_info:
        exception_group()

    assert exc_info.group_contains(RuntimeError, match=r".* 123 .*")
    assert not exc_info.group_contains(TypeError)


def exception_group_at_given_depth():
    raise ExceptionGroup(
        "Group message",
        [
            RuntimeError(),
            ExceptionGroup(
                "Nested group",
                [
                    TypeError()
                ]
            )
        ]
    )


def test_exception_group_at_given_depth():
    with pytest.raises(ExceptionGroup) as exc_info:
        exception_group_at_given_depth()

    assert exc_info.group_contains(RuntimeError, depth=1)
    assert not exc_info.group_contains(TypeError, depth=1)

    assert exc_info.group_contains(TypeError, depth=2)
    assert not exc_info.group_contains(RuntimeError, depth=2)
