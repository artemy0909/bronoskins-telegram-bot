import logging


class StateError(BaseException):
    pass


class StateGroup:
    def __init__(self, caption: str, on_finish_state, on_return_state=None):
        if not isinstance(on_finish_state, State):
            raise TypeError
        self._on_finish_state = on_finish_state
        if on_return_state is not None and not isinstance(on_return_state, State):
            raise TypeError
        self._on_return_state = on_return_state
        self._caption = caption
        self._states = []

    def __str__(self):
        return self._caption

    @property
    def on_finish_state(self):
        return self._on_finish_state

    @property
    def on_return_state(self):
        return self._on_return_state

    def add_state(self, state):
        if not isinstance(state, State):
            raise TypeError
        if state.group is not self:
            state.group = self
        self._states.append(state)

    def start(self):
        try:
            return self._states[0]
        except IndexError:
            raise StateError("States undefined")

    def next_state(self, current_state):
        try:
            return self._states[self._states.index(current_state) + 1]
        except IndexError:
            raise StateError("Next state undefined")

    def prev_state(self, current_state):
        if self._states.index(current_state) - 1 < 0:
            raise StateError("Prev state undefined")
        try:
            return self._states[self._states.index(current_state) - 1]
        except IndexError:
            raise StateError("Prev state undefined")

    def is_my_state(self, state):
        return state in self._states


class State:
    def __init__(self, caption: str = "not configured", group: StateGroup = None, button_text: str = ""):
        self._caption = caption
        self._button_text = button_text
        if not group:
            self._group = StateGroup("not configured", self)
        elif not isinstance(group, StateGroup):
            raise TypeError
        else:
            self._group = group
        self._group.add_state(self)

    def __str__(self):
        return self._caption

    @property
    def group(self) -> StateGroup:
        return self._group

    @group.setter
    def group(self, value):
        if not isinstance(value, StateGroup):
            raise TypeError
        self._group = value
        if not self._group.is_my_state(self):
            self._group.add_state(self)

    @property
    def back_button(self):
        return "⏪ Вернуться" if not self._button_text else f"⏪ Вернуться к {self._button_text}"

    @property
    def next_state(self):
        return self._group.next_state(self)

    @property
    def prev_state(self):
        return self._group.prev_state(self)


DEFAULT_STATE = State("default")


class StateMachine:
    def __init__(self):
        self._current_state = DEFAULT_STATE

    def _log_debug_state(self):
        logging.debug(f"current state is '{self._current_state}'")

    @property
    def current_state(self):
        return self._current_state

    def prev(self):
        if self._current_state.group.on_return_state:
            try:
                self._current_state = self._current_state.prev_state
            except StateError:
                self._current_state = self._current_state.group.on_return_state
        else:
            self._current_state = self._current_state.prev_state
        self._log_debug_state()

    def next(self):
        self._current_state = self._current_state.next_state
        self._log_debug_state()

    def finish(self):
        if self._current_state.group.on_finish_state is None:
            raise StateError("Finish state not configured")
        self._current_state = self._current_state.group.on_finish_state
        self._log_debug_state()

    def jump(self, state_group: StateGroup):
        if isinstance(state_group, StateGroup):
            self._current_state = state_group.start()
        else:
            raise ValueError
        self._log_debug_state()

    def set(self, state: State):
        if isinstance(state, State):
            self._current_state = state
        else:
            raise ValueError
        self._log_debug_state()
