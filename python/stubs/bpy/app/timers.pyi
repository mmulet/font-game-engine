from typing import Callable

TimerInputType = Callable[[], float | None]


def register(timer: TimerInputType) -> None: ...


def unregister(timer: TimerInputType) -> None: ...


def is_registered(timer: TimerInputType) -> bool: ...
