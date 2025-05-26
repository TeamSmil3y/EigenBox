import "./help.css";
import {
  get_service_status,
  start_service,
  stop_service,
  restart_service,
  get_service_help,
} from "../api";
import { useEffect, useState } from "react";

function Help(service_name) {
  return <div className="help"></div>;
}

export { Help };
