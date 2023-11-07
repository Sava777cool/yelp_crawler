from loguru import logger
from abc import abstractmethod
from requests import request, Response
from functools import cached_property
from fake_useragent import UserAgent


class BaseAPI:
    """Base class for make request to resource"""

    _user_agent: UserAgent = UserAgent().random

    def __init__(self, url: str, location: str):
        self._url = url
        self._location = location
        self.logger = logger.bind(class_name=self.__class__.__name__)

    @property
    def _url_builder(self):
        """Property need for adapt base url"""
        return self._url

    @property
    @abstractmethod
    def params(self):
        """Params of request"""
        pass

    @cached_property
    def request(self) -> Response:
        """Main method for request with params"""
        try:
            response = request(
                method="GET",
                url=self._url_builder,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": self._user_agent,
                },
                params=self.params,
            )
            self.logger.info(f"Request to {self._url_builder} success.")

        except Exception:
            self.logger.error(f"Something wrong: {response.text}")

        return response
