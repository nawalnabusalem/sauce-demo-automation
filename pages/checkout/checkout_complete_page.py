from typing import Tuple

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from logger.logger import CustomLogger


class CheckoutCompletePage(BasePage):
    def __init__(self, driver: webdriver, logger: CustomLogger, timeout: int = 10) -> None:
        super().__init__(driver=driver, logger=logger, timeout=timeout)

        self._home_button_locator: Tuple[str, str] = (By.ID, 'back-to-products')
        self._completion_message_locator: Tuple[str, str] = (By.CLASS_NAME, 'complete-header')


    def click_home_button(self) -> None:
        self.logger.debug(msg=f"Click home button and return back to the inventory page")

        self.click(self._home_button_locator)


    def is_the_checkout_completed(self) -> bool:
        self.logger.debug(msg=f"Verify if the thankful message is displayed")

        return 'Thank you for your order!' in self.get_text(locator=self._completion_message_locator)


