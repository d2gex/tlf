from src.config import Config


class TestingConfig(Config):
    # For testing CSRF token must be disabled. SECRET KEY must still appear though
    WTF_CSRF_ENABLED = False