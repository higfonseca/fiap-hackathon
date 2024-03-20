from typing import Any

from testfixtures import compare


def assert_exception_body(expected_exception: Exception, received_exception_context: Any) -> None:  # type:ignore[misc]
    compare(str(expected_exception), str(received_exception_context.exception))
