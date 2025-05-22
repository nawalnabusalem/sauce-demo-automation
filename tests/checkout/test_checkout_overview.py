from typing import List

import pytest

from pages.checkout.checkout_overview_page import CheckoutItem
from pages.inventory.inventory_page import Product
from tests.base_test import BaseTest
from tests.checkout.test_checkout_information import CheckoutStatus


class TestCheckoutInformation(BaseTest):

    @pytest.mark.parametrize("cart_count, first_name, last_name, postal_code, expected_result", [
        (3, 'Nour', 'Ali', 'K1A', CheckoutStatus.VALID_CHECKOUT)
    ])
    def test_checkout_overview(
            self,
            cart_count: int,
            first_name: str,
            last_name: str,
            postal_code: str,
            expected_result: CheckoutStatus
    ) -> None:
        self._login_and_get_main_page()

        added_product_names_list: List[str] = self._add_products_to_the_cart(cart_count=cart_count)

        self.logger.info(msg=f"open the cart page")
        self.main_page.click_cart_button()

        self.logger.info(msg=f"open the checkout information page")
        self.main_page.cart_page.click_checkout_button()

        self.logger.info(msg=f"Complete the checkout process with information - first name: {first_name}, last name: {last_name}, postal code: {postal_code}")
        self.main_page.checkout_information_page.make_checkout(first_name=first_name, last_name=last_name, postal_code=postal_code)

        self.logger.info(msg="Verify successful submitting checkout information")

        self.test_helper.assert_and_log(
            condition=self.main_page.checkout_overview_page.is_checkout_information_page_opened(),
            error_msg="Failed to submit checkout information",
            soft=True
        )

        self._verify_checkout_items(expected_added_items_names_list=added_product_names_list)
        self._verify_subtotal_price()
        self._verify_total_price()
        self._from_checkout_overview_cleanup_added_items()

        self.test_helper.raise_soft_failures()

        self.logger.info(msg="Verify the checkout Overview is passed")

    def _login_and_get_main_page(self) -> None:
        self.logger.info(msg="Attempt login with credentials - User: secret_sauce")
        self.login_page.load()
        self.login_page.login(username="standard_user", password="secret_sauce")

        self.test_helper.assert_and_log(
            condition=self.main_page.is_user_logged_in(),
            error_msg="Login failed (expected success login)"
        )

        self.logger.info(msg="Login successful - proceeding with main page")

    def _add_products_to_the_cart(self, cart_count: int) -> List[str]:
        self.logger.info(msg=f"Add the first {cart_count} product to the cart")
        product_list: List[Product] = self.main_page.inventory_page.get_all_products()
        added_products_name: List[str] = []

        self.test_helper.assert_and_log(
            condition=len(product_list) >= cart_count,
            error_msg=f"Too few products in inventory. Available: {len(product_list)}, Required: {cart_count}"
        )

        for index in range(cart_count):
            self.test_helper.assert_and_log(
                condition=product_list[index].add_to_cart_button is not None,
                error_msg=f"The product {product_list[index].product_name} is already added to the cart"
            )

            self.logger.info(msg=f"Add the product {product_list[index].product_name} to the cart")
            product_list[index].add_product_to_cart()
            added_products_name.append(product_list[index].product_name)

        return added_products_name

    def _from_checkout_overview_cleanup_added_items(self):
        self.logger.info(msg="Return back to the inventory and clean up the added items")
        self.main_page.checkout_overview_page.click_cancel_button()
        self.main_page.side_menu.reset_app_state()

    def _verify_checkout_items(self, expected_added_items_names_list: List[str]) -> None:
        self.logger.info(msg="Verify if all of the added items are in the checkout list")

        checkout_items_name_list: List[str] = self.main_page.checkout_overview_page.get_all_items_name()

        self.test_helper.assert_and_log(condition=len(checkout_items_name_list) > 0, error_msg="There is no items added to the checkout list")
        self.test_helper.assert_equal_and_log(
            actual=len(checkout_items_name_list),
            expected=len(expected_added_items_names_list),
            error_msg="The checkout list count is not equal to the added items count",
            soft=True

        )

        for product_name in expected_added_items_names_list:
            self.logger.info(msg=f"Verify if the product {product_name} in the checkout list")

            self.test_helper.assert_in_list(item=product_name, items_list=checkout_items_name_list, item_name="Added item", soft=True)

    def _verify_subtotal_price(self) -> None:
        self.logger.info(msg="Verify the subtotal price")

        checkout_items_list: List[CheckoutItem] = self.main_page.checkout_overview_page.get_all_checkout_items()
        actual_subtotal_price: float = self.main_page.checkout_overview_page.get_subtotal_price()
        expected_subtotal_price: float = 0

        for item in checkout_items_list:
            expected_subtotal_price += item.item_price

        self.test_helper.assert_equal_and_log(
            actual=actual_subtotal_price,
            expected=expected_subtotal_price,
            error_msg="The actual subtotal price is not equal to the expected subtotal price",
            soft=True
        )

    def _verify_total_price(self) -> None:
        self.logger.info(msg="Verify the total price")

        checkout_items_list: List[CheckoutItem] = self.main_page.checkout_overview_page.get_all_checkout_items()
        actual_total_price: float = self.main_page.checkout_overview_page.get_total_price_with_tax()
        expected_total_price: float = self.main_page.checkout_overview_page.get_tax_amount()

        for item in checkout_items_list:
            expected_total_price += item.item_price

        self.test_helper.assert_equal_and_log(
            actual=actual_total_price,
            expected=expected_total_price,
            error_msg="The actual total price is not equal to the expected total price",
            soft=True
        )
