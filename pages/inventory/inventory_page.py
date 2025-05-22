from enum import Enum
from typing import Tuple, List, Optional

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from logger.logger import CustomLogger


class Product:
    def __init__(self,
                 logger: CustomLogger,
                 driver: webdriver,
                 timeout: int,
                 product_image: str,
                 product_name: str,
                 product_description: str,
                 product_price: float,
                 add_to_cart_button: WebElement = None,
                 remove_from_cart_button: WebElement = None
                 ) -> None:
        self.logger: CustomLogger = logger
        self.driver: webdriver = driver
        self.timeout: int = timeout
        self.product_image: str = product_image
        self.product_name: str = product_name
        self.product_description: str = product_description
        self.product_price: float = product_price
        self.add_to_cart_button: Optional[WebElement] = add_to_cart_button
        self.remove_from_cart_button: Optional[WebElement] = remove_from_cart_button

    def add_product_to_cart(self) -> None:
        self.logger.debug(msg=f"Add the product with name {self.product_name} to the cart")

        try:
            add_to_cart_button: WebElement = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(self.add_to_cart_button))
            self.driver.execute_script("arguments[0].click();", add_to_cart_button)

        except Exception as e:
            self.logger.error(msg=f"Failed to add the product with name {self.product_name} to the cart deu error:\n{e}")

            assert False, f'Failed to add the product with name {self.product_name} to the cart'

    def remove_product_from_cart(self) -> None:
        self.logger.debug(msg=f"Remove the product with name {self.product_name} from the cart")

        try:
            remove_from_cart_button: WebElement = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.remove_from_cart_button))
            self.driver.execute_script("arguments[0].click();", remove_from_cart_button)
        except Exception as e:
            self.logger.error(msg=f"Failed to remove the product with name {self.product_name} from the cart deu error:\n{e}")

            assert False, f'Failed to remove the product with name {self.product_name} from the cart'

class SortOption(Enum):
    NAME_A_Z = 'az'
    NAME_Z_A = 'za'
    PRICE_LOW_HIGH = 'lohi'
    PRICE_HIGH_LOW = 'hilo'

class InventoryPages(BasePage):
    def __init__(self, driver: webdriver, logger: CustomLogger, timeout: int = 10) -> None:
        super().__init__(driver=driver, logger=logger, timeout=timeout)

        self._inventory_item_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item')
        self._product_name_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item_name')
        self._product_image_locator: Tuple[str, str] = (By.CSS_SELECTOR, ".inventory_item_img img")
        self._product_description_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item_desc')
        self._product_price_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item_price')
        self._add_to_cart_button_locator: Tuple[str, str] = (By.CSS_SELECTOR, '.btn.btn_primary.btn_small.btn_inventory')
        self._remove_from_cart_button_locator: Tuple[str, str] = (By.CSS_SELECTOR, '.btn.btn_secondary.btn_small.btn_inventory')

        self._product_sort_selector: Tuple[str, str] = (By.CLASS_NAME, 'product_sort_container')

    def get_all_products(self) -> List[Product]:
        self.logger.debug(msg=f"Get all products containers from inventory section with locator: {self._inventory_item_locator}")

        products_list: List[Product] = []

        try:
            items: List[WebElement] = self.wait.until(method= EC.presence_of_all_elements_located(self._inventory_item_locator))

            for item in items:
                product: Product = self._parse_product(item)

                if product:
                    products_list.append(product)

        except Exception as e:
            self.logger.error(msg=f'Failed to load the products list due to Exception: \n{e}')

            assert False, f"Failed to load the products list"

        return products_list

    def _parse_product(self, item: WebElement) -> Optional[Product]:
        self.logger.debug(msg=f"Parse the product object from the product element with name= {item.find_element(*self._product_name_locator).text}")

        try:
            return Product(
                logger=self.logger,
                driver=self.driver,
                timeout=self.timeout,
                product_image=self._get_product_image_url(item=item),
                product_name=item.find_element(*self._product_name_locator).text,
                product_description=item.find_element(*self._product_description_locator).text,
                product_price=float(item.find_element(*self._product_price_locator).text.strip("$")),
                add_to_cart_button= self._get_cart_button(item=item, locator=self._add_to_cart_button_locator),
                remove_from_cart_button=self._get_cart_button(item=item, locator=self._remove_from_cart_button_locator),
            )

        except Exception as e:
            self.logger.error(msg=f"Failed to parse the product item due to the error: \n{e}")

            assert False, f"Failed to parse the product item"

    def choice_product_selector_option(self, sort_option: SortOption) -> None:
        self.logger.debug(msg=f"Choice the option {sort_option} from dropdown with locator: {self._product_sort_selector}")

        sort_dropdown: Select = Select(self.wait.until(EC.visibility_of_element_located(self._product_sort_selector)))
        sort_dropdown.select_by_value(value=sort_option.value)

    def _get_product_image_url(self, item: WebElement) -> str:
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of(item))

            return item.find_element(*self._product_image_locator).get_attribute('src') or ""

        except Exception as e:
            self.logger.error(msg=f"Failed to get the image url for the item-id= {item.id} due to the error: \n{e}")

            assert False, f"Failed to get the product image"


    def _get_cart_button(self, item, locator) -> Optional[WebElement]:
        try:
            return item.find_element(*locator)

        except Exception:
            return None
