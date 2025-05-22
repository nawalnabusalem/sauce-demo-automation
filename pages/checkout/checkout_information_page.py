from typing import Tuple

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from logger.logger import CustomLogger


class CheckoutInformationPage(BasePage):
    def __init__(self, driver: webdriver,logger:CustomLogger, timeout: int = 10) -> None:
        super().__init__(driver=driver,logger=logger, timeout=timeout)

        self._first_name_edittext: Tuple[str:str] = (By.ID, 'first-name')
        self._last_name_edittext: Tuple[str:str] = (By.ID, 'last-name')
        self._postal_code_edittext: Tuple[str:str] = (By.ID, 'postal-code')
        self._continue_button_locator: Tuple[str:str] = (By.ID, 'continue')
        self._cancel_button_locator: Tuple[str:str] = (By.ID, 'cancel')
        self._error_message_textfield_locator: Tuple[str:str] = (By.CSS_SELECTOR, '#checkout_info_container > div > form > div.checkout_info > div.error-message-container.error > h3')

    def make_checkout(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.logger.debug(msg=f"Make a checkout, first name: {first_name}, last name: {last_name}, postal code: {postal_code}")

        self.clear_and_set_text(locator=self._first_name_edittext, text=first_name)
        self.clear_and_set_text(locator=self._last_name_edittext, text=last_name)
        self.clear_and_set_text(locator=self._postal_code_edittext, text=postal_code)

        self.click(locator=self._continue_button_locator)

    def get_error_message(self) -> str:
        self.logger.debug(msg=f"Get the checkout error message")

        return self.get_text(locator=self._error_message_textfield_locator)

    def back_to_cart_page(self) -> None:
        self.logger.debug(msg=f"Click the cancel button to return back to cart page")

        self.click(locator=self._cancel_button_locator)
