from typing import Tuple

from selenium.common import TimeoutException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.cart.cart_page import CartPage
from pages.checkout.checkout_complete_page import CheckoutCompletePage
from pages.checkout.checkout_information_page import CheckoutInformationPage
from pages.checkout.checkout_overview_page import CheckoutOverviewPage
from pages.inventory.inventory_page import InventoryPages
from pages.main_page.side_menu import SideMenu
from logger.logger import CustomLogger


class MainPage(BasePage):
    def __init__(self, driver: webdriver, logger: CustomLogger, timeout: int = 10) -> None:
        super().__init__(driver=driver, logger=logger, timeout=timeout)

        self.side_menu: SideMenu = SideMenu(driver=driver, logger=logger, timeout=timeout)
        self.inventory_page: InventoryPages = InventoryPages(driver=driver, logger=logger, timeout=timeout)
        self.cart_page: CartPage = CartPage(driver=driver, logger=logger, timeout=timeout)
        self.checkout_information_page: CheckoutInformationPage = CheckoutInformationPage(driver=driver, logger=logger, timeout=timeout)
        self.checkout_overview_page: CheckoutOverviewPage = CheckoutOverviewPage(driver=driver, logger=logger, timeout=timeout)
        self.checkout_complete_page: CheckoutCompletePage = CheckoutCompletePage(driver=driver, logger=logger, timeout=timeout)

        self._cart_button: Tuple[str, str] = (By.CLASS_NAME, 'shopping_cart_link')
        self._cart_badge: Tuple[str, str] = (By.CLASS_NAME, 'shopping_cart_badge')


    def is_user_logged_in(self) -> bool:
        self.logger.debug(msg="Check if the user is logged in")

        return self.is_element_visible(locator=self._cart_button)

    def click_cart_button(self) -> None:
        self.logger.debug(msg="Click the cart button")
        self.click(self._cart_button)

    def get_cart_count(self) -> int:
        self.logger.debug(msg="Get cart badge count")
        cart_count: int = 0

        try:
            cart_badge = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(self._cart_badge))
            cart_count = int(cart_badge.text)

        except TimeoutException:
            self.logger.warning(msg="The Cart badge will not be displayed when the cart count is zero.")

        except Exception as e:
            self.logger.error(msg=f"Failed to get the cart badge with locator {self._cart_badge} due to the error: \n{e}")

        return cart_count
