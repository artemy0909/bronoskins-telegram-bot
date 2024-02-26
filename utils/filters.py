from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery

from loader import users
from ui.inline_commands import get_callback_command
from ui.text.static import ACCESS_DENIED


class StateFilter(BoundFilter):
    def __init__(self, state):
        super().__init__()
        self.state = state

    async def check(self, message: Message) -> bool:
        if message.text and message.text[0] == "/":
            return False
        return users[message.from_user.id].state.current_state is self.state if message.from_user.id in users else False


class CallbackCommandFilter(BoundFilter):
    def __init__(self, command):
        super().__init__()
        self.command = command

    async def check(self, query: CallbackQuery) -> bool:
        return get_callback_command(query) == self.command


class AccessFilter(BoundFilter):
    def __init__(self, *access_levels):
        super().__init__()
        self.access_levels = list(access_levels)

    async def check(self, message: Message) -> bool:
        if message.from_user.id in users:
            access = users[message.from_user.id].right_level in self.access_levels
        else:
            access = False
        if not access:
            await message.reply(
                text=ACCESS_DENIED)
        return access


class OnExitFilter(BoundFilter):
    async def check(self, chat_member: ChatMemberUpdated) -> bool:
        return chat_member.new_chat_member.status == "kicked"


class UserNotAuthFilter(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.from_user.id not in users


class LinkSwitchFilter(BoundFilter):
    def __init__(self, link_uname):
        super().__init__()
        self.link_uname = link_uname

    async def check(self, message: Message) -> bool:
        return message.text[:4] == f"/{self.link_uname}_"
