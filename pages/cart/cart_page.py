from typing import Tuple, List, Optional

from selenium.common import TimeoutException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from logger.logger import CustomLogger


class CartItem:
    def __init__(self,
                 logger: CustomLogger,
                 driver: webdriver,
                 timeout: int,
                 item_name: str,
                 item_description: str,
                 item_price: float,
                 remove_button: WebElement = None
                 ) -> None:
        self.logger: CustomLogger = logger
        self.driver: webdriver = driver
        self.timeout: int = timeout
        self.item_name: str = item_name
        self.item_description: str = item_description
        self.item_price: float = item_price
        self.remove_button: WebElement = remove_button

    def remove_product_from_cart(self) -> None:
        self.logger.debug(msg=f"Remove the product with name {self.item_name} from the cart")

        try:
            WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(self.remove_button)).click()

        except Exception as e:
            self.logger.error(msg=f"Failed to remove the product with name {self.item_name} from the cart deu error:\n{e}")

            assert False, f"Failed to remove the product with name {self.item_name} from the cart"


class CartPage(BasePage):
    def __init__(self, driver: webdriver, logger: CustomLogger, timeout: int = 10) -> None:
        super().__init__(driver=driver, logger=logger, timeout=timeout)

        self._cart_item_locator: Tuple[str, str] = (By.CLASS_NAME, 'cart_item')
        self._item_name_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item_name')
        self._item_description_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item_desc')
        self._item_price_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item_price')
        self._remove_button_locator: Tuple[str, str] = (By.CSS_SELECTOR, '.btn.btn_secondary.btn_small.cart_button')

        self._continue_shopping_button_locator: Tuple[str, str] = (By.ID, 'continue-shopping')
        self._checkout_button_locator: Tuple[str, str] = (By.ID, 'checkout')

    def get_all_cart_items(self) -> List[CartItem]:
        self.logger.debug(msg=f"Get all cart items containers with locator: {self._cart_item_locator}")

        cart_items_list: List[CartItem] = []

        try:
            items: List[WebElement] = self.wait.until(method= EC.presence_of_all_elements_located(self._cart_item_locator))

            for item in items:
                cart_item: CartItem = self._parse_item(item)

                if cart_item:
                    cart_items_list.append(cart_item)

        except TimeoutException:
            self.logger.debug('Empty cart list')

            return  cart_items_list

        except Exception as e:
            self.logger.error(msg=f'Failed to load the cart items list due to Exception: \n{e}')

            assert False, f"Failed to load the cart items list"

        return cart_items_list

    def _parse_item(self, item: WebElement) -> Optional[CartItem]:
        self.logger.debug(msg=f"Parse the cart item object from the item element with name= {item.find_element(*self._item_name_locator).text}")

        try:
            return CartItem(
                logger=self.logger,
                driver=self.driver,
                timeout=self.timeout,
                item_name=item.find_element(*self._item_name_locator).text,
                item_description=item.find_element(*self._item_description_locator).text,
                item_price=float(item.find_element(*self._item_price_locator).text.strip("$")),
                remove_button=item.find_element(*self._remove_button_locator)
            )

        except Exception as e:
            self.logger.error(msg=f"Failed to parse the cart item due to the error: \n{e}")

            assert False, f"Failed to parse the cart item"

    def get_all_items_name(self) -> List[str]:
        self.logger.debug(msg="Get all cart items name")

        names_list: List[str] = []

        for cart_item in self.get_all_cart_items():
            names_list.append(cart_item.item_name)

        return names_list

    def click_continue_shopping_button(self) -> None:
        self.logger.debug(msg=f"Click continue shopping button")
        self.click(locator=self._continue_shopping_button_locator)

    def click_checkout_button(self) -> None:
        self.logger.debug(msg=f"Click checkout button")
        self.click(locator=self._checkout_button_locator)

