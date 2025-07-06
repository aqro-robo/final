from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from . import crud, schemas
from .auth import create_access_token, verify_access_token
from .models import Wallet, Transaction, Message, BotChatLog, MarketItem, MarketOrder, User
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, Dict, List
import os
import shutil
import uuid
import asyncio

# --------- ایمپورت روبات‌ها و ساخت دیکشنری مرکزی BOT_MAP ---------
from .aqro_bots.petros import PetrosBot
from .aqro_bots.azra import AzraBot
from .aqro_bots.zentrox import ZentroxBot
from .aqro_bots.nava import NavaBot
from .aqro_bots.sayra import SayraBot
from .aqro_bots.zilat import ZilatBot

BOT_MAP = {
    "petros": PetrosBot(),
    "azra": AzraBot(),
    "zentrox": ZentroxBot(),
    "nava": NavaBot(),
    "sayra": SayraBot(),
    "zilat": ZilatBot(),
}

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # برای تست *، برای تولید فقط دامنه‌ات رو بذار
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(crud.User).filter(crud.User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def admin_required(current_user: crud.User = Depends(get_current_user)):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# ========== Auth & Profile & Avatar ==========
@app.post("/register", response_model=schemas.UserProfileOut)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db, user)
    return db_user

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.verify_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer", "user": db_user}

@app.get("/profile/me", response_model=schemas.UserProfileOut)
def get_my_profile(current_user: crud.User = Depends(get_current_user)):
    return current_user

