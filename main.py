import json
import botpy
from botpy.message import Message

# 读取机器人的id和访问密钥
with open("secret_info.json") as info_file:
    secret = json.load(info_file)

# 机器人类
class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")


intents = botpy.Intents(public_guild_messages=True) 
client = MyClient(intents=intents)


client.run(appid=secret["APPID"], secret=secret["SECRET"])