import botpy
from botpy.message import Message

APPID = "102096507"
SECRET = "yV2Z6dAiGoMuS0Y7gFoNwV5fFpPzZAlM"

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")

intents = botpy.Intents(public_guild_messages=True) 
client = MyClient(intents=intents)
client.run(appid=APPID, secret=SECRET)