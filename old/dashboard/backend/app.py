from argparse import ArgumentParser
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.services import list_services, service_status, restart_service, stop_service, start_service, service_help, ServiceNotFoundError
import logging

app = FastAPI()

# Allow all origins (for development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/services/list")
async def route_list_services():
    """
    List all available services.
    """
    return list_services()

@app.get("/services/{service_name}/status")
async def route_service_status(service_name: str):
    """
    Get the status of a specific service.
    """
    try:
        return service_status(service_name)
    except ServiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/services/{service_name}/logs")
async def route_service_logs(service_name: str):
    """
    Get the logs of a specific service.
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.get("/services/{service_name}/help")
async def route_service_help(service_name: str):
    """
    Get help information for a specific service.
    """
    try:
        return service_help(service_name)
    except ServiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/services/{service_name}/restart")
async def route_restart_service(service_name: str):
    """
    Restart a specific service.
    """
    try:
        return restart_service(service_name)
    except ServiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/services/{service_name}/stop")
async def route_stop_service(service_name: str):
    """
    Stop a specific service.
    """
    try:
        return stop_service(service_name)
    except ServiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/services/{service_name}/start")
async def route_start_service(service_name: str):
    """
    Start a specific service.
    """
    try:
        return start_service(service_name)
    except ServiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/services/{service_name}/config")
async def route_service_config(service_name: str):
    """
    Get the configuration of a specific service.
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.get("/services/{service_name}/config/update")
async def route_update_service_config(service_name: str):
    """
    Update the configuration of a specific service.
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")




def run():
    parser = ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port to run the server on")
    parser.add_argument("-d", "--debug", action="store_true", help="Run the server in debug mode")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f"Starting server on port {args.port} with debug mode {'on' if args.debug else 'off'}")

    print("not implemented yet")

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    run()
