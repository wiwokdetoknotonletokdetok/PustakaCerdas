import os

from dotenv import load_dotenv

from pustakacerdas import create_app

load_dotenv()

app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "yes")
    app.run(debug=debug_mode)
