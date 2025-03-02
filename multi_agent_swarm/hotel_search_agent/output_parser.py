from pydantic import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser


class HotelSearchResults(BaseModel):
    hotel_name: str = Field(description="The name of the hotel")
    hotel_location: str = Field(description="The location of the hotel")
    hotel_distance_from_airport: str = Field(
        description="The distance of the hotel from the airport"
    )
    hotel_price: str = Field(description="The price of the hotel")
    hotel_rating: str = Field(description="The rating of the hotel")
    hotel_reviews: str = Field(description="The reviews of the hotel")


class HotelSearchOutputParser(PydanticOutputParser[HotelSearchResults]):
    """Parser for hotel search results."""

    def __init__(self):
        super().__init__(pydantic_object=[HotelSearchResults])

    @property
    def _type(self) -> str:
        return "hotel_search_results"

    def get_format_instructions(self) -> str:
        """Return the formatted output instructions."""
        return """Return the hotel search results in the following format:
                [
                    {
                        "hotel_name": "Hotel Name",
                        "hotel_location": "Hotel Location",
                        "hotel_distance_from_airport": "Hotel Distance from Airport",
                        "hotel_price": "Hotel Price",
                        "hotel_rating": "Hotel Rating",
                        "hotel_reviews": "Hotel Reviews"
                    }
                ]
        """

    def parse(self, text: str) -> List[HotelSearchResults]:
        """
        Parse the text into a list of HotelSearchResults objects.
        Args:
            text: The text to parse.
        Returns:
            A list of HotelSearchResults objects.
        """
        try:
            return super().parse(text)
        except Exception as e:
            raise ValueError(f"Failed to parse the text: {text}. Error: {e}")


hotel_output_parser = HotelSearchOutputParser()

__all__ = [hotel_output_parser]
