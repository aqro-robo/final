from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from .models import (
    User, Wallet, Transaction, MarketItem, MarketOrder, MarketReview,
    BotChatLog
)
from .schemas import UserRegister, UserProfileUpdate
import uuid

# ========== User/Account ==========
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserRegister):
    hashed_pw = bcrypt.hash(user.password)
    db_user = User(
        id=uuid.uuid4(),
        email=user.email,
        password_hash=hashed_pw,
        display_name=user.display_name,
        profile_data={}
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    create_wallet_for_user(db, db_user.id)
    return db_user

def verify_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not bcrypt.verify(password, user.password_hash):
        return None
    return user

def update_user_profile(db: Session, user_id, update_data: UserProfileUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    if update_data.display_name is not None:
        user.display_name = update_data.display_name
    if update_data.avatar_url is not None:
        user.avatar_url = update_data.avatar_url
    if update_data.profile_data:
        user.profile_data = {**(user.profile_data or {}), **update_data.profile_data}
    db.commit()
    db.refresh(user)
    return user

# ========== Wallet & Transaction ==========
def create_wallet_for_user(db: Session, user_id: str):
    address = str(uuid.uuid4())
    wallet = Wallet(id=uuid.uuid4(), user_id=user_id, address=address, balance=0)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet

def get_or_create_wallet(db: Session, user_id: str):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        wallet = create_wallet_for_user(db, user_id)
    return wallet

def get_wallet_by_user(db: Session, user_id: str):
    return db.query(Wallet).filter(Wallet.user_id == user_id).first()

def create_transaction(db: Session, wallet_id: str, tx_type: str, amount: float):
    tx = Transaction(
        id=uuid.uuid4(),
        wallet_id=wallet_id,
        tx_type=tx_type,
        amount=amount,
        status="done",
    )
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if tx_type == "deposit":
        wallet.balance += amount
    elif tx_type == "withdraw" and wallet.balance >= amount:
        wallet.balance -= amount
    else:
        tx.status = "failed"
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def get_transactions(db: Session, wallet_id: str):
    return db.query(Transaction).filter(Transaction.wallet_id == wallet_id).all()

# ========== Messaging ==========
def send_message(db: Session, from_id: str, to_id: str, text: str, type: str = "text"):
    from .models import Message
    msg = Message(
        id=uuid.uuid4(),
        from_id=from_id,
        to_id=to_id,
        text=text,
        type=type
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages_between_users(db: Session, user1_id: str, user2_id: str):
    from .models import Message
    return db.query(Message).filter(
        ((Message.from_id == user1_id) & (Message.to_id == user2_id)) |
        ((Message.from_id == user2_id) & (Message.to_id == user1_id))
    ).order_by(Message.timestamp.asc()).all()

# ========== Bot Chat Log ==========
def log_bot_chat(db: Session, user_id: str, bot_name: str, user_message: str, bot_reply: str):
    log = BotChatLog(
        id=uuid.uuid4(),
        user_id=user_id,
        bot_name=bot_name,
        user_message=user_message,
        bot_reply=bot_reply,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

# ========== Marketplace ==========
def create_market_item(db: Session, seller_id: str, data):
    item = MarketItem(
        id=uuid.uuid4(),
        seller_id=seller_id,
        title=data.title,
        description=data.description,
        price=data.price,
        extra_data=data.extra_data or {},
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_market_items_new_new(db: Session):
    return db.query(MarketItem).filter(MarketItem.status == "active").all()

def create_market_order(db: Session, buyer_id: str, item_id: str, amount: float):
    item = db.query(MarketItem).filter(MarketItem.id == item_id, MarketItem.status == "active").first()
    if not item or amount < item.price:
        return None

    # ولت خریدار و فروشنده
    buyer_wallet = db.query(Wallet).filter(Wallet.user_id == buyer_id).first()
    seller_wallet = db.query(Wallet).filter(Wallet.user_id == item.seller_id).first()

    # چک موجودی خریدار
    if not buyer_wallet or buyer_wallet.balance < amount:
        return None

    # کم کردن موجودی خریدار و اضافه کردن به فروشنده
    buyer_wallet.balance -= amount
    seller_wallet.balance += amount

    # ثبت تراکنش برای هر دو
    tx_buyer = Transaction(
        id=uuid.uuid4(),
        wallet_id=buyer_wallet.id,
        tx_type="market_buy",
        amount=-amount,
        status="done"
    )
    tx_seller = Transaction(
        id=uuid.uuid4(),
        wallet_id=seller_wallet.id,
        tx_type="market_sell",
        amount=amount,
        status="done"
    )

    db.add(tx_buyer)
    db.add(tx_seller)

    # ثبت سفارش
    order = MarketOrder(
        id=uuid.uuid4(),
        buyer_id=buyer_id,
        item_id=item_id,
        amount=amount,
        status="paid"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def list_my_orders(db: Session, buyer_id: str):
    return db.query(MarketOrder).filter(MarketOrder.buyer_id == buyer_id).all()

# ========== Market Review ==========
def add_market_review(db: Session, user_id: str, data):
    review = MarketReview(
        id=uuid.uuid4(),
        item_id=data.item_id,
        user_id=user_id,
        rating=data.rating,
        comment=data.comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_item_reviews(db: Session, item_id: str):
    return db.query(MarketReview).filter(MarketReview.item_id == item_id).all()
