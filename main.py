from src.app.app import app
from src.core.config import Settings

if __name__ == "__main__":
    settings = Settings()
    app(settings.ORIGINAL + settings.ORIGINAL_IMAGES[2])