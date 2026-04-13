import requests
from sqlalchemy.orm import Session
import models
import repository

# 🔥 PRODUCT SERVICE URL
PRODUCT_SERVICE_URL = "http://127.0.0.1:8001"

# ADD TO CART (with validation)
def add_to_cart_service(db: Session, user_id: int, product_id: int, quantity: int):

    # 🔥 CALL PRODUCT SERVICE
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")

    # Validate product exists
    if response.status_code != 200:
        raise Exception("Product not found")

    product = response.json()

    # Validate stock
    if product["stock"] < quantity:
        raise Exception("Insufficient stock")

    # 🔥 CREATE CART
    cart = models.Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)

    # 🔥 ADD ITEM
    cart_item = models.CartItem(
        cart_id=cart.id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Item added to cart",
        "cart_id": cart.id
    }