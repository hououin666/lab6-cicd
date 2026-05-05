document.addEventListener('DOMContentLoaded', () => {
    const userIdInput = document.getElementById('userId');
    const itemsContainer = document.getElementById('itemsContainer');
    const addItemBtn = document.getElementById('addItemBtn');
    const submitBtn = document.getElementById('submitOrderBtn');
    const resultArea = document.getElementById('resultArea');

    function addItemRow(name = '', price = '', quantity = '') {
        const row = document.createElement('div');
        row.className = 'item-row';
        row.innerHTML = `
            <input type="text" class="item-name" placeholder="Название" value="${name}">
            <input type="number" class="item-price" placeholder="Цена" value="${price}">
            <input type="number" class="item-quantity" placeholder="Кол-во" value="${quantity}">
            <button class="remove-item">❌</button>
        `;
        row.querySelector('.remove-item').onclick = () => row.remove();
        itemsContainer.appendChild(row);
    }

    addItemBtn.onclick = () => addItemRow();

    async function submitOrder() {
        const userId = parseInt(userIdInput.value);
        const items = [];

        for (const row of document.querySelectorAll('.item-row')) {
            const name = row.querySelector('.item-name').value;
            const price = parseFloat(row.querySelector('.item-price').value);
            const quantity = parseInt(row.querySelector('.item-quantity').value);
            if (name && price > 0 && quantity > 0) {
                items.push({ name, price, quantity });
            }
        }

        if (items.length === 0) {
            resultArea.textContent = 'Добавьте хотя бы один товар';
            resultArea.className = 'error';
            return;
        }

        try {
            const response = await fetch('/api/cart/checkout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId, items })
            });

            const data = await response.json();

            if (response.ok) {
                let msg = `✅ Заказ оформлен! Сумма: ${data.total} руб.`;
                if (data.couponSent) msg += ' 🎉 Вам отправлен промо-купон!';
                resultArea.textContent = msg;
                resultArea.className = 'success';
            } else {
                resultArea.textContent = `❌ Ошибка: ${data.detail}`;
                resultArea.className = 'error';
            }
        } catch (error) {
            resultArea.textContent = `❌ Ошибка соединения: ${error.message}`;
            resultArea.className = 'error';
        }
    }

    submitBtn.onclick = submitOrder;
});