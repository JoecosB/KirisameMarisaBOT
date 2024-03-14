import json
import re
import datetime
import os
import requests
import botpy
import pyautogui
from botpy.message import Message
from random import randint

# 读取机器人的id和访问密钥
with open("secret_info.json") as info_file:
    secret = json.load(info_file)

# 读取今天的日期
today_date = datetime.date.today().strftime('%d')


# 读取服务端的用户信息
with open("user_data.json") as data:
    try:
        users_data = json.load(data)
    except json.decoder.JSONDecodeError:
        print("服务端没有user_data.json文件, 已在脚本目录下创建。")
        users_data = {}

# 设置帮助信息
HELP_INFO = '''雾雨魔理沙现有功能:
1. 窥屏
2. 随机二次元
3. 随机金句
4. 猫猫
5. 今日运势

更多功能敬请期待!'''

# 机器人类
class MyClient(botpy.Client):

    async def on_at_message_create(self, message: Message):
        # 获取信息内容和发送信息用户id
        content = re.search(r"> (\w+)", message.content).group(1)
        user_name = message.author.username
        userID = message.author.id

        # 从users_data中获取该用户的信息，若该用户是新用户则创建该用户的信息。
        try:
            user_data = users_data[f"{userID}"]
        except KeyError:
            users_data[f"{userID}"] = {"user_luck":{"luck_date":f"{int(today_date)-1}", "luck_rate":0}}
            user_data = users_data[f"{userID}"]

        # 功能：测试bot是否存活
        if content == "测试":
            print(f"{user_name}进行了测试")
            await message.reply(content=f"<@{user_name}>沙沙一直在的啦～")


        # 功能：偷看我的屏幕
        elif content == "窥屏":
            print(f"{user_name}进行了窥屏")
            await message.reply(content="让我看看那个死宅在做什么...稍等片刻DAZE☆")

            # 获取屏幕截图并保存到本地，方便以二进制流读取
            screen = pyautogui.screenshot()
            screen.save(f"{user_name}.png")

            # 以二进制流读取图片，并发送给用户
            with open(f"{user_name}.png", "rb") as image:
                await message.reply(content=f"<@{user_name}>啊哈～客官要的截图！", file_image = image)

                # 删除已经发送的图片
                os.remove(f"{user_name}.png")


        # 功能：获取好康的
        elif content == "随机二次元":
            print(f"{user_name}进行了随机二次元")
            await message.reply(content="获取二次元中...")

            # 使用get方法从api获取二次元图像，并发送给用户
            image = requests.get("https://api.anosu.top/img").content
            await message.reply(content=f"<@{user_name}>嗯哼～客官要的二次元！", file_image = image)
        

        # 功能：火星语转换
        elif content == "":
            pass


        # 功能：随机金句
        elif content == "随机金句":
            print(f"{user_name}进行了随机金句")
            await message.reply(content="翻阅姆Q那里「借」来的书中...")

            # 使用requests库调用随机金句api, 并把获取的json字符串转换成字典, 并获取金句的作者和金句内容
            res = requests.get("https://api.xygeng.cn/one")
            res_dict = json.loads(res.text)
            quote = res_dict["data"]["content"]
            origin = res_dict["data"]["origin"]

            # 回复消息
            await message.reply(content=f"来自于 {origin} 的金句：\n{quote}")


        # 功能：猫猫
        elif content == "猫猫":
            print(f"{user_name}进行了猫猫")
            await message.reply(content="获取猫猫中...")

            # 通过requests库调取api，并把获取的json字符串转换成字典
            res = requests.get("https://api.thecatapi.com/v1/images/search?size=full")
            res_dict = json.loads(res.text)

            # 获取图片url，并将图片保存在本地
            url = res_dict[0]["url"]
            pic = requests.get(url)
            with open(f"{user_name}.png", "wb") as temp:
                temp.write(pic.content)

            # 以二进制形式打开图片，并发送给客户
            with open(f"{user_name}.png", "rb") as image:
                await message.reply(content=f"<@{user_name}>您要的猫猫啦", file_image = image)

                # 删除已经发送的图片
                os.remove(f"{user_name}.png")


        # 功能：占卜
        elif content == "今日运势":
            print(f"{user_name}请求了今日运势")
            await message.reply(content="沙沙可是能看见你的未来的哦～")

            # 从user_data中读取user_luck部分
            user_luck = user_data['user_luck']

            # 从user_luck中读取上一次保存的运气值的日期和运气值
            luck = user_luck['luck_rate']
            date = user_luck['luck_date']

            # 若日期是不今天，则生成新运气, 并更新日期
            if date != today_date:
                luck = randint(0, 100)
                date = today_date
            
            # 判断运气分级，并发送对应的图片
            luck_class = int(luck/16.6666)
            luck_name = ["大凶", "中凶", "末凶", "末吉", "中吉", "大吉"][luck_class]
            with open(f"luck_imgs/{luck_class}.png", "rb") as image:
                await message.reply(content=f"您今天的运气值是{luck}, 属于「{luck_name}」哦！", file_image = image)

            # 把user_data更新
                user_data['user_luck']['luck_date'] = date
                user_data['user_luck']['luck_rate'] = luck


        # 功能：发送已有功能列表
        elif content == "帮助":
            print(f"{user_name}请求了帮助")
            await message.reply(content=f"{HELP_INFO}")
        

        # 隐藏功能：亲亲
        elif content == "亲亲":
            print(f"{user_name}进行了亲亲")
            await message.reply(content=f"@<{user_name}>只能偷偷亲一下哦～")
        
        
        # 隐藏功能：抱抱
        elif content == "抱抱":
            print(f"{user_name}进行了抱抱")
            await message.reply(content=f"@<{user_name}>那就来抱抱吧！嗯唔～")


        # 将修改过的user_data重新写入users_data并更新json文件
        users_data[f"{userID}"] = user_data
        with open("user_data.json", "w") as file:
            json.dump(users_data, file, indent=4)


intents = botpy.Intents(public_guild_messages=True) 
client = MyClient(intents=intents)


client.run(appid=secret["APPID"], secret=secret["SECRET"])