import json
from loguru import logger
from bs4 import BeautifulSoup
from typing import List, Dict
from functools import cached_property


from src.api import MainPageAPI, BusinessAPI, ReviewsAPI


class WrongCategoryException(Exception):
    def __init__(self, message="There is no category in list", *args):
        super().__init__(message, *args)


class BaseScraper:
    def __init__(self, url: str, category: str, location: str, business_limit: int):
        self._url = url
        self._category = category
        self._location = location
        self._business_limit = business_limit
        self.logger = logger.bind(class_name=self.__class__.__name__)

    @cached_property
    def _get_categories_list(self) -> List:
        """
        Method scrape category from main page
        :return: list, [category1, category2, ...]
        """
        try:
            main_page_response = MainPageAPI(
                url=self._url, location="San Francisco, CA"
            ).request

            parsed_page = BeautifulSoup(main_page_response.text, "html.parser")

            elements = parsed_page.select(
                "nav[aria-label='Business categories'] a[href*='find_desc']"
            )
            categories_list = [element.text for element in elements]
            self.logger.info(
                f"Find {len(categories_list)} categories on page {self._url}."
            )
        except Exception as e:
            raise e
        return categories_list

    @cached_property
    def _get_businesses_list(self) -> List[Dict]:
        """
        Method get business list from XHR request and validation in pydantic schema
        :return: list[dict] -> [{biz_name1: name}, {biz_name2: name}, ...]
        """
        try:
            businesses_response = BusinessAPI(
                url=self._url,
                category=self._category,
                location=self._location,
                business_limit=self._business_limit,
            )
            businesses_list = [
                data for item in businesses_response.get_business_list for data in item
            ]
            self.logger.info(
                f"Total find {len(businesses_list)} businesses in category: {self._category}"
            )
        except Exception as e:
            raise e
        return businesses_list

    def _get_review_list(self, biz_id: str) -> List[Dict]:
        """
        Method for get review list by biz_id, data takes from XHR request
        :param biz_id: str, need for request
        :return: list[dict] -> [review1, review2, ...]
        """
        try:
            review_response = ReviewsAPI(
                url=self._url, location=self._location, business_id=biz_id
            )
        except Exception as e:
            raise e
        return review_response.get_reviews_list

    def _save_json_file(self, data: List[Dict]) -> None:
        file_name = f"{self._category.lower()}_data.json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            self.logger.info(f'Data to file: {file_name} successful save.')

    def run(self):
        """
        Main method for run scrape logic
        :return: None
        """
        categories_list = self._get_categories_list

        # Check if there is category in list
        if categories_list and self._category in categories_list:
            scrape_data = []
            business_list = self._get_businesses_list

            # Check if there business list
            if business_list:
                # Scrape reviews for each business by business_id
                for item in business_list:
                    biz_id = list(item.keys())[0]
                    review_list = self._get_review_list(biz_id=biz_id)
                    # Add all scrape data to list
                    scrape_data.append({**item[biz_id], "Reviews list": review_list})
            self._save_json_file(data=scrape_data)
        else:
            self.logger.warning(f"There is no {self._category} in list")
            self.logger.warning(f"Please choose one from: {categories_list}")
