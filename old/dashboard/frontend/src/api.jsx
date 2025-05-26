import { toast } from "react-toastify";

const API_BASE = "http://backend.smiley.hb.teamsmiley.org";

class Service {
  constructor(name, status, description, url, help) {
    this.name = name;
    this.status = status;
    this.description = description;
    this.url = url;
    this.help = help;
  }
}

async function request(path) {
  return (await fetch(API_BASE + path)).text();
}

async function list_services() {
  const data = JSON.parse(await request("/services/list"));
  const services = Object.entries(data).map(([name, data]) => {
    return new Service(
      name,
      data["status"],
      data["description"],
      data["url"],
      data["help"],
    );
  });
  return services;
}

async function get_service_status(service_name) {
  return JSON.parse(await request(`/services/${service_name}/status`));
}

async function start_service(service_name) {
  toast(`Starting ${service_name}`, { hideProgressBar: true });
  return JSON.parse(await request(`/services/${service_name}/start`));
}

async function stop_service(service_name) {
  toast(`Stopping ${service_name}`, { hideProgressBar: true });
  return JSON.parse(await request(`/services/${service_name}/stop`));
}

async function restart_service(service_name) {
  toast(`Restarting ${service_name}`, { hideProgressBar: true });
  return JSON.parse(await request(`/services/${service_name}/restart`));
}

async function get_service_help(service_name) {
  return JSON.parse(await request(`/services/${service_name}/help`));
}

export {
  list_services,
  get_service_status,
  start_service,
  stop_service,
  restart_service,
  get_service_help,
  API_BASE,
};
