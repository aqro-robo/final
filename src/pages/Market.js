import React, { useEffect, useState } from "react";
import { getMarketItems, createMarketItem, createMarketOrder } from "../api/api";

function Market({ token }) {
  const [items, setItems] = useState([]);
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [price, setPrice] = useState("");

  const loadItems = () => getMarketItems().then(res => setItems(res.data));
  useEffect(() => { loadItems(); }, []);

  const handleCreate = async () => {
    await createMarketItem(token, { title, description: desc, price: parseFloat(price) });
    loadItems();
    setTitle(""); setDesc(""); setPrice("");
  };

  const handleBuy = async (item) => {
    await createMarketOrder(token, { item_id: item.id, amount: item.price });
    alert("سفارش ثبت شد");
  };

  return (
    <div>
      <h3>مارکت</h3>
      <input placeholder="عنوان" value={title} onChange={e=>setTitle(e.target.value)} />
      <input placeholder="توضیح" value={desc} onChange={e=>setDesc(e.target.value)} />
      <input placeholder="قیمت" value={price} onChange={e=>setPrice(e.target.value)} />
      <button onClick={handleCreate}>ایجاد آیتم</button>
      <hr />
      {items.map(item =>
        <div key={item.id} style={{border:"1px solid #ccc",margin:6,padding:5}}>
          <b>{item.title}</b> - {item.price} تومان
          <br/>
          {item.description}
          <br/>
          <button onClick={()=>handleBuy(item)}>خرید</button>
        </div>
      )}
    </div>
  );
}

export default Market;