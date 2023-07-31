import logging
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    token = os.getenv('BOT_TOKEN')


@dataclass
class ProxyConfig:
    proxy_url_1 = f'https://{os.getenv("PROXY_LOGIN")}:{os.getenv("PROXY_PASS")}@{os.getenv("PROXY_IP1")}'
    proxy_url_2 = f'https://{os.getenv("PROXY_LOGIN")}:{os.getenv("PROXY_PASS")}@{os.getenv("PROXY_IP2")}'
    proxy_url_3 = f'https://{os.getenv("PROXY_LOGIN")}:{os.getenv("PROXY_PASS")}@{os.getenv("PROXY_IP3")}'


@dataclass
class Config:
    logging_level: int = int(os.getenv('LOGGING_LEVEL', logging.INFO))
    debug: bool = bool(os.getenv('DEBUG'))

    proxy: ProxyConfig = ProxyConfig()
    bot: BotConfig = BotConfig()


conf = Config()
