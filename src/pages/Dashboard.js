import React, { useEffect, useState } from "react";
import { getProfile } from "../api/api";
import Wallet from "./Wallet";
import Market from "./Market";

function Dashboard({ token, onLogout }) {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    getProfile(token).then(res => setProfile(res.data));
  }, [token]);

  if (!profile) return <p>در حال بارگذاری...</p>;

  return (
    <div>
      <h2>داشبورد</h2>
      <p><b>ایمیل:</b> {profile.email}</p>
      <p><b>نام نمایشی:</b> {profile.display_name}</p>
      <button onClick={onLogout}>خروج</button>
      <hr/>
      <Wallet token={token} />
      <hr/>
      <Market token={token} />
    </div>
  );
}

export default Dashboard;