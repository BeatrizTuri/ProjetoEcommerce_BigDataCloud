
import asyncio
from aiohttp import web
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    BotFrameworkAdapter,
    ConversationState,
    MemoryStorage,
    UserState,
)
from botbuilder.schema import Activity, ActivityTypes

from bots.dialog_bot import DialogBot
from dialogs.main_dialog import MainDialog

from dotenv import load_dotenv
load_dotenv()

# Configurações do Bot
APP_ID = ""
APP_PASSWORD = ""
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Estados
MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
USER_STATE = UserState(MEMORY)

# Diálogo principal
DIALOG = MainDialog()
BOT = DialogBot(CONVERSATION_STATE, USER_STATE, DIALOG)

# Endpoint de mensagens
async def messages(req):
    body = await req.json()
    activity = Activity().deserialize(body)

    async def call_bot(turn_context):
        await BOT.on_turn(turn_context)

    await ADAPTER.process_activity(activity, "", call_bot)
    return web.Response(status=200)

# Inicializa servidor
app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(app, host="localhost", port=3978)
    except Exception as error:
        raise error
