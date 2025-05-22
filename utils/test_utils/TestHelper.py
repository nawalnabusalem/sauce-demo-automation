from enum import Enum
from typing import Any, List, Type, Callable, Optional


from logger.logger import CustomLogger


class TestHelper:
    def __init__(self, logger: CustomLogger) -> None:
        self.logger: CustomLogger = logger

        self.soft_failures:List[str] = []

    def assert_and_log(self, condition: bool, error_msg: str, pre_failure_hook: Optional[Callable[[], None]] = None, soft: bool = False) -> None:
        if not condition:
            self.logger.error(error_msg)

            if soft:
                self.soft_failures.append(error_msg)

            else:
                if pre_failure_hook:
                    pre_failure_hook()

                assert False, error_msg

    def assert_equal_and_log(
            self,
            actual: Any,
            expected: Any,
            error_msg: str,
            pre_failure_hook: Optional[Callable[[], None]] = None,
            soft: bool = False
    ) -> None:
        if actual != expected:
            self.logger.error(f"{error_msg} Expected: {expected}, Actual: {actual}")

            if soft:
                self.soft_failures.append("Values do not match")

            else:
                if pre_failure_hook:
                    pre_failure_hook()

                assert False, error_msg or "Values do not match"

    def assert_in_list(
            self,
            item: Any,
            items_list: List[Any],
            item_name: str = "Item",
            pre_failure_hook: Optional[Callable[[], None]] = None,
            soft: bool = False
    ) -> None:
        self.assert_and_log(
            condition=item in items_list,
            error_msg=f"{item_name} '{item}' was not found in the list.",
            pre_failure_hook=pre_failure_hook,
            soft=soft
        )

    def assert_equal_list(
            self,
            expected_list: List[Any],
            actual_list: List[Any],
            error_msg: str,
            pre_failure_hook: Optional[Callable[[], None]] = None,
            soft: bool = False
    ) -> None:
        if sorted(actual_list) != sorted(expected_list):
            self.logger.error(f"{error_msg} Expected: {expected_list}, Actual: {actual_list}")

            if soft:
                self.soft_failures.append("Lists do not match")

            else:
                if pre_failure_hook:
                    pre_failure_hook()

                assert False, error_msg or "Lists do not match"


    def validate_positive_integer(self, value: int, field_name: str = "Value", soft: bool = False) -> None:
        self.assert_and_log(condition=value > 0, error_msg=f"{field_name} must be greater than 0", soft=soft)

    def verify_error_message(
            self,
            actual_message: str,
            expected_error: Enum,
            allowed_enum: Type[Enum],
            pre_failure_hook: Optional[Callable[[], None]] = None,
            soft: bool = False
    ) -> None:
        allowed_errors = [e.value for e in allowed_enum]

        if expected_error.value not in actual_message:
            self.logger.error(
                f"ERROR MESSAGE VALIDATION FAILED\n"
                f"Expected: {expected_error.value}\n"
                f"Actual: {actual_message}\n"
                f"Allowed errors: {allowed_errors}"
            )
            if soft:
                self.soft_failures.append(f"{expected_error.value} not in {actual_message}")

            else:
                if pre_failure_hook:
                    pre_failure_hook()

                assert False, f"{expected_error.value} not in {actual_message}"

        else:
            self.logger.info(f"Error message validation passed: {expected_error.value}")

    def raise_soft_failures(self) -> None:
        if self.soft_failures:
            full_error = "\n".join(self.soft_failures)
            self.soft_failures = []
            raise AssertionError(f"Soft Assertion Failures:\n{full_error}")