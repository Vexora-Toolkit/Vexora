import pytest
from pydantic import BaseModel, Field

import vexora


class Location(BaseModel):
    city: str = Field(
        description="The city's proper name. For New York City, use 'New York'"
    )
    state: str = Field(description="2-letter abbreviation")


class TestBuiltins:
    def test_extract_numbers(self):
        result = vexora.extract("one, two, three", int)
        assert result == [1, 2, 3]

    @pytest.mark.usefixtures("gpt_4o")
    def test_extract_complex_numbers(self):
        """Uses gpt-4o to avoid flaky behavior"""
        result = vexora.extract(
            "I paid $10 for 3 coffees and they gave me back a dollar 25 cents",
            float,
        )
        assert result == [10.0, 3.0, 1.25]

    @pytest.mark.usefixtures("gpt_4o")
    def test_extract_complex_numbers_all(self):
        """Uses gpt-4o to avoid flaky behavior"""
        result = vexora.extract(
            "I paid $10 for 3 coffees and they gave me back a dollar and 25 cents",
            float,
            instructions="include all numbers",
        )

        assert result == [10.0, 3.0, 1, 25]

    def test_extract_money(self):
        result = vexora.extract(
            "I paid $10 for 3 coffees and they gave me back a dollar 25 cents",
            float,
            instructions="extract monetary values only. $3.50 is 3.5",
        )
        assert result == [10.0, 1.25]

    def test_extract_names(self):
        result = vexora.extract(
            "My name is John, my friend's name is Mary, and my other friend's name"
            " is Bob",
            str,
            instructions="names",
        )
        assert result == ["John", "Mary", "Bob"]

    @pytest.mark.flaky(max_runs=3)
    def test_float_to_int(self):
        result = vexora.extract("the numbers are 1, 2, and 3.2", int)
        assert result == [1, 2, 3]


class TestInstructions:
    def test_city_and_state(self):
        result = vexora.extract(
            "I live in the big apple",
            str,
            instructions="formal city name, state abbreviation - properly capitalized",
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] in ["New York, NY", "New York City, NY"]


class TestPydantic:
    def test_extract_location(self):
        result = vexora.extract("I live in New York, NY", Location)
        assert result == [Location(city="New York", state="NY")]

    def test_extract_multiple_locations(self):
        result = vexora.extract(
            "I live in New York, NY and work in San Francisco, CA",
            Location,
        )
        assert result == [
            Location(city="New York", state="NY"),
            Location(city="San Francisco", state="CA"),
        ]

    def test_extract_multiple_locations_by_nickname(self):
        result = vexora.extract("I live in the big apple and work in SF", Location)
        assert result == [
            Location(city="New York", state="NY"),
            Location(city="San Francisco", state="CA"),
        ]

    @pytest.mark.xfail(reason="tuples aren't working right now")
    def test_extract_complex_pattern(self):
        result = vexora.extract(
            "John lives in Boston, Mary lives in NYC, and I live in SF",
            tuple[str, Location],
            instructions="pair names and locations",
        )
        assert result == []


class TestAsync:
    async def test_extract_numbers(self):
        result = await vexora.extract_async("one, two, three", int)
        assert result == [1, 2, 3]
