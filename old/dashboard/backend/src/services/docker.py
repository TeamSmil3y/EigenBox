from .exceptions import ServiceNotFoundError
import subprocess

SERVICES = {
    "nextcloud": {
        "description": "Self-hosted cloud storage and collaboration platform.",
        "url": "http://cloud.smiley.hb.teamsmiley.org",
        "help": {
            "description": "Nextcloud is a self-hosted productivity platform that keeps you in control.",
            "link": {
                "apple": "https://apps.apple.com/us/app/nextcloud/id1125420102",
                "google": "https://play.google.com/store/apps/details?id=com.nextcloud.client&pcampaignid=web_share",
            },
            "instructions": [
                "Download the Nextcloud app from the App Store or Google Play.",
                "Open the app and enter your server URL (e.g., http://cloud.smiley.hb.teamsmiley.org).",
                "Log in with your Nextcloud credentials.",
                "Start using Nextcloud to store and share files securely."
            ]
        }
    },
    "photoprism": {
        "description": "AI-powered photo management and sharing platform.",
        "url": "http://photos.smiley.hb.teamsmiley.org",
        "help": {
            "description": "PhotoPrism is an AI-powered photo app for the decentralized web.",
            "link": {
                "apple": "https://apps.apple.com/de/app/photo-uploader-for-photoprism/id1607500083?l=en-GB",
                "google": "https://play.google.com/store/apps/details?id=ua.com.radiokot.photoprism",
            },
            "instructions": [
                "Open your web browser and go to your PhotoPrism server URL (e.g., http://your-server-ip:8020).",
                "Log in with username 'admin' and password 'teamsmiley'.",
                "Upload photos to the originals folder or use the web interface.",
                "PhotoPrism will automatically index and organize your photos with AI."
            ]
        }
    },
}

def list_services():
    results = {}
    for service_name, meta in SERVICES.items():
        try:
            output = subprocess.check_output(["docker", "inspect", "-f", "{{.State.Status}}", service_name], stderr=subprocess.DEVNULL)
            status = output.decode().strip()
        except subprocess.CalledProcessError:
            status = "not found"
        results[service_name] = {
            "status": status, 
            "description": meta["description"], 
            "url": meta["url"], 
            "help": meta["help"]
        }
    return results

def check_service_name(func):
    def wrapper(service_name: str, *args, **kwargs):
        if service_name not in SERVICES:
            raise ServiceNotFoundError(f"Service '{service_name}' not found.")
        return func(service_name, *args, **kwargs)
    return wrapper

@check_service_name
def service_status(service_name: str):
    try:
        output = subprocess.check_output(["docker", "inspect", "-f", "{{.State.Status}}", service_name], stderr=subprocess.DEVNULL)
        return {"status": output.decode().strip()}
    except subprocess.CalledProcessError:
        return {"status": "not found"}

@check_service_name
def restart_service(service_name: str):
    subprocess.run(["docker", "restart", service_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return {"status": "restarted"}

@check_service_name
def stop_service(service_name: str):
    subprocess.run(["docker", "stop", service_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["docker", "container", "prune", "-f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return {"status": "stopped"}

@check_service_name
def start_service(service_name: str):
    if service_name == "nextcloud":
        try:
            # Try to start existing container first
            result = subprocess.run(["docker", "start", "nextcloud"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"status": "started"}
        except subprocess.CalledProcessError:
            # Container doesn't exist, create and run it
            try:
                subprocess.run([
                    "docker", "run", "-d",
                    "--name", "nextcloud",
                    "--memory", "2048m",
                    "-p", "8010:80",
                    "-v", "/opt/nextcloud/data:/var/www/html/data",
                    "nextcloud"
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return {"status": "started"}
            except subprocess.CalledProcessError as e:
                return {"status": "error", "message": "Failed to start nextcloud container"}
    elif service_name == "photoprism":
        try:
            # Try to start existing container first
            result = subprocess.run(["docker", "start", "photoprism"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"status": "started"}
        except subprocess.CalledProcessError:
            # Container doesn't exist, create and run it
            try:
                subprocess.run([
                    "docker", "run", "-d",
                    "--name", "photoprism",
                    "--security-opt", "seccomp=unconfined",
                    "--security-opt", "apparmor=unconfined",
                    "-p", "8020:2342",
                    "-e", "PHOTOPRISM_UPLOAD_NSFW=true",
                    "-e", "PHOTOPRISM_ADMIN_PASSWORD=teamsmiley",
                    "-v", "/opt/photoprism/data:/photoprism/storage",
                    "-v", "/opt/photoprism/originals:/photoprism/originals",
                    "photoprism/photoprism:latest"
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return {"status": "started"}
            except subprocess.CalledProcessError as e:
                return {"status": "error", "message": "Failed to start photoprism container"}
    
    else:
        # This shouldn't happen due to @check_service_name decorator, but handle gracefully
        return {"status": "error", "message": f"Unknown service: {service_name}"}

@check_service_name
def service_help(service_name: str):
    return {"help": SERVICES[service_name]["help"]}