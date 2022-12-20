import pydantic

from simaple.core.base import Stat
from simaple.simulate.base import State
from simaple.simulate.component.base import Component, reducer_method, view_method
from simaple.simulate.component.state import IntegerState, IntervalState
from simaple.simulate.component.view import Running, Validity
from simaple.simulate.global_property import Dynamics


class ChargeableStackState(State):
    stack: int
    elapsed_time_after_latest_charge: float
    max_stack: int = pydantic.Field(allow_mutation=False)
    charge_interval: float = pydantic.Field(allow_mutation=False)

    class Config:
        validate_assignment = True

    def elapse(self, time: float):
        if self.stack == self.max_stack:
            return

        self.elapsed_time_after_latest_charge += time

        while self.elapsed_time_after_latest_charge >= self.charge_interval:
            self.stack += 1
            self.elapsed_time_after_latest_charge -= self.charge_interval
            if self.stack == self.max_stack:
                self.elapsed_time_after_latest_charge = 0
                return

    def has_enough_stack(self, amount: int) -> bool:
        return amount <= self.stack

    def use_charge(self, amount: int) -> bool:
        if not self.has_enough_stack(amount):
            return False

        self.stack -= amount
        return True

    def get_time_left(self) -> float:
        return self.charge_interval - self.elapsed_time_after_latest_charge


class ChargeableStackDependentTickDamageSkillComponent(Component):
    """Component for howling Gale"""

    name: str
    delay: float

    max_stack: int
    charge_interval: float

    duration: float
    tick_interval: float
    tick_damage: list[float]
    tick_hit: list[float]

    def get_default_state(self):
        return {
            "stack_state": ChargeableStackState(
                max_stack=self.max_stack,
                charge_interval=self.charge_interval,
                stack=self.max_stack,
                elapsed_time_after_latest_charge=0,
            ),
            "interval_state": IntervalState(interval=self.tick_interval, time_left=0),
            "current_used_stack": IntegerState(value=0),
        }

    @reducer_method
    def use(
        self,
        amount: int,
        stack_state: ChargeableStackState,
        interval_state: IntervalState,
        current_used_stack: IntegerState,
    ):
        if not stack_state.has_enough_stack(amount):
            return (
                stack_state,
                interval_state,
                current_used_stack,
            ), self.event_provider.rejected()

        stack_state = stack_state.copy()
        interval_state = interval_state.copy()
        current_used_stack = current_used_stack.copy()

        stack_state.use_charge(amount)
        interval_state.set_time_left(self.duration)
        current_used_stack.set_value(amount)

        return (stack_state, interval_state, current_used_stack), [
            self.event_provider.dealt(0, 0),
            self.event_provider.delayed(self.delay),
        ]

    @reducer_method
    def elapse(
        self,
        time: float,
        stack_state: ChargeableStackState,
        interval_state: IntervalState,
        current_used_stack: IntegerState,
    ):
        stack_state = stack_state.copy()
        interval_state = interval_state.copy()

        stack_state.elapse(time)
        lapse_count = 0
        for _ in interval_state.resolving(time):
            lapse_count += 1

        return (stack_state, interval_state, current_used_stack), [
            self.event_provider.elapsed(time)
        ] + [
            self.event_provider.dealt(
                self.tick_damage[current_used_stack.value - 1],
                self.tick_hit[current_used_stack.value - 1],
            )
            for _ in range(lapse_count)
        ]

    @view_method
    def validity(self, stack_state):
        return Validity(
            name=self.name,
            valid=stack_state.has_enough_stack(1),
            time_left=stack_state.get_time_left(),
        )

    @view_method
    def running(self, interval_state: IntervalState) -> Running:
        return Running(name=self.name, time_left=interval_state.interval_time_left)

    @view_method
    def stack(self, stack_state):
        return stack_state.stack
