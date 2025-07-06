import React, { useEffect, useState } from "react";
import { getWallet, deposit, withdraw } from "../api/api";

function Wallet({ token }) {
  const [wallet, setWallet] = useState(null);
  const [amount, setAmount] = useState("");

  const loadWallet = () =>
    getWallet(token).then(res => setWallet(res.data));

  useEffect(() => { loadWallet(); }, [token]);

  const handleDeposit = async () => {
    await deposit(token, amount);
    loadWallet();
    setAmount("");
  };
  const handleWithdraw = async () => {
    await withdraw(token, amount);
    loadWallet();
    setAmount("");
  };

  if (!wallet) return <div>در حال بارگذاری ولت...</div>;

  return (
    <div>
      <h3>کیف پول</h3>
      <p>آدرس: {wallet.address}</p>
      <p>موجودی: {wallet.balance}</p>
      <input value={amount} onChange={e=>setAmount(e.target.value)} placeholder="مقدار"/>
      <button onClick={handleDeposit}>واریز</button>
      <button onClick={handleWithdraw}>برداشت</button>
    </div>
  );
}

export default Wallet;