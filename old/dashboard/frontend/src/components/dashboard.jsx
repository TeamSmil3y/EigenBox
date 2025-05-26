import "./dashboard.css";
import { ServiceCard } from "./servicecard";
import {
  list_services,
  get_service_status,
  start_service,
  stop_service,
  restart_service,
  get_service_help,
} from "../api";
import { useEffect, useState } from "react";

function Dashboard() {
  const [services, setServices] = useState(null);

  useEffect(() => {
    async function fetchServices() {
      setServices(await list_services());
      setTimeout(() => {
        fetchServices();
      }, 1000);
    }
    fetchServices();
  }, []);

  return (
    <div className="dashboard">
      <div className="dashboard-services">
        {services === null ? (
          <div className="loading"></div>
        ) : (
          services.map((service) => {
            const service_logo_url =
              process.env.PUBLIC_URL + "/service-img/" + service.name + ".jpg";
            return (
              <ServiceCard service={service} service_logo={service_logo_url} />
            );
          })
        )}
      </div>
    </div>
  );
}

export { Dashboard };
