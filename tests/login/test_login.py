from enum import Enum

import pytest


from tests.base_test import BaseTest


class LoginStatus(Enum):
    VALID_LOGIN = 'valid-login'
    INVALID_CREDENTIALS = 'Epic sadface: Username and password do not match any user in this service'
    LOCKED_USER = 'Epic sadface: Sorry, this user has been locked out.'
    MISSING_USERNAME = 'Epic sadface: Username is required'
    MISSING_PASSWORD = 'Epic sadface: Password is required'


class TestLogin(BaseTest):

    @pytest.mark.parametrize("username,password,expected_result", [
        ("standard_user", "any_pass", LoginStatus.INVALID_CREDENTIALS),
        ("locked_out_user", "secret_sauce", LoginStatus.LOCKED_USER),
        ("", "", LoginStatus.MISSING_USERNAME),
        ("standard_user", "", LoginStatus.MISSING_PASSWORD),
        ("standard_user", "secret_sauce", LoginStatus.VALID_LOGIN),
    ])
    def test_login_page(self,
                        username: str,
                        password: str,
                        expected_result: LoginStatus) -> None:

        self.login_page.load()

        self.logger.info(f"Attempt login with credentials - User: {username}")
        self.login_page.login(username=username, password=password)

        if expected_result == LoginStatus.VALID_LOGIN:
            self.logger.info("Verify successful login")

            self.test_helper.assert_and_log(condition=self.main_page.is_user_logged_in(), error_msg="Login failed when it should success as expected")

            self.logger.info("Login successful - proceeding with logout")
            self.main_page.side_menu.logout()

        else:
            self.logger.info("Verify failed login as expected")

            self.test_helper.assert_and_log(condition=not self.main_page.is_user_logged_in(), error_msg="Login succeeded when it should fail as expected")

            self.test_helper.verify_error_message(
                actual_message=self.login_page.get_error_message().strip(),
                expected_error=expected_result,
                allowed_enum=LoginStatus
            )

