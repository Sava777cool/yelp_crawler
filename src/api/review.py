from typing import List, Dict
from functools import cached_property


from .base import BaseAPI
from src.schemas import ReviewsList


class ReviewsAPI(BaseAPI):
    def __init__(self, url: str, location: str, business_id: str):
        super().__init__(url, location)
        self._business_id = business_id
        self.offset = 5

    @property
    def _url_builder(self):
        return f"{self._url}/biz/{self._business_id}/review_feed"

    @cached_property
    def params(self):
        return {
            "rl": "en&q",
            "sort_by": "relevance_desc",
            "start": 5,
        }

    @cached_property
    def get_reviews_list(self) -> List[Dict]:
        """
        Method for get reviews data, limit 5 reviews.
        :return: list[dict], [review1, review2, ...]
        """
        try:
            response = self.request
            schema_data = ReviewsList(**response.json())
        except Exception as e:
            raise e

        return schema_data.review_data[:5]
