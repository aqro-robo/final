import React, { useState } from "react";
import { login } from "../api/api";

function Login({ onSwitch, onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await login(email, password);
      onLogin(res.data.access_token);
    } catch (err) {
      setMsg(err.response?.data?.detail || "خطا!");
    }
  };

  return (
    <div>
      <h2>ورود</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="ایمیل" value={email} onChange={e=>setEmail(e.target.value)} required /><br/>
        <input type="password" placeholder="رمزعبور" value={password} onChange={e=>setPassword(e.target.value)} required /><br/>
        <button type="submit">ورود</button>
      </form>
      <p>{msg}</p>
      <button onClick={onSwitch}>ثبت‌نام</button>
    </div>
  );
}
export default Login;