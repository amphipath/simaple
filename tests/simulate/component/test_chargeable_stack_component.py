# pylint: disable=W0621
import pytest

from simaple.simulate.component.chargeable import (
    ChargableStackDependentTickDamageSkillComponent,
)
from simaple.simulate.reserved_names import Tag


@pytest.fixture
def chargable_stack_component():
    return ChargableStackDependentTickDamageSkillComponent(
        name="test-chargable-stack",
        delay=300,
        max_stack=3,
        charge_interval=20_000,
        duration=10_000,
        tick_interval=1_000,
        tick_damage=[50, 100, 130],
        tick_hit=[3, 4, 5],
    )


@pytest.fixture
def compiled_chargable_stack_component(chargable_stack_component, bare_store):
    return chargable_stack_component.compile(bare_store)


def test_initial_chargable_stack_is_full(compiled_chargable_stack_component):
    assert compiled_chargable_stack_component.stack() == 3


def test_initial_chargable_stack_is_consumed(compiled_chargable_stack_component):
    for idx in range(3):
        event = compiled_chargable_stack_component.use(1)
        assert event[0].tag != Tag.REJECT


@pytest.mark.parametrize("stack, damage, hit", [(1, 50, 3), (2, 100, 4), (3, 130, 5)])
def test_chargable_with_various_stack(
    compiled_chargable_stack_component, stack, damage, hit
):
    compiled_chargable_stack_component.use(stack)
    events = compiled_chargable_stack_component.elapse(5_000)
    dealing_count = sum([e.tag == Tag.DAMAGE for e in events])

    assert dealing_count == 5
    for e in events:
        if e.tag == Tag.DAMAGE:
            assert e.payload == {"damage": damage, "hit": hit}

    events = compiled_chargable_stack_component.elapse(10_000)
    dealing_count = sum([e.tag == Tag.DAMAGE for e in events])

    assert dealing_count == 5
