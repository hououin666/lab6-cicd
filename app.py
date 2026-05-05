from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import os

app = FastAPI(title="Корзина интернет-магазина API", version="1.0.0")

# Подключаем статические файлы (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="public"), name="static")


@app.get("/")
async def serve_index():
    """Отдает главную страницу"""
    return FileResponse("public/index.html")




orders_db = []


class Item(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)


class CheckoutRequest(BaseModel):
    userId: int
    items: List[Item]
    autoDiscountThreshold: float = 5000.0
    autoDiscountPercent: float = 5.0


@app.get("/api/status")
async def get_status():
    return {"status": "online", "timestamp": datetime.now().isoformat()}


@app.get("/api/users/{userId}/discount")
async def get_user_discount(userId: int):
    if userId not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"userId": userId, "discount": users_db[userId]["discount"]}


users_db = {
    1: {"discount": 10, "balance": 100000},  # ← добавили баланс
    2: {"discount": 0, "balance": 5000},  # ← добавили баланс
}


@app.post("/api/cart/checkout", status_code=201)
async def checkout_order(request: CheckoutRequest):
    if not request.items:
        raise HTTPException(status_code=400, detail="Корзина пуста")

    # Проверка существования пользователя
    if request.userId not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user_discount = users_db[request.userId]["discount"]
    user_balance = users_db[request.userId]["balance"]  # ← получаем баланс

    subtotal = sum(item.price * item.quantity for item in request.items)
    personal_discount = subtotal * (user_discount / 100)
    after_personal = subtotal - personal_discount

    # Проверка баланса
    if after_personal > user_balance:
        raise HTTPException(status_code=400, detail="Недостаточно средств на балансе")

    auto_discount = 0.0
    auto_applied = False
    if after_personal > 5000:
        auto_discount = after_personal * 0.05
        final_total = after_personal - auto_discount
        auto_applied = True
    else:
        final_total = after_personal

    should_send_promo = after_personal > 10000

    order = {
        "orderId": len(orders_db) + 1,
        "userId": request.userId,
        "subtotal": round(subtotal, 2),
        "personalDiscount": round(personal_discount, 2),
        "autoDiscountApplied": auto_applied,
        "autoDiscount": round(auto_discount, 2),
        "total": round(final_total, 2),
        "couponSent": should_send_promo
    }
    orders_db.append(order)
    return order

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=3000)