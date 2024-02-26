import json
import logging
import typing

import config
from utils import rights
from utils.database import Login, Stuff, CallbackData
from utils.state_machine import StateMachine


class User:
    def __init__(self, data_base_item: Stuff):
        self._database_item = data_base_item
        self._state = StateMachine()
        self._dialog_temp_data = {}
        self._button_data = {}

    @property
    def im(self):
        return self._database_item

    @property
    def id(self):
        return self._database_item.id

    @property
    def name(self):
        return self._database_item.name

    @property
    def surname(self):
        return self._database_item.surname

    @property
    def right_level(self):
        return self._database_item.right_level

    @property
    def state(self) -> StateMachine:
        return self._state

    @state.setter
    def state(self, value):
        if isinstance(value, StateMachine):
            self._state = value
        else:
            raise TypeError

    def __setitem__(self, key, value):
        self._dialog_temp_data[key] = value
        if config.DEBUG:
            logging.debug(f"arg set '{key}'={value}")

    def __getitem__(self, key):
        return None if key not in self._dialog_temp_data else self._dialog_temp_data[key]

    def __contains__(self, item):
        return item in self._dialog_temp_data

    def __delitem__(self, key):
        if key in self._dialog_temp_data:
            del self._dialog_temp_data[key]
        if config.DEBUG:
            logging.debug(f"arg del '{key}'")

    def set_data(self, **kwargs):
        for k, v in kwargs.items():
            self._dialog_temp_data[k] = v
            if config.DEBUG:
                logging.debug(f"arg set '{k}'={v}")

    def del_all_dialog_data(self, *exceptions):
        if exceptions:
            for key in self._dialog_temp_data.keys():
                if key not in exceptions:
                    del self._dialog_temp_data[key]
        else:
            self._dialog_temp_data = {}

    def load_args_from_callback(self, key):
        self._dialog_temp_data.update(json.loads(CallbackData.get(worker=self.im, key=key).data))

    def check_access(self, *right_levels):
        return self.right_level in right_levels

    def is_admin(self):
        return self.check_access(*rights.ACCESS_FOR_ADMINS)


def load_user_dict() -> typing.Dict[int, User]:
    result = {}
    for login in Login.select():
        result[login.telegram_id] = User(Stuff.get(Stuff.id == login.user.id))
    return result
