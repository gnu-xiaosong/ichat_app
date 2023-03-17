<template>
  <q-page>
    <q-splitter
    v-model="splitterModel"
    separator-class="bg-orange"
    separator-style="width: 3px"
    style="height: 100vh"
    >
      <template v-slot:before>
        <div class="left">
          <div class="phone">
            <div class="top-fun">消息列表</div>
            <div class="phone-list bg-grey-1">
              <q-card square style="width:100%;height: 100%">
                  <!-- 会话列表 -->
                  <q-list bordered>
                      <q-item v-for="contact,index in chat" :key="index" class="q-my-sm" clickable v-ripple>
                          <q-item-section avatar>
                            <q-avatar color="primary" text-color="white">
                              {{ contact.avatar }}
                            </q-avatar>
                          </q-item-section>

                          <q-item-section>
                            <q-item-label>{{ contact.nickName }}</q-item-label>
                            <q-item-label caption lines="1">{{ contact.name }}</q-item-label>
                          </q-item-section>

                          <q-item-section side>
                            <!-- 拓展功能区 -->
                            <q-icon name="chat_bubble" color="green" />
                            {{ contact.type }}
                          </q-item-section>
                        </q-item>
                  </q-list>
              </q-card>
            </div>
          </div>
          <div class="function shadow-1">
            <div class="add">
              <q-fab
                v-model="fabCenter"
                vertical-actions-align="center"
                color="primary"
                glossy
                icon="add"
                direction="up"
              >
                <div class="row add-some shadow-1">
                  <div class="col add-some-item">
                    <q-tooltip
                      q-tooltip
                      anchor="top middle"
                      self="center middle"
                      content-class="bg-indigo"
                      :offset="[10, 10]"
                    >
                      新增聊天
                    </q-tooltip>
                    <q-icon
                      @click="openAddChat()"
                      class="add-some-icon"
                      name="person_add"
                      size="25px"
                    />
                  </div>
                  <div class="col add-some-item">
                    <q-tooltip
                      content-class="bg-indigo"
                      self="center middle"
                      anchor="top middle"
                      :offset="[10, 10]"
                    >
                      新增直播
                    </q-tooltip>
                    <q-icon
                      class="add-some-icon"
                      name="video_camera_front "
                      size="25px"
                    />
                  </div>
                </div>
              </q-fab>
            </div>
          </div>
        </div>
      </template>

      <template v-slot:after>
        <q-splitter v-model="insideModel" horizontal>
          <!-- 顶部 -->
          <div class="top"></div>

          <template v-slot:before>
              <div class="chat" >
                <!-- 聊天 -->
                <div class="scroll chat_win" id="scroll">
                  <!-- 标题 -->
                  <q-chat-message label="Sunday, 19th" />
                  <q-chat-message
                    v-for="(item, index) in chat[chat_index].chat_data"
                    :key="index"
                    :size="$q.platform.is.mobile==true?6:2"
                    :sent="item.send"
                    bg-color="primary"
                    :label="item.label"
                    
                  >
                    <template v-slot:default >
                    <span >{{ item.msg }}</span> 
                    </template>
                    <template v-slot:name>{{ item.name }}</template>
                    <template v-slot:stamp>{{ item.time }}</template>
                    <template v-slot:avatar>
                      <img
                        style="margin-right: 3px"
                        v-if="item.send"
                        class="q-message-avatar q-message-avatar--sent shadow-4"
                        src="https://cdn.quasar.dev/img/avatar4.jpg"
                      />
                      <img
                        v-else
                        style="margin-right: 3px"
                        class="q-message-avatar q-message-avatar--sent shadow-4"
                        src="https://cdn.quasar.dev/img/avatar4.jpg"
                      />
                    </template>
                  </q-chat-message>
                </div>
              </div>
          </template>

          <template v-slot:after>
            <div class="fun" dark>
              <div class="text">
                <!-- 功能区 -->
                <div class="top_tool"></div>
                <!-- 文本框 -->
                <div class="txet_input">
                  <q-input
                    v-model="msg"
                    clearable
                    standout
                    borderless
                    autogrow
                    @keydown.enter="enterSend()"
                  />
                </div>
              </div>
              <div class="send">
                <q-btn
                  @click="simulateSubmit()"
                  :loading="submitting"
                  label="发送"
                  icon-right="send"
                  class="q-mt-md"
                  size="13px"
                  color="teal"
                >
                  <template v-slot:loading>
                    <q-spinner-facebook />
                  </template>
                </q-btn>
              </div>
            </div>
          </template>
        </q-splitter>
      </template>
    </q-splitter>
    <!-- 增加个人聊天 -->
    <q-dialog
      v-model="bar"
      persistent
      transition-show="flip-down"
      transition-hide="flip-up"
    >
      <q-card class="bg-primary text-white" style="width: 700px; max-width: 80vw;">
        <q-bar>
          <q-icon name="chat_bubble" />
          <q-space />
          <div style="font-size: 14px">增加聊天</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-white text-primary">Close</q-tooltip>
          </q-btn>
        </q-bar>

        <q-card-section class="q-pt-none">
          <div class="add-chat">
            <div class="row">
                <div class="col aa">
                  <!-- 会话类型：私聊，群聊 -->
                  <div class="tt">
                    <span style="margin-right: 25px">类型</span> 
                    <q-radio v-model="chat_type" color="cyan"  val="person" label="私聊" />
                    <q-radio v-model="chat_type" color="cyan" val="group" label="群聊" />
                  </div>
                  <!-- 会话窗口名称 -->
                  <q-input
                    filled
                    bottom-slots
                    item-aligned
                    v-model="add_chat.name"
                    class="aaa"
                  >
                    <template v-slot:before >
                      <span style="font-size:10px">窗口名称</span> 
                    </template>
                  </q-input>
                  <!-- 会话昵称 -->
                  <q-input
                    filled
                    bottom-slots
                    item-aligned
                    v-model="add_chat.nickName"
                    
                    class="aaa"
                  >
                    <template v-slot:before >
                      <span style="font-size:10px">昵称  </span> 
                    </template>
                  </q-input>
                </div>
                <div class="col aa">
                   <!-- 头像 -->
                  <q-input
                    filled
                    bottom-slots
                    item-aligned
                    v-model="add_chat.avatar"
                    label="头像"
                    
                    class="aaa"
                  >
                    <template v-slot:before>
                      <q-icon name="face" />
                    </template>
                  </q-input>
                  <!-- ws地址 -->
                  <q-input
                    filled
                    item-aligned
                    bottom-slots
                    v-model="add_chat.ws_addr"
                   
                  
                    label="默认全局"
                    class="aaa"
                  >
                    <template v-slot:before >
                      <span style="font-size:10px">服务器 </span> 
                    </template>
                  </q-input>
                  <!-- 会话秘钥 -->
                  <q-input
                    filled
                    bottom-slots
                    v-model="add_chat.secret"
                 
                    label="会话密钥"
                    item-aligned
                    class="aaa"
                  >
                    <template v-slot:before >
                      <span style="font-size:10px">密钥</span> 
                    </template>
                    <template v-slot:after >
                        <q-tooltip
                            q-tooltip
                            anchor="top middle"
                            self="center middle"
                            content-class="bg-indigo"
                            :offset="[10, 10]"
                          >
                            自动生成
                          </q-tooltip>
                        <q-icon
                            @click="generat()"
                            name="power"
                          />
                    </template>
                  </q-input>
                </div>
                 
            </div>
          </div>
        </q-card-section>

        <q-card-section style="text-align: center">
          <q-btn @click="addUserList()" color="secondary" style="margin-right: 9px" label="添加" />
          <q-btn @click="connection()" color="purple" label="连接" />
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>
<script>
import { date } from "quasar";
export default {
  name: "MainLayout",
  data() {
    return {
      drawer: false,
      msg: "",
      fabCenter: false,
      contentStyle: {
        backgroundColor: 'rgba(0,0,0,0.02)',
        color: '#555'
      },

      contentActiveStyle: {
        backgroundColor: '#eee',
        color: 'black'
      },

      thumbStyle: {
        right: '2px',
        borderRadius: '5px',
        backgroundColor: '#027be3',
        width: '5px',
        height:'10px',
        opacity: 0.75
      },
      splitterModel: 25,
      insideModel: 80,
      submitting: false,
      public_ws_url: "ws://localhost:8005",
      chat_type: "person",
      add_chat: {
        type: "person", //会话方式:person  grounp
        name: "会话窗口1", //名称
        nickName: "", //会话昵称
        avatar: "account_circle", //头像
        status: true, //会话状态
        ws_addr: "ws://localhost:8005", //ws地址
        secret: "xskj", //通讯秘钥
        ID: "", //聊天seesion
        websocket: {}, //websocket对象
        chat_data: [//聊天数据
          
        ],
      },
      // 聊天组=私聊+群聊
      chat: [
        {
        type: "person", //会话方式:person  grounp
        name: "会话窗口", //名称
        nickName: "", //会话昵称
        avatar: "account_circle", //头像
        status: true, //会话状态
        ws_addr: "ws://localhost:8005", //ws地址
        secret: "xskj", //通讯秘钥
        ID: "234234", //聊天seesion
        websocket: {}, //websocket对象
        chat_data: [//聊天数据
          
        ],
      },
      ], 
      bar: false,
      alive_websocket: {},  //当前活跃websocket对象
      chat_index:0          //当前会话的chat的index小标
    };
  },
  mounted() {
    // this.$q.dark.set(true);
    // 实例化websocket-->公共
  },
  methods: {
    scrollFooter() {
      this.$nextTick(() => {
        var div = document.getElementById('scroll');;
        div.scrollTop = div.scrollHeight;
      });
    },
    enterSend() {
      this.send();
      this.scrollFooter();
      this.msg = "";
    },
    generat() {
      var secret = new Date().getTime() + Math.random().toString(36).substr(2);
      this.add_chat.secret = secret;
    },
    addUserList() {
      const timeStamp = Date.now();
      let ID = date.formatDate(timeStamp, "YYYYMMDDTHHmmssSSSZ");
      
      this.add_chat.ID = ID;
      this.add_chat.status = false;
      if (this.chat.push(this.add_chat)){
        this.$q.notify({
          message: `添加[${this.add_chat.name}]会话成功!`,
          color: "purple",
          icon: "chat_bubble",
          position: "top",
        });
      }
      
    },
    connection() {
      this.chat_websocket(this.add_chat);
      this.openAddChat()
    },
    // openAddChat()
    openAddChat() {
      this.bar = !this.bar;
    },
    // 聊天实例
    chat_websocket(chat_item) {
      let _this = this;
      if ("WebSocket" in window) {
        // 新建一个会话websocket连接
        let wx_addr =
          chat_item.ws_addr.length == 0
            ? this.public_ws_url
            : chat_item.ws_addr;
        var ws = new WebSocket(wx_addr);
        // 连接成功回调处理
        ws.onopen = function () {
          let config = `{"secret_key":"${chat_item.secret}","nickName": "${chat_item.nickName}"}`;
          // 设置会话秘钥
          ws.send(config);
          // 遍历匹配添加进会话聊天信息数组中
          _this.chat_index = _this.chat.indexOf(chat_item);

        };


        // 监听数据-->接收数据
        ws.onmessage = function (evt) {
          var a = evt.data.replace(/'/g, '"');
          var data = JSON.parse(a);

          if (data.type == "connect") {
            // 连接成功
            console.log("连接状态:");
            console.log(data.msg);
            _this.$q.notify({
              message: `连接${chat_item.name}会话成功!`,
              color: "purple",
              icon: "connect_without_contact",
              position: "top",
            });
            // websocket对象
            _this.alive_websocket = ws;
          } else if (data.type == "config") {
            console.log("配置设置:");
            console.log(data.msg);
          } else {
            // 正常会话  
            // 添加进会话聊天数组中
            _this.chat[_this.chat_index].chat_data.push({
              name: data.nickName, //昵称
              time: data.send_time, //时间
              send: false, //是否为发送者：false or true
              msg: data.msg, //消息内容
              label: "", //标签
            });
          }
          _this.scrollFooter();
        };
        ws.onclose = function () {
          // 关闭 websocket
          _this.$q.notify({
            message: `${chat_item.name}会话连接中断!`,
            color: "purple",
            icon: "portable_wifi_off ",
            position: "top",
          });
        };
      } else {
        // 浏览器不支持 WebSocket
        this.$q.notify({
          message: `您的浏览器不支持 WebSocket!`,
          color: "purple",
          icon: "highlight_off",
          position: "top",
        });
      }
    },
    send() {
      // 获取当前活跃chat
      let chat = this.chat[this.chat_index];
      // 发送时间
      const timeStamp = Date.now();
      let send_time = date.formatDate(timeStamp, "YYYY-MM-DDTHH:mm:ss");
      console.log("----------------------")
      console.log(chat);
      let send_msg = {
        name: chat.nickName.length ==0?"我":this.chat[this.chat_index].nickName, //昵称
        time: send_time, //时间
        send: true, //是否为发送者：false or true
        msg: this.msg, //消息内容
        label: "", //标签
      };
      // push进消息队列
      this.chat[this.chat_index].chat_data.push(send_msg);
      // 滑动到底部
      // this.scrollFooter();
      // 检测
      console.log(typeof chat.websocket);
      // 发送   
      try {
         this.alive_websocket.send(this.msg)
      }catch(err) {
        // 发送失败
        this.$q.notify({
          message: `消息发送失败!`,
          color: "purple",
          caption: err,
          icon: "portable_wifi_off ",
          position: "top",
        });
      }
    },
    simulateSubmit() {
      this.submitting = true;
      this.send();
      this.submitting = false;
      this.msg = "";
      this.scrollFooter();
    },
  },
};
</script>

<style scoped>
.left {
  position: relative;
  width: 100%;
  height: 100%;
}

.fun {
  width: 100%;
  height: 100%;
  position: relative;
}
.send {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  bottom: 20px;
  right: 10px;
  width: 10%;
  height: auto;
  /* background-color: pink; */
}

.function {
  position: absolute;
  bottom: 0px;
  width: 100%;
  margin: auto;
  height: 15%;
  border-radius: 7px 7px 0 0;
  background-color: #9c27b0;
}

.phone {
  width: 100%;
  height: 85%;
  /* background-color: green; */
}

.chat {
  position: relative;
  width: 99%;
  height: 100%;
  margin: auto;
  /* background-color: pink; */
}

.top {
  position: absolute;
  top: 0px;
  width: 100%;
  height: 40px;
  background-color: blue;
}

.chat_win {
  width: 100%;
  height: 100%;
  margin: auto;
  padding-top: 40px;
  padding: 10px;
  padding-bottom: 20px;
  background-color: pink;
}
.a {
  width: 100%;
  height: 100%;
  /* background-color: red; */
}

.b {
  width: 100%;
  height: 100%;
  /* background-color: red; */
}

.text {
  width: 100%;
  height: 100%;
  /* background-color: blue; */
}

.top_tool {
  width: 100%;
  height: 20%;
  /* background-color: yellow; */
}

.txet_input {
  width: 100%;
  height: 80%;
  padding-left: 9px;
  background-color: red;
}

.add {
  width: 60px;
  height: 60px;
  margin: -30px auto;
  /* background-color: white; */
}

.top-fun {
  width: 100%;
  height: 5%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 700;
  background-color: red;
}

.phone-list {
  width: 100%;
  height: 95%;
}

.add-chat {
  display: flex;
  align-items: center;
  width: 100%;
  height: 300px;
  margin: 10px auto;
  font-weight: 700;
  /* color: black; */
  /* background-color: pink; */
}
.add-some {
  width: 250%;
  height: 50px;
  border-radius: 5px;
  background-color: #83c785;
}

.add-some-item {
  display: flex;
  justify-content: center;
  align-items: center;
}

.add-some-icon {
  color: #607d8b;
}



.aa {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
}
.aaa {
  width: 90%;
}
.add-some-icon:hover {
  color: #1976d2;
}

.tt {
  width: 100%;
  height: 10px;
  padding-left: 10%;
  margin-bottom: 40px;
  color: rgba(0,0,0,0.54);
  font-size: 10px;
  /* margin-left: 20px; */
}
</style>
