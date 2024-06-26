import json
import re
import datetime
import os
import requests
import botpy
import pyautogui
from botpy.message import Message
from random import randint

def get_remain(url, headers, payload):
    """查询电费余额"""

    # 发送POST请求, 提取json中的errmsg
    response = requests.request("POST", url, headers=headers, data=payload)
    raw = response.json()["errmsg"]

    # 从请求中提取余额并返回
    remain = re.search(r"\d+\.\d+", raw).group(0)
    return remain


# 读取机器人的id和访问密钥
with open("./json/secret_info.json") as info_file:
    secret = json.load(info_file)

# 读取查询电费的url和payload表单, 获取headers
with open("./json/electricity.json") as info_file:
    elec_info = json.load(info_file)
    headers = elec_info["headers"]

# 读取今天的日期
today_date = datetime.date.today().strftime('%d')

# 读取服务端的用户信息
with open("./json/user_data.json") as data:
    try:
        users_data = json.load(data)
    except json.decoder.JSONDecodeError:
        print("服务端没有user_data.json文件, 已在脚本目录下创建。")
        users_data = {}

# 读取运势解读
with open("./json/stories.json") as data:
    stories = json.load(data)
FATES = stories["fates"]

# 设置帮助信息
HELP_INFO = '''雾雨魔理沙现有功能:
1. 窥屏
2. 随机二次元
3. 随机金句
4. 猫猫
5. 今日运势
6. 签到
7. 商店
8. 背包
9. 魔力查询
有关「农场」请查询“农场帮助”

更多功能敬请期待!'''

FARM_INFO = '''农场帮助：
1. 种植魔晶
3. 收获
'''

# 设置魔法店信息
STORE_ITEM = '''雾雨魔法店商品列表：
1.【魔法晶种】        20魔力值
2.【一次性八卦炉】    200魔力值
3.【河童隐身逃跑科技】 50魔力值 
4.【鲣鱼昆布茶泡饭】  150魔力值

请@我， 输入[购买][空格][商品名称][空格][数量]来购买物品哦
'''
ITEM_PRICE = {
    "魔法晶种":20,
    "一次性八卦炉":200,
    "河童隐身逃跑科技":50,
    "鲣鱼昆布茶泡饭":150
}


