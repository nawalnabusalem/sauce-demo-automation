from typing import List

import pytest

from pages.cart.cart_page import CartItem
from pages.inventory.inventory_page import Product
from tests.base_test import BaseTest


class TestCart(BaseTest):

    @pytest.mark.parametrize("cart_count", [
        3
    ])
    def test_add_products_to_cart(self, cart_count: int) -> None:
        self.test_helper.validate_positive_integer(value=cart_count, field_name="cart_count")

        self._login_and_get_main_page()

        added_products_name: List[str] =self._add_products_to_the_cart(cart_count=cart_count)

        self._verify_cart_badge_count(count=cart_count)

        self.logger.info(msg=f"open the cart page")
        self.main_page.click_cart_button()

        self.logger.info(msg=f"Verify if the added products are in the cart list")

        cart_items_name_list: List[str] = self.main_page.cart_page.get_all_items_name()

        self.test_helper.assert_and_log(condition=len(cart_items_name_list) > 0, error_msg="There is no product added to the cart")
        self.test_helper.assert_equal_and_log(
            actual=len(cart_items_name_list),
            expected=cart_count,
            error_msg="The cart list count is not equal to the requested cart count"
        )

        for product_name in added_products_name:
            self.test_helper.assert_in_list(product_name, cart_items_name_list, "Product")

        self.logger.info(msg=f"Cleanup and remove all the added products from the cart")

        self.main_page.cart_page.click_continue_shopping_button()
        self.main_page.side_menu.reset_app_state()

        self.logger.info(f"Adding {cart_count} products to the cart page is passed")

    @pytest.mark.parametrize("cart_count", [3])
    def test_remove_cart_items_from_inventory(self, browser, cart_count: int) -> None:
        self.test_helper.validate_positive_integer(value=cart_count, field_name="cart_count")

        self._login_and_get_main_page()

        added_products_name: List[str]=self._add_products_to_the_cart(cart_count=cart_count)
        self._verify_cart_badge_count(count=cart_count)

        self.logger.info(msg=f"Remove all the added products in the cart from the inventory page")
        self._remove_products_using_inventory_by_name(added_products_name=added_products_name)

        self._verify_cart_badge_count(count=0)

        self.logger.info(f"Adding and removing {cart_count} products to/from inventory passed")

    @pytest.mark.parametrize("cart_count", [2])
    def test_remove_cart_items_from_cart(self, browser, cart_count: int) -> None:
        self.test_helper.validate_positive_integer(value=cart_count, field_name="cart_count")

        self._login_and_get_main_page()

        self._add_products_to_the_cart(cart_count=cart_count)
        self._verify_cart_badge_count(count=cart_count)

        self.logger.info("Open cart page")
        self.main_page.click_cart_button()

        self.logger.info(msg=f"Remove all the added products in the cart from the cart page")
        cart_items_list: List[CartItem] = self.main_page.cart_page.get_all_cart_items()

        self.test_helper.assert_equal_and_log(
            actual=len(cart_items_list),
            expected=cart_count,
            error_msg="The cart list count is not equal to the requested cart count"
        )

        for cart_item in cart_items_list:
            self.logger.info(msg=f'Remove the cart item {cart_item.item_name} from the cart list')

            cart_item.remove_product_from_cart()

        self.logger.info(msg=f"Verify cart is now empty")
        cart_items_list: List[CartItem] = self.main_page.cart_page.get_all_cart_items()
        self.test_helper.assert_and_log(condition=len(cart_items_list) == 0, error_msg="The cart list is not empty")


        self.logger.info(msg=f"Return back the inventory page")
        self.main_page.cart_page.click_continue_shopping_button()

        self.logger.info(msg=f"Verify no product has remove-from-cart button")
        product_list: List[Product] = self.main_page.inventory_page.get_all_products()

        for product in product_list:
            self.test_helper.assert_and_log(
                condition=product.remove_from_cart_button is None,
                error_msg=f"Product {product.product_name} should not have a remove button"
            )

        self._verify_cart_badge_count(count=0)

        self.logger.info(f"Adding and removing {cart_count} products to the cart from the cart is passed")

    def _login_and_get_main_page(self) -> None:
        self.logger.info(msg="Attempt login with credentials - User: secret_sauce")
        self.login_page.load()
        self.login_page.login(username="standard_user",password="secret_sauce")

        self.test_helper.assert_and_log(
            condition=self.main_page.is_user_logged_in(),
            error_msg="Login failed (expected success login)"
        )

        self.logger.info(msg="Login successful - proceeding with main page")

    def _verify_cart_badge_count(self, count: int) -> None:
        self.logger.info(msg=f"Verify the cart count badge")
        self.test_helper.assert_equal_and_log(
            actual=self.main_page.get_cart_count(),
            expected=count,
            error_msg=f"The cart badge count is {self.main_page.get_cart_count()}, but it should be: {count}"
        )

        if count == 0:
            self.logger.info(msg=f"The cart badge is disappeared since the cart is empty")

        else:
            self.logger.info(msg=f"The cart badge count is set correctly to be {count} items")

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

    def _remove_products_using_inventory_by_name(self, added_products_name: List[str]) -> None:
        updated_product_list: List[Product] = self.main_page.inventory_page.get_all_products()

        for product in updated_product_list:
            if product.product_name in added_products_name and product.remove_from_cart_button:
                self.logger.info(msg=f"Remove the product {product.product_name} from the cart")

                product.remove_product_from_cart()
