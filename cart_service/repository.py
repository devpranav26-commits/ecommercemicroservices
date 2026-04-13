from sqlalchemy.orm import Session
from models import Cart, CartItem

# ------------------------------
# CREATE CART
# ------------------------------
def create_cart(db: Session, cart: Cart):
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


# ------------------------------
# ADD ITEM TO CART
# ------------------------------
def add_cart_item(db: Session, item: CartItem):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# ------------------------------
# GET CART BY ID
# ------------------------------
def get_cart_by_id(db: Session, cart_id: int):
    return db.query(Cart).filter(Cart.id == cart_id).first()


# ------------------------------
# GET CART ITEMS BY CART ID
# ------------------------------
def get_cart_items(db: Session, cart_id: int):
    return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()


# ------------------------------
# DELETE CART ITEM
# ------------------------------
def delete_cart_item(db: Session, item_id: int):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item


# ------------------------------
# DELETE CART
# ------------------------------
def delete_cart(db: Session, cart_id: int):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart:
        db.delete(cart)
        db.commit()
    return cart