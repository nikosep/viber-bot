import os


class Config:
    # Viber Bot Configuration
    VIBER_BOT_NAME = os.getenv('VIBER_BOT_NAME')
    VIBER_TOKEN = os.getenv('VIBER_TOKEN')

    # OpenAI API Key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Directory for persistent data
    PERSIST_DIR = "reviews_hotels3"