# 机器人类
class MyClient(botpy.Client):

    async def on_at_message_create(self, message: Message):
        # 获取信息内容和发送信息用户id
        content = re.search(r"> (.*)", message.content).group(1)

        user_name = message.author.username
        userID = message.author.id

        # 从users_data中获取该用户的信息，若该用户是新用户则创建该用户的信息。
        try:
            user_data = users_data[f"{userID}"]
        except KeyError:
            users_data[f"{userID}"] = {}
            user_data = users_data[f"{userID}"]
            user_data["user_luck"] = {"luck_date":f"{int(today_date)-1}", "luck_rate":0}
            user_data["mana"] = 0
            user_data["last_check_in"] = str(0)
            user_data["storage"] = {}


        # 功能：测试bot是否存活
        if content == "/测试":
            print(f"{user_name}进行了测试")
            await message.reply(content=f"<@{user_name}>沙沙一直在的啦～")


        # 功能：偷看我的屏幕
        elif content == "/窥屏":
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
        elif content == "/随机二次元":
            print(f"{user_name}进行了随机二次元")
            await message.reply(content="获取二次元中...")

            # 使用get方法从api获取二次元图像，并发送给用户
            image = requests.get("https://api.anosu.top/img").content
            await message.reply(content=f"<@{user_name}>嗯哼～客官要的二次元！", file_image = image)
        

        # 功能：火星语转换
        elif content == "":
            pass


        # 功能：随机金句
        elif content == "/随机金句":
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
        elif content == "/猫猫":
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
        elif content == "/占卜":
            print(f"{user_name}请求了今日运势")

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
                await message.reply(file_image = image, content=f"<@{user_name}>今天的运气值是{luck}, 属于「{luck_name}」哦！")

            # 发送对应的运势解读
            interpret = FATES[f"{luck_class}"]
            await message.reply(content=interpret)

            # 把user_data更新
            user_data['user_luck']['luck_date'] = date
            user_data['user_luck']['luck_rate'] = luck


        # 功能：签到
        elif content == "/签到":
            print(f"{user_name}进行了签到")

            # 读取用户签到状态，若今天已经签到，则不签到
            if user_data["last_check_in"] == today_date:
                await message.reply(content=f"<@{user_name}>您今天已经签过到啦～贪心的人会受到幻想乡的惩罚哦")
            
            else:
                add_mana = 100 + randint(-30, 30)
                user_data["mana"] += add_mana
                mana = user_data["mana"]

                await message.reply(content=f"<@{user_name}>签到成功!\n你从雾雨魔法店获得了{add_mana}点魔力值。你现在共有{mana}点魔力值。")
                user_data["last_check_in"] = today_date


        # 功能：展示雾雨魔法店商品列表
        elif content == "/雾雨魔法店":
            print(f"{user_name}访问了雾雨魔法店")
            await message.reply(content=f"{STORE_ITEM}")


        # 功能：购买商品
        elif content[0:2] == "/购买":
            print(f"{user_name}进行了购买")

            # 读取用户背包信息
            user_storage = user_data["storage"]

            # 获取用户购买商品名称和购买数量
            item = re.findall(r"(?<=\s).+?(?=\s)", content)[0]
            count = int(re.findall(r"\d+$", content)[0])

            # 查询用户输入的物品是否在商店中
            in_store = 1
            try:
                price = ITEM_PRICE[f"{item}"]*count
            except KeyError:
                price = 100000
                await message.reply(content=f"<@{user_name}>小店没有您要买的这件东西呢～看看有没有其他感兴趣的吧！")
                in_store = 0

            # 判断用户是否买得起该数量的该物品
            if int(user_data["mana"]) >= price:
                affordable = 1
            else:
                affordable = 0

            # 若物品在商店中且买得起，则继续购买流程
            if in_store and affordable:

                # 查询用户是否曾经拥有过该物品, 若不曾拥有，则在user_storage中创建该物品的键
                try:
                    user_storage[f"{item}"] += count
                except KeyError:
                    user_storage[f"{item}"] = count
                await message.reply(content=f"<@{user_name}>交易成功！\n您共花费了{price}魔力值，购买了{count}个「{item}」")

                # 从用户的账户中扣除对应魔力值
                user_data["mana"] = int(user_data["mana"]) - price
            
            # 若物品在商店中但买不起，则终止交易并返回信息
            else:
                if in_store and not affordable:
                    await message.reply(content=f"<@{user_name}>您的魔力值不够呢！试着每天签到，坚持每日签到、种植魔晶吧！")

            # 更新user_data
            user_data["storage"] = user_storage


        # 功能：查看背包
        elif content == "/背包":
            print(f"{user_name}查看了背包")

            # 从user_data中提取user_storage
            user_storage = user_data["storage"]

            # 遍历user_storage中的物品，并整合到字符串output中; 同时计算背包中拥有的物品数量
            output = "您的背包中有："
            item_count = 0
            for item in user_storage.keys():
                count = user_storage[f"{item}"]

                # 如果count是0，则不输出此物品
                if count != 0:
                    item_count += 1
                    output += f"\n{count}个「{item}」"
            
            #检测item_count，若是0则返回特殊消息
            if item_count != 0:
                await message.reply(content=f"<@{user_name}>{output}")
            else:
                await message.reply(content=f"<@{user_name}>您的背包空空如也呢，快来逛逛雾雨魔法店吧！")


        # 功能：查看魔力值
        elif content == "/魔力查询":
            print(f"{user_name}查询了魔力")

            # 从user_data中读取mana，并发送给用户
            mana = user_data["mana"]
            await message.reply(content=f"<@{user_name}>您有{mana}点魔力值哦")


        # 功能：种植魔晶
        elif content == "/种植魔晶":
            print(f"{user_name}进行了魔晶种植")

            # 尝试查询用户的农场，若农场不存在，则创建新的农场
            try:
                farm = user_data["farm"]
            except KeyError:
                user_data["farm"] = {"lv":"1", "planted":"false", "last_plant_date":"0", "exp":"0"}
                farm = user_data["farm"]
            
            # 查询用户背包中是否存在过魔法晶种
            user_storage = user_data["storage"]
            try:
                seed = user_storage["魔法晶种"]
            except KeyError:
                user_storage["魔法晶种"] = 0
                seed = user_storage["魔法晶种"]

            # 检测魔晶种子数量，若数量小于1则不种植
            if seed != 0:
                seed -= 1
                have_seed = 1
            else:
                have_seed = 0
                await message.reply(content=f"<@{user_name}>您还没有购买魔晶种子呢！快去雾雨魔法店看看吧！")
            
            # 判断是否已经有种植魔晶，若未种植则种植
            if farm["planted"] == "false" and have_seed:
                farm["planted"] = "true"
                farm["last_plant_date"] = str(today_date)
                await message.reply(content=f"<@{user_name}>您已成功种植魔晶！记得明天来收获哦～")
            elif farm["planted"] == "true":
                await message.reply(content=f"<@{user_name}>您已经有种植好的魔晶啦！")

            # 更新user_data
            user_storage["魔法晶种"] = seed
            user_data["storage"] = user_storage
            user_data["farm"] = farm


        # 功能：收获魔晶
        elif content == "/收获":
            print(f"{user_name}收获了魔晶")

            # 尝试查询用户的农场，若农场不存在，则创建新的农场
            try:
                farm = user_data["farm"]
            except KeyError:
                user_data["farm"] = {"lv":"1", "planted":"false", "last_plant_date":"0", "exp":"0"}
                farm = user_data["farm"]
            farm_lv = farm['lv']
            farm_exp = farm['exp']
            
            # 查询用户农场中是否有种植的魔晶，并判断种植时间是不是今天
            if farm["planted"] != "false" and int(farm["last_plant_date"]) != today_date:
                condition = 1
            else:
                condition = 0

            # 如果条件符合则开始收获，反之停止收获
            if condition == 0:
                await message.reply(content=f"<@{user_name}>你还没有种植魔晶哦～快去种植吧！")
            else:
                farm["planted"] = 'false'

                # 增加用户的魔力值和农场经验
                add_mana = 200*(1+farm_lv/10) + randint(-50, 50)
                user_data['mana'] += add_mana
                add_exp = 3 + randint(-2, 2)
                farm_exp = add_exp
            
            # 判断用户的农场是否可以升级
            if farm_exp >= 20:
                farm_lv += 1
                farm_exp -= 20
            
            # 向用户反馈收获成果
            await message.reply(content=f"<@{user_name}>收获成功, 获得了{add_mana}点魔力值！您现在的农场等级为{farm_lv}，距离下一级还有{20-farm_exp}经验值")
            
            # 更新user_data
            farm['lv'] = farm_lv
            farm['exp'] = farm_exp
            user_data['farm'] = farm

        # 功能：查询电费
        elif content[0:3] == "/电费":
            print(f"{user_name}查询了电费")

            # 获取用户查询的寝室号
            room = content[4:]

            # 发送提示
            await message.reply(content=f"正在查询{room}的空调电量和公共电量...")

            try:
                # 查询1号房间空调余量
                url = elec_info[f"{room}-1"]["url"]
                payload = elec_info[f"{room}-1"]["payload"]
                remain_1 = get_remain(url, headers=headers, payload=payload)

                # 查询2号房间空调余量
                url = elec_info[f"{room}-2"]["url"]
                payload = elec_info[f"{room}-2"]["payload"]
                remain_2 = get_remain(url, headers=headers, payload=payload)

                # 查询公共电费余量
                url = elec_info[f"{room}"]["url"]
                payload = elec_info[f"{room}"]["payload"]
                remain = get_remain(url, headers=headers, payload=payload)

                # 发送结果
                await message.reply(
                    content=f"{room}-1小寝空调电量剩余：{remain_1}\n{room}-2小寝空调电量剩余：{remain_2}\n{room}公共电量剩余：{remain}")
            except KeyError:
                await message.reply(content=f"抱歉，{room}暂时不可查询，或者该房间不存在！")

        # 功能：发送已有功能列表
        elif content[-2:] == "/帮助":
            print(f"{user_name}请求了帮助")

            if content == "帮助":
                await message.reply(content=f"{HELP_INFO}")

            elif content == "农场帮助":
                await message.reply(content=f"{FARM_INFO}")
        

        # 隐藏功能：亲亲
        elif content == "亲亲":
            print(f"{user_name}进行了亲亲")
            await message.reply(content=f"<@{user_name}>只能偷偷亲一下哦～")
        
        
        # 隐藏功能：抱抱
        elif content == "抱抱":
            print(f"{user_name}进行了抱抱")
            await message.reply(content=f"<@{user_name}>那就来抱抱吧！嗯唔～")


        # 将修改过的user_data重新写入users_data并更新json文件
        users_data[f"{userID}"] = user_data
        with open("./json/user_data.json", "w") as file:
            json.dump(users_data, file, indent=4)


intents = botpy.Intents(public_guild_messages=True) 
client = MyClient(intents=intents)


client.run(appid=secret["APPID"], secret=secret["SECRET"])