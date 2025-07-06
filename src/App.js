import React, { useState, useEffect } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Navbar from "./components/Navbar";

function App() {
  const [page, setPage] = useState("loading"); // حالت اولیه: loading
  const [token, setToken] = useState(null);

  useEffect(() => {
    // توکن را از localStorage بخوان
    const t = localStorage.getItem("token");
    if (t) {
      setToken(t);
      setPage("dashboard");
    } else {
      setPage("login");
    }
  }, []);

  const saveToken = (t) => {
    setToken(t);
    localStorage.setItem("token", t);
    setPage("dashboard");
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem("token");
    setPage("login");
  };

  if (page === "loading") return <div>در حال بارگذاری...</div>;

  if (!token) {
    return (
      <div>
        <Navbar />
        {page === "login" ? (
          <Login onSwitch={() => setPage("register")} onLogin={saveToken} />
        ) : (
          <Register onSwitch={() => setPage("login")} onRegister={() => setPage("login")} />
        )}
      </div>
    );
  }

  // اگر توکن معتبر، مستقیماً داشبورد (یا چت) را نشان بده
  return (
    <div>
      <Navbar />
      <Dashboard token={token} onLogout={logout} />
      {/* اگر صفحه چت داشتی، اینجا جایگزین کن */}
    </div>
  );
}

export default App;