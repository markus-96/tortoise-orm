import asyncio
from decimal import Decimal

from tests.testmodels import Event, BenchmarkFewFields, DecimalFields
from tortoise.expressions import F
from tortoise.functions import Count


def test_function_count(benchmark, few_fields_benchmark_dataset):
    loop = asyncio.get_event_loop()

    @benchmark
    def bench():
        async def _bench():
            await BenchmarkFewFields.annotate(text_count=Count("text")).all()

        loop.run_until_complete(_bench())


def test_values_related_m2m(benchmark, create_team_with_participants):
    loop = asyncio.get_event_loop()

    @benchmark
    def bench():
        async def _bench():
            await Event.filter(name="Test").values("name", "participants__name")

        loop.run_until_complete(_bench())


def test_filter_decimal(benchmark, create_decimals):
    loop = asyncio.get_event_loop()

    @benchmark
    def bench():
        async def _bench():
            await DecimalFields.annotate(d=F("decimal")).filter(d=Decimal("1.2346")).first()

        loop.run_until_complete(_bench())
