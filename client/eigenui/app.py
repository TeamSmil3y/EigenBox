from argparse import ArgumentParser
from pathlib import Path
from eigen import Eigen

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "eigen/config.toml"

def main():
    parser = ArgumentParser(description="Eigen CLI Tool")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to the Eigen configuration file (default: config.toml in the eigen directory)",
    )
    args = parser.parse_args()

    eigen = Eigen(config_path=args.config)


if __name__ == "__main__":
    main()
