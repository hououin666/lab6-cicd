from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.user_id_input = "#userId"
        self.add_item_button = "#addItemBtn"
        self.submit_button = "#submitOrderBtn"
        self.result_area = "#resultArea"

    def navigate(self, url="http://localhost:3000"):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def set_user_id(self, user_id: int):
        self.page.fill(self.user_id_input, str(user_id))

    def add_item(self, name: str, price: float, quantity: int):
        # Ждем, пока кнопка добавления станет доступна
        self.page.wait_for_selector(self.add_item_button, state="visible")
        self.page.click(self.add_item_button)

        # Ждем появления новой строки
        self.page.wait_for_selector(".item-row", state="visible")

        # Находим последнюю строку
        rows = self.page.locator(".item-row")
        last_row = rows.last

        # Заполняем поля
        last_row.locator(".item-name").fill(name)
        last_row.locator(".item-price").fill(str(price))
        last_row.locator(".item-quantity").fill(str(quantity))

        # Небольшая пауза для обновления DOM
        self.page.wait_for_timeout(200)

    def clear_all_items(self):
        rows = self.page.locator(".item-row")
        # Удаляем все строки, кроме первой пустой
        while rows.count() > 1:
            rows.nth(1).locator(".remove-item").click()
            self.page.wait_for_timeout(100)

    def submit_order(self):
        # Ждем, когда кнопка станет видимой и кликабельной
        submit_btn = self.page.locator(self.submit_button)
        submit_btn.wait_for(state="visible", timeout=5000)
        submit_btn.click()

    def get_success_message(self) -> str:
        result_div = self.page.locator("#resultArea.success")
        expect(result_div).to_be_visible(timeout=10000)
        return result_div.text_content()

    def get_error_message(self) -> str:
        result_div = self.page.locator("#resultArea.error")
        expect(result_div).to_be_visible(timeout=10000)
        return result_div.text_content()