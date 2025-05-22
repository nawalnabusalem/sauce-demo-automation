from typing import List

import pytest

from pages.inventory.inventory_page import Product, SortOption
from tests.base_test import BaseTest


class TestMainInventory(BaseTest):

    @pytest.mark.parametrize("sort_option", [
        SortOption.NAME_A_Z,
        SortOption.NAME_Z_A,
        SortOption.PRICE_LOW_HIGH,
        SortOption.PRICE_HIGH_LOW
    ])
    def test_products_sorting(self, sort_option: SortOption) -> None:
        self._login_and_get_main_page()

        self.logger.info(msg=f"Get the original products list and sort it according to the option: {sort_option}")

        expected_products_order: List[Product] = self.main_page.inventory_page.get_all_products()
        expected_products_order.sort(
            key=lambda x: x.product_name if sort_option in [SortOption.NAME_A_Z, SortOption.NAME_Z_A] else x.product_price)

        self.logger.info(msg=f"Select the order of product : {sort_option}")
        self.main_page.inventory_page.choice_product_selector_option(sort_option=sort_option)

        self.logger.info(msg=f"Get the ordered products list")
        actual_products_order: List[Product] = self.main_page.inventory_page.get_all_products()

        if sort_option in [SortOption.NAME_Z_A, SortOption.PRICE_HIGH_LOW]:
            expected_products_order.reverse()

        self.logger.info(msg=f"Verify the order of actual products is as the expected products order...")

        if sort_option in [SortOption.NAME_A_Z, SortOption.NAME_Z_A]:
            actual_names = [p.product_name for p in actual_products_order]
            expected_names = [p.product_name for p in expected_products_order]

            self.test_helper.assert_equal_list(
                expected_list=expected_names,
                actual_list=actual_names,
                error_msg=f"Products not sorted correctly for {sort_option} option.",

            )

        if sort_option in [SortOption.PRICE_LOW_HIGH, SortOption.PRICE_HIGH_LOW]:
            actual_prices = [p.product_price for p in actual_products_order]
            expected_prices = [p.product_price for p in expected_products_order]

            self.test_helper.assert_equal_list(
                expected_list=expected_prices,
                actual_list=actual_prices,
                error_msg=f"Products not sorted correctly for {sort_option} option.",

            )

        self.logger.info(f"Sort the products inventory with order {sort_option} is passed")

    def _login_and_get_main_page(self) ->None:
        self.logger.info(msg="Attempt login with credentials - User: standard_user")

        self.login_page.load()
        self.login_page.login(username="standard_user", password="secret_sauce")

        self.test_helper.assert_and_log(
            condition=self.main_page.is_user_logged_in(),
            error_msg="Login failed (expected success login)"
        )

        self.logger.info(msg="Login successful - proceeding with main page")
