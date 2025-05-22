import re
from typing import Tuple, List, Optional

from selenium.common import TimeoutException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from logger.logger import CustomLogger


class CheckoutItem:
    def __init__(self, item_name: str, item_description: str, item_price: float) -> None:
        self.item_name: str = item_name
        self.item_description: str = item_description
        self.item_price: float = item_price


class CheckoutOverviewPage(BasePage):
    def __init__(self, driver: webdriver, logger: CustomLogger, timeout: int = 10) -> None:
        super().__init__(driver=driver, logger=logger, timeout=timeout)

        self._cart_item_locator: Tuple[str, str] = (By.CLASS_NAME, 'cart_item')
        self._item_name_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item_name')
        self._item_description_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item_desc')
        self._item_price_locator: Tuple[str, str] = (By.CLASS_NAME, 'inventory_item_price')

        self._finish_button_locator: Tuple[str, str] = (By.ID, 'finish')
        self._cancel_button_locator: Tuple[str, str] = (By.ID, 'cancel')

        self._checkout_title_locator: Tuple[str, str] = (By.CLASS_NAME, 'title')
        self._items_subtotal_price_locator: Tuple[str, str] = (By.CLASS_NAME, 'summary_subtotal_label')
        self._tax_price_locator: Tuple[str, str] = (By.CLASS_NAME, 'summary_tax_label')
        self._items_total_price_locator: Tuple[str, str] = (By.CLASS_NAME, 'summary_total_label')

    def get_all_checkout_items(self) -> List[CheckoutItem]:
        self.logger.debug(msg=f"Get all checkout items containers with locator: {self._cart_item_locator}")

        checkout_items_list: List[CheckoutItem] = []

        try:
            items: List[WebElement] = self.wait.until(method= EC.presence_of_all_elements_located(self._cart_item_locator))

            for item in items:
                checkout_item: CheckoutItem = self._parse_item(item)

                if checkout_item:
                    checkout_items_list.append(checkout_item)

        except TimeoutException:
            self.logger.debug('Empty checkout list')

            return  checkout_items_list

        except Exception as e:
            self.logger.error(msg=f'Failed to load the checkout items list due to Exception: \n{e}')

            assert False, f"Failed to load the checkout items list"

        return checkout_items_list

    def _parse_item(self, item: WebElement) -> Optional[CheckoutItem]:
        self.logger.debug(msg=f"Parse the checkout item object from the item element with name= {item.find_element(*self._item_name_locator).text}")

        try:
            return CheckoutItem(
                item_name=item.find_element(*self._item_name_locator).text,
                item_description=item.find_element(*self._item_description_locator).text,
                item_price=float(item.find_element(*self._item_price_locator).text.strip("$"))
            )

        except Exception as e:
            self.logger.error(msg=f"Failed to parse the cart item due to the error: \n{e}")

            assert False, f"Failed to parse the cart item"

    def get_all_items_name(self) -> List[str]:
        self.logger.debug(msg="Get all checkout items name")

        names_list: List[str] = []

        for cart_item in self.get_all_checkout_items():
            names_list.append(cart_item.item_name)

        return names_list

    def is_checkout_information_page_opened(self) -> bool:
        return 'Checkout: Overview' in self.get_text(locator=self._checkout_title_locator).strip()

    def click_finish_button(self) -> None:
        self.logger.debug(msg=f"Click finish button to confirm the checkout")

        self.click(locator=self._finish_button_locator)

    def click_cancel_button(self) -> None:
        self.logger.debug(msg=f"Click cancel button to cancel the checkout")

        self.click(locator=self._cancel_button_locator)

    def get_subtotal_price(self) -> float:
        self.logger.debug(msg=f"Get the subtotal price of the items without tax")

        return float(re.search(pattern=r'\d+(\.\d+)?', string= self.get_text(locator=self._items_subtotal_price_locator)).group())

    def get_tax_amount(self) -> float:
        self.logger.debug(msg=f"Get the tax amount of the checkout items")

        return float(re.search(pattern=r'\d+(\.\d+)?', string=self.get_text(locator=self._tax_price_locator)).group())

    def get_total_price_with_tax(self) -> float:
        self.logger.debug(msg=f"Get the total price of the items with tax amount")

        return float(re.search(pattern=r'\d+(\.\d+)?', string=self.get_text(locator=self._items_total_price_locator)).group())