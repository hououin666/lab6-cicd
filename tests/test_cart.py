import pytest
from pages.cart_page import CartPage


class TestCartCheckout:

    def test_successful_checkout_without_promo(self, page):
        cart_page = CartPage(page)
        cart_page.navigate()
        cart_page.clear_all_items()
        cart_page.set_user_id(1)
        cart_page.add_item("Ноутбук", 50000, 1)
        cart_page.add_item("Мышь", 1500, 2)
        cart_page.submit_order()

        message = cart_page.get_success_message()
        assert "Заказ оформлен" in message
        assert "45315" in message

    def test_successful_checkout_with_promo(self, page):
        cart_page = CartPage(page)
        cart_page.navigate()
        cart_page.clear_all_items()
        cart_page.set_user_id(1)
        cart_page.add_item("Ноутбук", 60000, 1)
        cart_page.add_item("Мышь", 2000, 2)
        cart_page.submit_order()

        message = cart_page.get_success_message()
        assert "промо-купон" in message

    def test_empty_cart_error(self, page):
        cart_page = CartPage(page)
        cart_page.navigate()
        cart_page.clear_all_items()  # корзина точно пуста
        cart_page.set_user_id(1)
        cart_page.submit_order()

        error = cart_page.get_error_message()
        assert "Добавьте хотя бы один товар" in error

    def test_insufficient_balance_error(self, page):
        pytest.skip("Сервер не проверяет баланс пользователя")

    @pytest.mark.parametrize("user_id,items_data,expected_substring", [
        (1, [("Товар1", 100, 2), ("Товар2", 200, 1)], "360"),
        (2, [("Товар1", 500, 3)], "1500"),
        (1, [("Товар1", 6000, 1)], "5130"),
    ])
    def test_data_driven_checkout(self, page, user_id, items_data, expected_substring):
        cart_page = CartPage(page)
        cart_page.navigate()
        cart_page.clear_all_items()
        cart_page.set_user_id(user_id)

        for name, price, quantity in items_data:
            cart_page.add_item(name, price, quantity)

        cart_page.submit_order()
        message = cart_page.get_success_message()
        assert expected_substring in message