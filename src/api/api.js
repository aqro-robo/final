import axios from "axios";

// آدرس سرور بک‌اندت را اینجا وارد کن
const API_URL = "http://65.109.202.154:8000"; // مثلا: "http://65.109.202.154:8000"

export const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" }
});

// ------ Auth ------
export function register(email, password) {
  return api.post("/register", { email, password });
}
export function login(email, password) {
  return api.post("/login", { email, password });
}
export function getProfile(token) {
  return api.get("/profile/me", {
    headers: { Authorization: "Bearer " + token }
  });
}
export function updateProfile(token, data) {
  return api.put("/profile/me", data, {
    headers: { Authorization: "Bearer " + token }
  });
}

// ------ Wallet ------
export function getWallet(token) {
  return api.get("/wallet/me", { headers: { Authorization: "Bearer " + token } });
}
export function deposit(token, amount) {
  return api.post(
    `/wallet/me/deposit?amount=${amount}`,
    {},
    { headers: { Authorization: "Bearer " + token } }
  );
}
export function withdraw(token, amount) {
  return api.post(
    `/wallet/me/withdraw?amount=${amount}`,
    {},
    { headers: { Authorization: "Bearer " + token } }
  );
}
export function getTransactions(token) {
  return api.get("/wallet/me/transactions", { headers: { Authorization: "Bearer " + token } });
}

// ------ Market ------
export function getMarketItems() {
  return api.get("/market/items");
}
export function createMarketItem(token, data) {
  return api.post("/market/item", data, { headers: { Authorization: "Bearer " + token } });
}
export function createMarketOrder(token, data) {
  return api.post("/market/order", data, { headers: { Authorization: "Bearer " + token } });
}
export function getMyOrders(token) {
  return api.get("/market/myorders", { headers: { Authorization: "Bearer " + token } });
}

// ------ Review ------
export function addReview(token, data) {
  return api.post("/market/review", data, { headers: { Authorization: "Bearer " + token } });
}
export function getItemReviews(item_id) {
  return api.get(`/market/item/${item_id}/reviews`);
}

// ------ Messages ------
export function sendMessage(token, data) {
  return api.post("/messages/send", data, { headers: { Authorization: "Bearer " + token } });
}
export function getMessages(token, to_user_id) {
  return api.get(`/messages/${to_user_id}`, { headers: { Authorization: "Bearer " + token } });
}

// ------ Bots (Aqro AI Bots) ------
export function chatWithBot(token, bot_name, message) {
  return api.post(
    `/bots/${bot_name}/chat`,
    { message },
    { headers: { Authorization: "Bearer " + token } }
  );
}
export function getBotHistory(token, bot_name) {
  return api.get(
    `/bots/${bot_name}/history`,
    { headers: { Authorization: "Bearer " + token } }
  );
}