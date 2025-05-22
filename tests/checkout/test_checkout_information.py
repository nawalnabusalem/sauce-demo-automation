from enum import Enum
from typing import List

import pytest

from pages.inventory.inventory_page import Product
from tests.base_test import BaseTest


class CheckoutStatus(Enum):
    VALID_CHECKOUT = 'valid checkout'
    MISSING_FIRST_NAME = 'Error: First Name is required'
    MISSING_LAST_NAME = 'Error: Last Name is required'
    MISSING_POSTAL_CODE = 'Error: Postal Code is required'

class TestCheckoutInformation(BaseTest):

    @pytest.mark.parametrize("cart_count, first_name, last_name, postal_code, expected_result", [
        (3, '', 'Ali', 'K1A', CheckoutStatus.MISSING_FIRST_NAME),
        (3, 'Nour', '', 'K1A', CheckoutStatus.MISSING_LAST_NAME),
        (3, 'Nour', 'Ali', '', CheckoutStatus.MISSING_POSTAL_CODE),
        (3, 'Nour', 'Ali', 'K1A', CheckoutStatus.VALID_CHECKOUT),
    ])
    def test_checkout_information(
            self,
            cart_count: int,
            first_name: str,
            last_name: str,
            postal_code: str,
            expected_result: CheckoutStatus
    ) -> None:
        self._login_and_get_main_page()

        self._add_products_to_the_cart(cart_count=cart_count)

        self.logger.info(msg=f"open the cart page")
        self.main_page.click_cart_button()

        self.logger.info(msg=f"open the checkout information page")
        self.main_page.cart_page.click_checkout_button()

        self.logger.info(msg=f"Complete the checkout process with information - first name: {first_name}, last name: {last_name}, postal code: {postal_code}")
        self.main_page.checkout_information_page.make_checkout(first_name=first_name, last_name=last_name, postal_code=postal_code)

        if expected_result == CheckoutStatus.VALID_CHECKOUT:
            self.logger.info(msg="Verify successful submitting checkout information")

            self.test_helper.assert_and_log(
                condition=self.main_page.checkout_overview_page.is_checkout_information_page_opened(),
                error_msg="Failed to submit checkout information"
            )

            self._from_checkout_overview_cleanup_added_items()

        else:
            self.logger.info(msg="Verify failed checkout as expected and Verify error message matches expected")
            actual_message: str = self.main_page.checkout_information_page.get_error_message().strip()

            self.test_helper.verify_error_message(
                actual_message=actual_message,
                expected_error=expected_result,
                allowed_enum=CheckoutStatus,
                pre_failure_hook=self._from_checkout_information_cleanup_added_items
            )

            self._from_checkout_information_cleanup_added_items()

        self.logger.info(msg="Filling the checkout information is passed")

    def _login_and_get_main_page(self) -> None:
        self.logger.info(msg="Attempt login with credentials - User: secret_sauce")
        self.login_page.load()
        self.login_page.login(username="standard_user", password="secret_sauce")

        self.test_helper.assert_and_log(
            condition=self.main_page.is_user_logged_in(),
            error_msg="Login failed (expected success login)"
        )

        self.logger.info(msg="Login successful - proceeding with main page")

    def _add_products_to_the_cart(self, cart_count: int) -> None:
        self.test_helper.validate_positive_integer(value=cart_count, field_name="cart_count")

        self.logger.info(msg=f"Add the first {cart_count} product to the cart")

        product_list: List[Product] = self.main_page.inventory_page.get_all_products()

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

    def _from_checkout_information_cleanup_added_items(self):
        self.logger.info(msg="Return back to the inventory and clean up the added items")
        self.main_page.checkout_information_page.back_to_cart_page()
        self.main_page.cart_page.click_continue_shopping_button()
        self.main_page.side_menu.reset_app_state()

    def _from_checkout_overview_cleanup_added_items(self):
        self.logger.info(msg="Return back to the inventory and clean up the added items")
        self.main_page.checkout_overview_page.click_cancel_button()
        self.main_page.side_menu.reset_app_state()
