from functools import cached_property

from .base import BaseAPI


class MainPageAPI(BaseAPI):
    @cached_property
    def get_main_page_data(self) -> str:
        """
        Method for get data from main page
        :return: html page
        """
        try:
            response = self.request
            self.logger.info("Data from main page get successful")
        except Exception as e:
            raise e

        return response.text
