import re
import urllib.parse
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class BizDataSchema(BaseModel):
    name: str | None
    rating: float | None
    website: str | None
    review_count: int | None = Field(default=None, alias="reviewCount")
    yelp_url: str | None = Field(default=None, alias="businessUrl")

    @field_validator("website", "yelp_url", mode="before")
    def parse_biz_url(cls, value: str) -> str | None:
        """Validator need for scrape url from str"""
        if value:
            if isinstance(value, dict) and "href" in value:
                value = value["href"]

            match = re.search(r"redirect_url=([^&]+)", value)
            if match:
                # Extract the matched part
                encoded_url = match.group(1)
                first_decoded_url = urllib.parse.unquote(encoded_url)
                url_match = re.search(r"url=([^&]+)", first_decoded_url)

                if url_match:
                    # Decode the URL-encoded actual URL found in the 'url' parameter
                    second_decoded_url = urllib.parse.unquote(url_match.group(1))
                    value = second_decoded_url
                else:
                    # Return the first decoding result
                    value = first_decoded_url
            return value
        return None


class MainContentSchema(BaseModel):
    biz_id: str | None = Field(default=None, alias="bizId")
    result: BizDataSchema = Field(..., alias="searchResultBusiness")

    @property
    def business_data(self):
        return {
            self.biz_id: {
                "Business name": self.result.name,
                "Business rating": self.result.rating,
                "Number of reviews": self.result.review_count,
                "Business yelp url": self.result.yelp_url,
                "Business website": self.result.website,
            }
        }


class BusinessesListSchema(BaseModel):
    main_content: Optional[List[MainContentSchema]]

    @property
    def get_page_data(self):
        return [{**item.business_data} for item in self.main_content]
