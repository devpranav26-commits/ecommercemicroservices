import requests
from sqlalchemy.orm import Session
from kafka import KafkaProducer
import json
import logging

import models
import repository

# 🔥 Logging
logging.basicConfig(level=logging.INFO)

# PRODUCT SERVICE URL
PRODUCT_SERVICE_URL = "http://127.0.0.1:8001"

# 🔥 KAFKA PRODUCER
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


# ADD TO CART SERVICE
def add_to_cart_service(db: Session, user_id: int, product_id: int, quantity: int):

    try:
        # 🔹 Call Product Service (with timeout)
        response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}",
            timeout=5
        )

    except requests.exceptions.RequestException:
        raise Exception("Product Service is down")

    # 🔹 Validate product exists
    if response.status_code != 200:
        raise Exception("Product not found")

    product = response.json()

    # 🔹 Validate stock
    if product["stock"] < quantity:
        raise Exception("Insufficient stock")

    # 🔹 Create Cart
    cart = models.Cart(user_id=user_id)
    cart = repository.create_cart(db, cart)

    # 🔹 Add Cart Item
    cart_item = models.CartItem(
        cart_id=cart.id,
        product_id=product_id,
        quantity=quantity
    )

    repository.add_cart_item(db, cart_item)

    # 🔥 KAFKA EVENT
    event = {
        "cartId": cart.id,
        "productId": product_id,
        "quantity": quantity
    }

    try:
        producer.send("cart-topic", value=event)
        producer.flush()  # 🔥 ensure message is sent

        logging.info(f"🔥 Kafka Event Sent: {event}")

    except Exception as e:
        logging.error(f"Kafka error: {str(e)}")

    return {
        "message": "Item added to cart",
        "cartId": cart.id
    }