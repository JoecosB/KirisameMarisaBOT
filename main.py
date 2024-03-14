import json
import re
import os
import requests
import botpy
import pyautogui
from botpy.message import Message

# 读取机器人的id和访问密钥
with open("secret_info.json") as info_file:
    secret = json.load(info_file)

# 设置帮助信息
HELP_INFO = '''JocoBOT现有功能:
1. 窥屏
2. 随机二次元

更多功能敬请期待!'''

# 机器人类
class MyClient(botpy.Client):

    async def on_at_message_create(self, message: Message):
        # 获取信息内容和发送信息用户id
        content = re.search(r"> (\w+)", message.content).group(1)
        userID = message.author.username

        # 功能：测试bot是否存活
        if content == "测试":
            print(f"{userID}进行了测试")
            await message.reply(content=f"<@{userID}>testis ok!")


        # 功能：偷看我的屏幕
        elif content == "窥屏":
            print(f"{userID}进行了窥屏")
            await message.reply(content="让我看看那个死宅在做什么...稍等片刻哦")

            # 获取屏幕截图并保存到本地，方便以二进制流读取
            screen = pyautogui.screenshot()
            screen.save(f"{userID}.png")

            # 以二进制流读取图片，并发送给用户
            with open(f"{userID}.png", "rb") as image:
                await message.reply(content=f"<@{userID}>嗯哼～客官要的截图！", file_image = image)

                # 删除已经发送的图片
                os.remove(f"{userID}.png")


        # 功能：获取好康的
        elif content == "随机二次元":
            print(f"{userID}进行了随机二次元")
            await message.reply(content="获取二次元中...")

            # 使用get方法从api获取二次元图像，并发送给用户
            image = requests.get("https://api.anosu.top/img").content
            await message.reply(content=f"<@{userID}>嗯哼～客官要的二次元！", file_image = image)
        

        # 功能：发送已有功能列表
        elif content == "帮助":
            print(f"{userID}请求了帮助")
            await message.reply(content=f"{HELP_INFO}")


intents = botpy.Intents(public_guild_messages=True) 
client = MyClient(intents=intents)


client.run(appid=secret["APPID"], secret=secret["SECRET"])