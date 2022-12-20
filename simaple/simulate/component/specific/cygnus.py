from simaple.simulate.component.base import reducer_method, view_method
from simaple.simulate.component.skill import SkillComponent
from simaple.simulate.component.state import CooldownState, DelayedLimitedIntervalState
from simaple.simulate.component.trait.impl import CooldownValidityTrait, DelayedLimitedTickEmittingTrait
from simaple.simulate.component.view import Running, Validity
from simaple.simulate.global_property import Dynamics


class CygnusPhalanx(SkillComponent, DelayedLimitedTickEmittingTrait, CooldownValidityTrait):
    name: str
    cooldown: float
    delay: float

    tick_initial_delay: float
    tick_interval: float
    tick_damage: float
    tick_hit: float
    tick_count_max: float
    duration: float

    def get_default_state(self):
        return {
            "cooldown_state": CooldownState(time_left=0),
            "delayed_limited_interval_state": DelayedLimitedIntervalState(
                interval=self.tick_interval,
                time_left=0,
                maximum_count=self.tick_count_max
            ),
        }

    @reducer_method
    def elapse(
        self,
        time: float,
        cooldown_state: CooldownState,
        delayed_limited_interval_state: DelayedLimitedIntervalState
    ):
        (
            cooldown_state, delayed_limited_interval_state
        ), events = self.elapse_tick_emitting_trait(
            time, cooldown_state, delayed_limited_interval_state
        )

        return (cooldown_state, delayed_limited_interval_state), events

    @reducer_method
    def use(
        self,
        _: None,
        cooldown_state: CooldownState,
        delayed_limited_interval_state: DelayedLimitedIntervalState,
        dynamics: Dynamics,
    ):
        (
            cooldown_state, delayed_limited_interval_state, dynamics,
        ), events = self.use_tick_emitting_trait(
            cooldown_state, delayed_limited_interval_state, dynamics
        )

        return (cooldown_state, delayed_limited_interval_state, dynamics), events

    @view_method
    def validity(self, cooldown_state):
        return self.invalidate_if_disabled(
            Validity(
                name=self.name,
                time_left=max(0, cooldown_state.time_left),
                valid=cooldown_state.available,
            )
        )

    @view_method
    def running(self, delayed_limited_interval_state: DelayedLimitedIntervalState) -> Running:
        return Running(name=self.name, time_left=delayed_limited_interval_state.interval_time_left)

    def _get_delay(self) -> float:
        return self.delay

    def _get_initial_delay(self) -> float:
        return self.tick_initial_delay

    def _get_duration(self) -> float:
        return self.duration

    def _get_tick_damage_hit(self) -> tuple[float, float]:
        return self.tick_damage, self.tick_hit