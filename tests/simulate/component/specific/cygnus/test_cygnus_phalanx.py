import pytest

from simaple.simulate.component.specific.cygnus import CygnusPhalanx
from simaple.simulate.reserved_names import Tag


@pytest.fixture(name="cygnus_phalanx")
def fixture_cygnus_phalanx(bare_store):
    component = CygnusPhalanx(
        name="test-cygnus-phalanx",
        cooldown=30_000,
        delay=600,
        tick_initial_delay=600,
        tick_interval=120,
        tick_damage=810,
        tick_hit=1,
        tick_count_max=60,
        duration=20_000,
    )
    return component.compile(bare_store)


def test_cygnus_phalanx_delay_smaller_time(cygnus_phalanx):
    cygnus_phalanx.use(None)
    events = cygnus_phalanx.elapse(500)

    dealing_event = [e for e in events if e.tag == Tag.DAMAGE]
    assert len(dealing_event) == 0
    assert cygnus_phalanx.delayed_limited_interval_state.delay == 100


def test_cygnus_phalanx_delay_tick(cygnus_phalanx):
    cygnus_phalanx.use(None)
    events = cygnus_phalanx.elapse(1_000)

    dealing_event = [e for e in events if e.tag == Tag.DAMAGE]
    assert len(dealing_event) == 3


def test_cygnus_phalanx_max_tick(cygnus_phalanx):
    cygnus_phalanx.use(None)
    events = cygnus_phalanx.elapse(23_000)

    dealing_event = [e for e in events if e.tag == Tag.DAMAGE]
    assert len(dealing_event) == 60
