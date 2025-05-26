import logo from "./logo.svg";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Dashboard } from "./components/dashboard";
import { Help } from "./components/help";
import { Sidebar } from "./components/sidebar";
import { ToastContainer } from "react-toastify";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Router>
        <Sidebar />
        <ToastContainer theme="light" />
        <div className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/help/:service_name" element={<Help />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
