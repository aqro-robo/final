import React, { useState } from "react";
import { register } from "../api/api";

function Register({ onSwitch, onRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register(email, password);
      setMsg("ثبت‌نام موفق! حالا وارد شوید.");
      onRegister();
    } catch (err) {
      setMsg(err.response?.data?.detail || "خطا!");
    }
  };

  return (
    <div>
      <h2>ثبت‌نام</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="ایمیل" value={email} onChange={e=>setEmail(e.target.value)} required /><br/>
        <input type="password" placeholder="رمزعبور" value={password} onChange={e=>setPassword(e.target.value)} required /><br/>
        <button type="submit">ثبت‌نام</button>
      </form>
      <p>{msg}</p>
      <button onClick={onSwitch}>ورود</button>
    </div>
  );
}
export default Register;