from typing import List, Dict
from functools import cached_property


from .base import BaseAPI
from src.schemas import BusinessesListSchema


class BusinessAPI(BaseAPI):
    def __init__(self, url: str, location: str, category: str, business_limit: int):
        super().__init__(url, location)
        self._category = category
        self._b_limit = business_limit
        self.offset = 0

    @property
    def _url_builder(self):
        return f"{self._url}/search/snippet?"

    @cached_property
    def params(self):
        """Params of request"""
        return {
            "find_desc": self._category,
            "find_loc": self._location,
            "start": self.offset,
            "parent_request": "",
            "ns": 1,
            "request_origin": "user",
        }

    @cached_property
    def get_business_list(self) -> List[Dict]:
        """
        Main method for get businesses data
        :return: valid and transform data
        """
        try:
            while True:
                response = self.request
                clear_data = [
                    item
                    for item in response.json()["searchPageProps"][
                        "mainContentComponentsListProps"
                    ]
                    if "bizId" in item.keys()
                ]
                schema_data = BusinessesListSchema(main_content=clear_data)

                yield schema_data.get_page_data

                if not schema_data or self.offset <= self._b_limit:
                    break

                self.offset += 10
                self.logger.info(f"Request business with {self.offset} offset.")

        except Exception as e:
            raise e
