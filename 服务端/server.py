# -*- coding: utf-8 -*-
import queue
from datetime import datetime
import uuid
import asyncio
import websockets
import threading
import json

"""
服务器面向用户消息队列编程：websocket版本
"""

# 存放在线用户数组
user_online =  []

class ChatServer:
    def __init__(self, ip='0.0.0.0', port=8005):
        """
        生命周期:
        init(初始化) ——>
        """
        # 1.初始化
        self.user_message_queue = queue.Queue()  # 实例化用户消息队列:空队列 --> (conn, user, addr, data)
        # 2.初始化
        self.init()

        print("------------websocket监听启动成功-------")
        print("--------------监听地址:{0}:{1}----------".format(ip, port))
        # 启动
        start_server = websockets.serve(self.conn_handle, ip, port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    def data_handle(self,data):
        """
        来源信息化处理
        :param data:
        :return:
        """
        return  data


    async def conn_handle(self, websocket):
        # 客户端连接： 客户端websocket对象
        conn_msg = {
            "code": 200,
            "type": "connect",
            "msg": "与服务器连接成功!"
        }

        await websocket.send(str(conn_msg))
        # 用户配置设置
        user_config_str =await websocket.recv()  # 接受信息
        """
        格式:
        {
          "secret_key:"",
          "nickName": "",
        }
        """
        user_config = json.loads(str(user_config_str))
        user = {
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),        # 连接时间
            "secret_key": user_config["secret_key"],                     # 密钥
            "uuid": str(uuid.uuid1()) ,                                  # 客户端唯一标识
            "client": websocket,                                         # clieent
            "nickName": user_config["nickName"]                          # 昵称
        }

        secret = {
            "code": 200,
            "type": "config",
            "msg":"用户配置信息完成设置成功"
        }
        await websocket.send(str(secret))
        user_online.append(user)

        print("[客户端]:{0}  连接成功".format(user["uuid"]))

        while True:
            # 接受消息
            try:
                message  = await websocket.recv()     #接受信息
                # print(message)
                msg_data = json.loads(str(message).replace('\\', '/'))      #格式化信息
                # print(msg_data['data'])
                """
                消息类型: 普通消息-text 视频-video 音频-audio 图片-picture
                """
                data_ = {
                    "type": msg_data['type'],                                #  消息类型: 普通消息-text 视频-video 音频-audio 图片-picture
                    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),    # 接受时间
                    "data": self.data_handle(msg_data['data']),              # 消息数据：信息化处理
                    "uuid": user["uuid"],  # 来源客户端
                    "secret_key": user["secret_key"],  # 秘钥
                    "user": user  # 用户信息
                }
                # 添加进消息队列
                self.user_message_queue.put(data_)

            except Exception as e:
                # 删除特定的对象
                # user_online.remove(user)
                print(repr(e))

    async def user_task_tread(self, user):
        """
        客户端 --> 服务器  接受
        用户任务
        :return:
        """
        # 提示连接ok
        print("开始处理客户端请求")

        print("连接客户端:{0} 进入消息回复队列".format(user["addr"]))
        try:
            while True:
                message = await user["client"].recv()
                print(message)
                print("{0} 接受消息:{1}".format(user["addr"], message))
                data_ = {
                    "type": 'text',                                        # 消息类型： file text
                    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 接受时间
                    "data": message,                                          # 消息数据
                    "uuid": user["uuid"],                                   #来源客户端
                    "secret_key": user["secret_key"],                      # 秘钥
                    "user": user                                              # 用户信息
                }

                print("{0}消息进队列".format(user["uuid"]))
                # 添加进消息队列
                self.user_message_queue.put(data_)

        except Exception as e:
            print(repr(e))

    def init(self):
        """
        初始化工作
        :return:
        """
        # 服务端连接信息
        self.server_conn = {
            "conn_count": 0  #连接数量
        }
        # 1.启动一个主服务器专门处理消息队列线程
        server_t = threading.Thread(target=self.server_chat_task_tread,
                                    args=(self.user_message_queue, user_online))
        server_t.start()

    def server_chat_task_tread(self,user_message_queue, user_online):
        """
        服务器 --> 客户端
        主服务器专门处理消息队列线程
        :return:
        """
        # 循环处理消息队列

        while True:
            # 获取消息
            if not user_message_queue.empty():
                user = user_message_queue.get()
                # 主动向客户端发送信息
                if  len(user_online) == 0:
                    msg = {
                        "code":300,
                        "msg": "发送失败！未有对应客户端上线"
                    }
                    user["user"]["client"].send(str(msg))

                async def test(websocket,data):
                    if await websocket.send(str(data)):
                        return True
                    return False

                for user_conn in user_online:
                    try:
                        if user_conn["secret_key"] == user["secret_key"] and user_conn["uuid"] != user["uuid"]:
                            try:
                                # task = asyncio.create_task(test(user_conn["client"], str(user["data"])))
                                # 如果要看到task的执行结果
                                # 可以使用await等待协程执行完成，并返回结果
                                # ret = await task
                                msg = {
                                    "code": 200,
                                    "type": user["type"],
                                    "msg": user["data"],
                                    "send_time": user["time"],
                                    "client": user["uuid"],
                                    "nickName": user["user"]["nickName"]
                                }
                                asyncio.run(test(user_conn["client"],  msg))
                                print("发送成功:{0}".format(msg))
                            except Exception as e:
                                # user_message_queue.put(user)  # 重新添加进消息队列
                                print("向{0}发送消息失败!".format(user["uuid"]))
                                print("错误信息: {0}".format(e))
                    except:
                        # msg = {
                        #     "code": 400,
                        #     "secret":user["secret_key"],
                        #     "msg": "当前未有客户端连接"
                        # }
                        # asyncio.run(test(user_conn["client"], msg))
                        # print("警告:{0}".format(msg))
                        user_message_queue.put(user)  # 重新添加进消息队列



if __name__ == '__main__':
    # 实例化聊天系统实例
    chat = ChatServer()

