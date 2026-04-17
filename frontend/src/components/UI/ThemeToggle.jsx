import { useState, useEffect } from "react";

export default function ThemeToggle() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("theme") || "light";
  });

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  return (
    <button className="theme-toggle" onClick={toggleTheme} title={`Switch to ${theme === "light" ? "dark" : "light"} mode`}>
      {theme === "light" ? "🌙" : "☀️"}
    </button>
  );
}