import uuid
from sqlalchemy import Column, String, DateTime, Numeric, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    display_name = Column(String)
    avatar_url = Column(String)
    profile_data = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ai_robots = relationship("AIRobot", back_populates="user")
    personality_profiles = relationship("PersonalityProfile", back_populates="user")
    nft_avatars = relationship("NFTAvatar", back_populates="user")
    market_items = relationship("MarketItem", back_populates="seller")
    wallet = relationship("Wallet", uselist=False, back_populates="user")

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    address = Column(String, unique=True, index=True, nullable=False)
    balance = Column(Numeric, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="wallet")
    transactions = relationship("Transaction", back_populates="wallet")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey('wallets.id'))
    tx_type = Column(String)
    amount = Column(Numeric)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    wallet = relationship("Wallet", back_populates="transactions")

class BotChatLog(Base):
    __tablename__ = "bot_chat_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    bot_name = Column(String)
    user_message = Column(Text)
    bot_reply = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class AIRobot(Base):
    __tablename__ = "ai_robots"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    robot_type = Column(String)
    config = Column(JSONB)
    state = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="ai_robots")

class MarketItem(Base):
    __tablename__ = "market_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    title = Column(String)
    description = Column(Text)
    price = Column(Numeric)
    extra_data = Column(JSONB)
    status = Column(String, default="active")  # active, sold, removed
    created_at = Column(DateTime, default=datetime.utcnow)
    seller = relationship("User", back_populates="market_items")

class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_id = Column(UUID(as_uuid=True))
    to_id = Column(UUID(as_uuid=True))
    text = Column(Text)
    type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class PersonalityProfile(Base):
    __tablename__ = "personality_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    traits = Column(JSONB)
    emotional_map = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="personality_profiles")

class NFTAvatar(Base):
    __tablename__ = "nft_avatars"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    glb_url = Column(String)
    minted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="nft_avatars")

class PetriumChainTX(Base):
    __tablename__ = "petrium_chain_tx"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_addr = Column(String)
    to_addr = Column(String)
    token = Column(String)
    amount = Column(Numeric)
    status = Column(String)
    tx_hash = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class MarketOrder(Base):
    __tablename__ = "market_orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    item_id = Column(UUID(as_uuid=True), ForeignKey('market_items.id'))
    amount = Column(Numeric)
    status = Column(String, default="pending")  # pending, paid, delivered, canceled
    created_at = Column(DateTime, default=datetime.utcnow)

class MarketReview(Base):
    __tablename__ = "market_reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey('market_items.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    rating = Column(Numeric)  # امتیاز 1 تا 5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)