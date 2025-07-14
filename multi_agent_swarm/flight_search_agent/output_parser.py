from pydantic import BaseModel, Field
import re
from typing import Optional, List
from langchain.output_parsers import PydanticOutputParser

class FlightSearchResults(BaseModel):
    source: str = Field(description="The source where flight will be departing from")
    destination: str = Field(description="The destination where flight will be arriving to")
    departure_date: str = Field(description="The date of departure")
    departure_time: str = Field(description="The time of departure")
    arrival_date: str = Field(description="The date of arrival")
    arrival_time: str = Field(description="The time of arrival")
    layover: str = Field(description="The layover time")
    layover_time: str = Field(description="The layover time")

class FlightSearchOutputParser(PydanticOutputParser[FlightSearchResults]):
    """Parser for flight search results."""
    def __init__(self):
        super().__init__(pydantic_object=[FlightSearchResults])

    @property
    def _type(self) -> str:
        return "flight_search_results"

    def get_format_instructions(self) -> str:
        """Return the formatted output instructions."""
        return """Return the flight search results in the following format:
                [
                    {
                        "source": "string",
                        "destination": "string",
                        "departure_date": "string",
                        "departure_time": "string",
                        "arrival_date": "string",
                        "arrival_time": "string",
                        "layover": "string",
                        "layover_time": "string"
                    }
                ]
        """

    def parse(self, text: str) -> List[FlightSearchResults]:
        """
            Parse the text into a list of FlightSearchResults objects.
            Args:
                text: The text to parse.
            Returns:
                A list of FlightSearchResults objects.
        """
        try:
            return super().parse(text)
        except Exception as e:
            raise ValueError(f"Failed to parse the text: {text}. Error: {e}")


flight_output_parser = FlightSearchOutputParser()

__all__ = [
    flight_output_parser
]

