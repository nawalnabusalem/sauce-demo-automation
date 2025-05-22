import logging

import pytest

from pages.login.login_page import LoginPage
from pages.main_page.main_page import MainPage
from utils.test_utils.TestHelper import TestHelper
from logger.logger import CustomLogger


class BaseTest:
    @classmethod
    def setup_class(cls) -> None:
        cls.logger = CustomLogger(name=f'{cls.__name__}')
        cls.test_helper = TestHelper(logger=cls.logger)

        cls.is_class_header_printed: bool = False

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, browser, request):
        self.logger.setup_handlers(
            report_path=f'reports/{self.__class__.__name__}/{request.config.getoption("--browser")}',
            level=self._get_console_level(request=request)
        )

        if not self.is_class_header_printed:
            self.logger.print_class_header(class_name=self.__class__.__name__)
            self.__class__.is_class_header_printed = True

        timeout: int = self._get_timeout(request=request)
        self.login_page = LoginPage(driver=browser, logger=self.logger, timeout=timeout)
        self.main_page = MainPage(driver=browser, logger=self.logger, timeout=timeout)

        self.logger.print_test_header(test_name=request.node.name)

        yield

        self.logger.log_test_result(item=request.node)
        self.logger.print_test_footer(item=request.node)

    @classmethod
    def teardown_class(cls):

        cls.logger.print_final_summary()

    def _get_console_level(self, request) -> int:
        console_level: str = request.config.getoption("--console-log-level")

        if console_level == "debug":
            return logging.DEBUG

        if console_level == "info":
            return logging.INFO

        if console_level == "warning":
            return logging.WARNING

        if console_level == "error":
            return logging.ERROR

        raise ValueError(f"Unsupported log level: {console_level}, available browsers are debug, info, warning, error")

    def _get_timeout(self, request) -> int:
        timeout_str: str = request.config.getoption("--timeout")

        if not timeout_str.isdigit():
            raise ValueError(f"Invalid timeout format: {timeout_str}, should be integer")


        return int(timeout_str)

