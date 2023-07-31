from dataclasses import dataclass

from fake_useragent import UserAgent


class CreateUA:
    def __init__(self, ua: UserAgent):
        self.ua = ua

    def get_ua(self) -> UserAgent:
        return self.ua.random


@dataclass
class Headers:
    ua: CreateUA = CreateUA(ua=None or UserAgent())

    def create_headers(self) -> dict[str, UserAgent | str]:
        headers_dict = {
            'User-Agent': self.ua.get_ua()
        }

        return headers_dict


headers = Headers()
