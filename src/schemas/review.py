from typing import List, Dict
from pydantic import BaseModel, Field


class UserDataScheme(BaseModel):
    reviewer_name: str = Field(..., alias="markupDisplayName")
    reviewer_location: str = Field(..., alias="displayLocation")


class ReviewSchema(BaseModel):
    user: UserDataScheme
    reviewer_location: str = Field(..., alias="localizedDate")


class ReviewsList(BaseModel):
    reviews: List[ReviewSchema]

    @property
    def review_data(self) -> List[Dict]:
        return [
            {
                "Reviewer name": review.user.reviewer_name,
                "Reviewer location": review.user.reviewer_location,
                "Review date": review.reviewer_location,
            }
            for review in self.reviews
        ]
