import "./servicecard.css";
import { start_service, stop_service, restart_service, API_BASE } from "../api";
import { Link } from "react-router-dom";
import { IoHelpCircleOutline } from "react-icons/io5";
import { FaPowerOff, FaLink } from "react-icons/fa6";
import { RiSettings2Fill } from "react-icons/ri";
import { FaGooglePlay } from "react-icons/fa";
import { FaAppStoreIos } from "react-icons/fa";
import { Popup } from "reactjs-popup";

function ServiceCard({ service, service_logo }) {
  return (
    <div
      className={"service-card " + "service-" + service.status}
      key={service.name}
    >
      <img src={service_logo} alt={service.name} className="service-logo" />
      <div className="service-controls">
        <h2 className="service-name">
          {service.name}
          <span className="service-controls">
            <RiSettings2Fill size={"1.5rem"} />
          </span>
        </h2>
        {service.status === "running" ? (
          <button
            className="service-button running"
            onClick={() => {
              stop_service(service.name);
            }}
          >
            <FaPowerOff className="power-icon" />{" "}
            <span className="status-msg">{service.status}</span>
          </button>
        ) : (
          <button
            className="service-button stopped"
            onClick={() => {
              start_service(service.name);
            }}
          >
            <FaPowerOff className="power-icon" />{" "}
            <span className="status-msg">{service.status}</span>
          </button>
        )}
        <a href={service.url} className="service-link">
          <FaLink size={"1.5rem"} />
        </a>
        <br style={{ marginBottom: "2rem" }} />
        <Popup
          modal
          nested
          trigger={
            <span to={"/help/" + service.name} className="service-button help">
              Help
              <IoHelpCircleOutline className="help-icon" size={"1.5rem"} />
            </span>
          }
        >
          {(close) => (
            <div className="modal-popup">
              <h2>{service.name}</h2>
              <p>{service.help.description}</p>
              <h4>Instructions</h4>
              <ol>
                {service.help.instructions.map((instruction, index) => {
                  return (
                    <li key={index}>
                      <p>{instruction}</p>
                    </li>
                  );
                })}
              </ol>
              <div className="downloads">
                <Link to={service.help.link.google} className="google-play">
                  <FaGooglePlay size={"2rem"} />
                </Link>
                <Link to={service.help.link.apple} className="app-store">
                  <FaAppStoreIos size={"2rem"} />
                </Link>
              </div>
            </div>
          )}
        </Popup>
      </div>
    </div>
  );
}

export { ServiceCard };
