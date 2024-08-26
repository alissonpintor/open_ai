import dotenv
import openai


class ChatGPTClient:
    _instance: openai.Client = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            dotenv.load_dotenv()
            cls._instance = openai.Client()
        return cls._instance
