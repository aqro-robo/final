from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfileOut(BaseModel):
    id: str
    email: EmailStr
    display_name: Optional[str]
    avatar_url: Optional[str]
    profile_data: Optional[Dict[str, Any]]
    wallet: Optional["WalletOut"] = None

class UserProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    profile_data: Optional[Dict[str, Any]] = None

class WalletOut(BaseModel):
    id: str
    address: str
    balance: float
    created_at: Optional[str]

class TransactionOut(BaseModel):
    id: str
    tx_type: str
    amount: float
    status: str
    created_at: Optional[str]

class MarketItemCreate(BaseModel):
    title: str
    description: str
    price: float
    extra_data: Optional[dict] = None

class MarketItemOut(BaseModel):
    id: str
    seller_id: str
    title: str
    description: str
    price: float
    extra_data: Optional[dict]
    status: str
    created_at: Optional[str]

class MarketOrderCreate(BaseModel):
    item_id: str
    amount: float

class MarketOrderOut(BaseModel):
    id: str
    buyer_id: str
    item_id: str
    amount: float
    status: str
    created_at: Optional[str]

class MarketReviewCreate(BaseModel):
    item_id: str
    rating: float
    comment: str

class MarketReviewOut(BaseModel):
    id: str
    item_id: str
    user_id: str
    rating: float
    comment: str
    created_at: Optional[str]

class MessageCreate(BaseModel):
    to_id: str
    text: str
    type: Optional[str] = "text"

class MessageOut(BaseModel):
    id: str
    from_id: str
    to_id: str
    text: str
    type: Optional[str] = "text"
    timestamp: Optional[str]

from pydantic import Extra
UserProfileOut.update_forward_refs()