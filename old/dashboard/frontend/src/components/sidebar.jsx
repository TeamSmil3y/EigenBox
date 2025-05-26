import "./sidebar.css";
import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { FaCircleCheck, FaHouse } from "react-icons/fa6";
import { MdEmail } from "react-icons/md";
import { BsGearWide } from "react-icons/bs";
import { AiFillMessage } from "react-icons/ai";
import { MdDashboard } from "react-icons/md";

function Sidebar() {
  const location = useLocation();
  let active_path = location.pathname;

  const pages = {
    "/": <FaHouse size={"2rem"} />,
    "/p2p": <AiFillMessage size={"2rem"} />,
    "/email": <MdEmail size={"2rem"} />,
  };

  return (
    <>
      <div className="topbar">
        <h2 className="brand">EigenBox</h2>
        <div className="meta">
          <span className="version">Version 0.1.5</span>
          <span className="update-icon">
            <FaCircleCheck size={"1.5rem"} />
          </span>
        </div>
      </div>
      <div className="page-bar">
        {Object.entries(pages).map(([path, icon]) => {
          return (
            <Link
              to={path}
              className={
                "sidebar-link " + (active_path === path ? "active" : "")
              }
            >
              {icon}
            </Link>
          );
        })}
      </div>
    </>
  );
}

export { Sidebar };
