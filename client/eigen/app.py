from argparse import ArgumentParser
from pathlib import Path
from . import load_config
import logging

DEFAULT_CONFIG_PATH = Path(__file__).parent / "config.toml"

def main():
    parser = ArgumentParser()
    #parser.add_argument("--host", type=str, default="localhost", help="Host to run the server on")
    #parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("command", type=str, help="Command to run")
    parser.add_argument("args", nargs="*", help="Arguments for the command")
    parser.add_argument("--config", type=str, default=DEFAULT_CONFIG_PATH, help="Path to the configuration file")
    args = parser.parse_args()

    load_config(args.config)

    match args.command:
        case "list":
            # Placeholder for listing all services
            logging.info("Listing all services...")

    if len(args.args) == 0:
        logging.error("No service slug provided. Please provide a service slug as an argument.")
        return

    match(args.command):
        case "start":
            # Placeholder for starting the service
            slug = args.args[0]
            logging.info("Starting the service...")
        case "stop":
            # Placeholder for stopping the service
            slug = args.args[0]
            logging.info("Stopping the service...")
        case "restart":
            # Placeholder for restarting the service
            slug = args.args[0]
            logging.info("Restarting the service...")
        case "status":
            # Placeholder for checking the status of the service
            slug = args.args[0]
            logging.info("Checking the status of the service...")
        case _:
            logging.error(f"Unknown command: {args.command}")
            return


    logging.warning("This is a placeholder for the startup logic.")

if __name__ == "__main__":
    main()
