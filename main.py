import time
import argparse
from loguru import logger

from src.scraper.base import BaseScraper

parser = argparse.ArgumentParser(description="Yelp Crawler")
parser.add_argument(
    "--category", type=str, required=True, help='Category name (e.g., "contractors")'
)
parser.add_argument(
    "--location", type=str, required=True, help='Location (e.g., "San Francisco, CA")'
)
parser.add_argument(
    "--amount_of_businesses",
    type=int,
    default=100,
    help="Amount of businesses by category (default: 100)",
)


URL = "https://www.yelp.com/"


def main():
    args = parser.parse_args()
    category = args.category
    location = args.location
    amount_businesses = args.amount_of_businesses

    start_point = time.perf_counter()
    logger.debug("Start script")

    BaseScraper(
        url=URL, category=category, location=location, business_limit=amount_businesses
    ).run()

    end_point = time.perf_counter()
    lead_time = end_point - start_point

    logger.info(f"Finish script. Lead time: {lead_time}")


if __name__ == "__main__":
    main()