@app.put("/profile/me", response_model=schemas.UserProfileOut)
def update_my_profile(update: schemas.UserProfileUpdate, db: Session = Depends(get_db), current_user: crud.User = Depends(get_current_user)):
    user = crud.update_user_profile(db, current_user.id, update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/profile/me/avatar")
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Avatar must be jpeg or png.")
    ext = file.filename.split('.')[-1]
    filename = f"{current_user.id}_{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    current_user.avatar_url = f"/uploads/{filename}"
    db.commit()
    db.refresh(current_user)
    return {"avatar_url": current_user.avatar_url}

from fastapi.staticfiles import StaticFiles
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

# ========== Wallet ==========
@app.get("/wallet/me", response_model=schemas.WalletOut)
def get_my_wallet(
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    wallet = crud.get_or_create_wallet(db, current_user.id)
    return wallet

@app.post("/wallet/me/deposit", response_model=schemas.TransactionOut)
def deposit(
    amount: float,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    wallet = crud.get_or_create_wallet(db, current_user.id)
    tx = crud.create_transaction(db, wallet.id, "deposit", amount)
    return tx

@app.post("/wallet/me/withdraw", response_model=schemas.TransactionOut)
def withdraw(
    amount: float,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    wallet = crud.get_or_create_wallet(db, current_user.id)
    tx = crud.create_transaction(db, wallet.id, "withdraw", amount)
    return tx

@app.get("/wallet/me/transactions", response_model=List[schemas.TransactionOut])
def list_my_transactions(
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    wallet = crud.get_or_create_wallet(db, current_user.id)
    return crud.get_transactions(db, wallet.id)

# ========== Messaging API (REST) ==========
@app.post("/messages/send", response_model=schemas.MessageOut)
def send_message_api(
    msg: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    sent_msg = crud.send_message(db, from_id=current_user.id, to_id=msg.to_id, text=msg.text, type=msg.type)
    return sent_msg

@app.get("/messages/{to_user_id}", response_model=List[schemas.MessageOut])
def get_chat_with_user(
    to_user_id: str,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    msgs = crud.get_messages_between_users(db, current_user.id, to_user_id)
    return msgs

# ========== Messaging API (WebSocket Chat) ==========
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/chat/{to_user_id}")
async def websocket_chat(websocket: WebSocket, to_user_id: str, token: Optional[str] = None):
    await websocket.accept()
    if token is None:
        await websocket.close(code=4001)
        return
    payload = verify_access_token(token)
    if not payload or "user_id" not in payload:
        await websocket.close(code=4003)
        return
    user_id = payload["user_id"]
    active_connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            text = data.get("text")
            msg_type = data.get("type", "text")
            db = SessionLocal()
            crud.send_message(db, from_id=user_id, to_id=to_user_id, text=text, type=msg_type)
            db.close()
            receiver_ws = active_connections.get(to_user_id)
            if receiver_ws:
                await receiver_ws.send_json({
                    "from_id": user_id,
                    "to_id": to_user_id,
                    "text": text,
                    "type": msg_type
                })
    except WebSocketDisconnect:
        if user_id in active_connections:
            del active_connections[user_id]

# ========== Bots Central Endpoint ==========
@app.post("/bots/{bot_name}/chat")
def chat_with_bot(
    bot_name: str,
    message: str,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    user_profile = current_user.profile_data or {}
    bot = BOT_MAP.get(bot_name)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    reply = bot.reply(user_profile, message)
    crud.log_bot_chat(db, current_user.id, bot_name, message, reply)
    asyncio.create_task(send_notification(
        current_user.id,
        {"type": "bot_reply", "bot": bot_name, "message": reply}
    ))
    return {"bot": bot_name, "reply": reply}

@app.get("/bots/{bot_name}/history")
def bot_chat_history(
    bot_name: str,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    logs = db.query(BotChatLog).filter(
        BotChatLog.user_id == current_user.id,
        BotChatLog.bot_name == bot_name
    ).order_by(BotChatLog.timestamp.desc()).all()
    return [
        {
            "timestamp": log.timestamp,
            "user_message": log.user_message,
            "bot_reply": log.bot_reply
        }
        for log in logs
    ]

# ========== Marketplace ==========
@app.post("/market/item", response_model=schemas.MarketItemOut)
def create_market_item_api(
    item: schemas.MarketItemCreate,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    return crud.create_market_item(db, current_user.id, item)

@app.get("/market/items", response_model=List[schemas.MarketItemOut])
def list_market_items_new_new_api(db: Session = Depends(get_db)):
    return crud.list_market_items_new_new(db)

@app.post("/market/order", response_model=schemas.MarketOrderOut)
def create_market_order_api(
    order: schemas.MarketOrderCreate,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    created = crud.create_market_order(db, current_user.id, order.item_id, order.amount)
    if not created:
        raise HTTPException(status_code=400, detail="Item not available")
    return created

@app.get("/market/myorders", response_model=List[schemas.MarketOrderOut])
def list_my_orders_api(
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    return crud.list_my_orders(db, current_user.id)

# ========== Admin Panel ==========
@app.get("/admin/users")
def admin_list_users(
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(admin_required)
):
    return db.query(User).all()

@app.get("/admin/market/items")
def admin_list_market_items_new_new(
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(admin_required)
):
    return db.query(MarketItem).all()

@app.get("/admin/orders")
def admin_list_orders(
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(admin_required)
):
    return db.query(MarketOrder).all()

# ========== Notification WebSocket ==========
notification_connections: Dict[str, List[WebSocket]] = {}

@app.websocket("/ws/notifications")
async def notifications_ws(websocket: WebSocket, token: str = None):
    await websocket.accept()
    if token is None:
        await websocket.close(code=4001)
        return
    payload = verify_access_token(token)
    if not payload or "user_id" not in payload:
        await websocket.close(code=4003)
        return
    user_id = payload["user_id"]
    if user_id not in notification_connections:
        notification_connections[user_id] = []
    notification_connections[user_id].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_connections[user_id].remove(websocket)
        if not notification_connections[user_id]:
            del notification_connections[user_id]

async def send_notification(user_id: str, notification: dict):
    connections = notification_connections.get(user_id, [])
    for ws in connections:
        try:
            await ws.send_json(notification)
        except Exception:
            continue

@app.get("/")
def read_root():
    return {"Aqro": "API is up & running!"}


@app.post("/market/review", response_model=schemas.MarketReviewOut)
def add_market_review_api(
    review: schemas.MarketReviewCreate,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_user)
):
    return crud.add_market_review(db, current_user.id, review)

@app.get("/market/item/{item_id}/reviews", response_model=List[schemas.MarketReviewOut])
def get_market_item_reviews_api(
    item_id: str,
    db: Session = Depends(get_db)
):
    return crud.get_item_reviews(db, item_id)
