from pathlib import Path
import sys
from streamlit.web.cli import main as stcli_main

STREAMLIT_APP = Path(__file__).parent / "app.py"

def main():
    sys.argv = ["streamlit", "run", str(STREAMLIT_APP)] + sys.argv[1:]
    sys.exit(stcli_main())


if __name__ == "__main__":
    main()
