from typing import Tuple

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from logger.logger import CustomLogger


class LoginPage(BasePage):
    def __init__(self, driver: webdriver,logger:CustomLogger, timeout: int = 10) -> None:
        super().__init__(driver=driver,logger=logger, timeout=timeout)

        self._username_edittext: Tuple[str:str] = (By.ID, 'user-name')
        self._password_edittext: Tuple[str:str] = (By.ID, 'password')
        self._login_button: Tuple[str:str] = (By.ID, 'login-button')
        self._error_message_textfield: Tuple[str:str] = (By.CSS_SELECTOR, '#login_button_container > div > form > div.error-message-container.error > h3')

    def load(self) -> None:
        self.logger.debug(msg=f"Load the login page")

        self.driver.get('https://www.saucedemo.com/')

    def login(self, username: str,password: str) -> None:
        self.logger.debug(msg=f"Login with username: {username}")

        self.clear_and_set_text(locator=self._username_edittext, text=username)
        self.clear_and_set_text(locator=self._password_edittext, text=password)
        self.click(locator=self._login_button)

    def get_error_message(self) -> str:
        self.logger.debug(msg=f"Get the login error message")

        return self.get_text(locator=self._error_message_textfield)
