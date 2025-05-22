from typing import Tuple

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logger.logger import CustomLogger


class BasePage:
    def __init__(self, driver: webdriver, logger: CustomLogger, timeout: int = 10):
        self.driver: webdriver = driver
        self.logger: CustomLogger = logger
        self.timeout: int = timeout
        self.wait: WebDriverWait = WebDriverWait(self.driver, timeout)

    def click(self, locator: Tuple[str, str]) -> None:
        self.logger.debug(msg=f"Click the element with locator: {locator}")

        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()

        except Exception as e:
            self.logger.error(msg=f"Failed to click the element with locator: {locator} due to error:\n{e}")

            assert False, f"Failed to click the element with locator: {locator}"



    def set_text(self, locator: Tuple[str, str], text: str) -> None:
        self.logger.debug(msg=f"Enter text {text} to the element locator: {locator}")

        try:
            self.wait.until(EC.visibility_of_element_located(locator)).send_keys(text)

        except Exception as e:
            self.logger.error(msg=f"Failed to send the text to the element with locator: {locator} due to error:\n{e}")

            assert False, f"Failed to send the text to the element with locator: {locator}"

    def clear(self, locator: Tuple[str, str]) -> None:
        self.logger.debug(f"Clear the content of the element with locator: {locator}")

        try:
            self.wait.until(EC.visibility_of_element_located(locator)).clear()

        except Exception as e:
            self.logger.error(msg=f"Failed to clear the text to the element with locator: {locator} due to error:\n{e}")

            assert False, f"Failed to clear the text to the element with locator: {locator}"

    def clear_and_set_text(self, locator: Tuple[str, str], text: str) -> None:
       self.clear(locator=locator)
       self.set_text(locator=locator, text=text)

    def get_text(self, locator: Tuple[str, str]) -> str:
        self.logger.debug(msg=f"Get the text of the element with locator: {locator}")

        try:
             return self.wait.until(EC.visibility_of_element_located(locator)).text

        except Exception as e:
            self.logger.error(msg=f"Failed to get the text of the element with locator: {locator} due to error:\n{e}")

            assert False, f"Failed to get the text of the element with locator: {locator}"

    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        self.logger.debug(msg=f"check the visibility of the element with locator: {locator}")

        try:
           self.wait.until(EC.visibility_of_element_located(locator))
           return True

        except TimeoutException :
            return False
