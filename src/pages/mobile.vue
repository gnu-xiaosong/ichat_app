<template>
  <q-layout view="lHh lpr lFf" container style="height: 100vh" class=" shadow-2 rounded-borders">
      <!-- 顶部 -->
      <q-header  class="gradient-1">
        <q-toolbar>
          <img src="../assets/logo.png" width="35px" />
          <q-space/>
          <!-- <q-badge  rounded :color="add_chat.status== true?`green`:`red`" />
          <q-toolbar-title class="nickName">{{ add_chat.nickName }}</q-toolbar-title> -->
          <q-btn flat round dense icon="settings" style="color:#c1e6de">
            <q-menu>
              <div class="row no-wrap q-pa-md">
                <div class="column">
                  <!-- <div class="text-h6 q-mb-md"></div> -->
                  <q-toggle @input="$q.dark.toggle()"  v-model="modeChange" label="夜间模式" />
                </div>
                </div>
              </q-menu>
          </q-btn>
        </q-toolbar>
      </q-header>
      <!-- 容器部分 -->
      <q-page-container>
        <q-infinite-scroll @load="onLoad" :offset="250">
          <q-card square class="no-shadow" style="width:100%;min-height: 400px;" >
            <!-- 会话列表 -->
            <q-list bordered>
              <q-item v-for="contact,index in chat" @click="$router.push({path: `/chat/${index}`})"   class="item-chat " :key="index"  clickable v-ripple>
                  <q-item-section avatar>
                    <q-avatar size="xl"  text-color="white">
                       <img :src="contact.avatar">
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
          <template v-slot:loading>
            <div class="row justify-center q-my-md">
              <q-spinner-dots color="primary" size="40px" />
            </div>
          </template>
        </q-infinite-scroll>
      </q-page-container>
      <!-- 底部页脚 -->
      <q-footer  style="background-color: #c1e6de;border-top: 1px solid;">
        <q-toolbar>
          <!-- drawer =!drawer -->
          <q-btn @click="show(true)" flat round dense icon="apps" color="black" class="q-mr-sm" />
          <div class="function">
            <div class="add">
              <q-fab
                v-model="fabCenter"
                vertical-actions-align="center"
                color="green-10"
                unelevated
                icon="chat_bubble"
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
        </q-toolbar>
      </q-footer>
      <!-- 侧滑 -->
      <q-drawer show-if-above v-model="drawer" side="left" bordered>
     ·   <setting></setting>
      </q-drawer>
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
                <!-- <div class="col aa"> -->
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
                     dense
                     disableclass="aaa"
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
                    dense
                    class="aaa"
                  >
                    <template v-slot:before >
                      <span style="font-size:10px">昵称  </span> 
                    </template>
                  </q-input>
                  <!-- 头像 -->
                  <q-input
                    filled
                    bottom-slots
                    item-aligned
                    v-model="add_chat.avatar"
                    label="头像"
                    dense
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
                    dense
                  
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
                    dense
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
          </q-card-section>

          <q-card-section style="text-align: center;margin-top:15px">
            <q-btn @click="addUserList()" color="secondary" style="margin-right: 9px" label="添加" />
            <q-btn @click="connection()" color="purple" label="连接" />
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- 工具箱容器 -->
      <q-dialog
        v-model="tool"
        persistent
        :maximized="maximizedToggle"
        transition-show="slide-up"
        transition-hide="slide-down"
      >
        <q-card class="bg-primary text-white">
          <q-bar>
            <q-space />
            <q-space />
              <div style="font-size: 14px">{{ tool_name }}</div>
            <q-space />
            <q-btn dense flat icon="minimize" @click="maximizedToggle = false" :disable="!maximizedToggle">
              <q-tooltip v-if="maximizedToggle" content-class="bg-white text-primary">Minimize</q-tooltip>
            </q-btn>
            <q-btn dense flat icon="crop_square" @click="maximizedToggle = true" :disable="maximizedToggle">
              <q-tooltip v-if="!maximizedToggle" content-class="bg-white text-primary">Maximize</q-tooltip>
            </q-btn>
            <q-btn dense flat icon="close" v-close-popup>
              <q-tooltip content-class="bg-white text-primary">Close</q-tooltip>
            </q-btn>
          </q-bar>
          <q-card-section class="q-pt-none">
            <transmission></transmission>
          </q-card-section>
        </q-card>
      </q-dialog>
      <q-dialog
        v-model="drawer"
        persistent
        :maximized="maximizedToggle"
        transition-show="flip-down"
        transition-hide="flip-up"
        >
          <q-card class="bg-primary text-white" style="width: 700px; max-width: 80vw;">
            <q-bar>
              <q-icon name="chat_bubble" />
              <q-space />
              <div style="font-size: 14px">{{ tool_name }}</div>
              <q-space />
              <q-btn dense flat icon="close" v-close-popup>
                <q-tooltip content-class="bg-white text-primary">Close</q-tooltip>
              </q-btn>
            </q-bar>

            <q-card-section class="q-pt-none">
              <div class="add-chat">
                <div class="row">
                  <!-- <div class="col aa"> -->
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
                      dense
                      disableclass="aaa"
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
                      dense
                      class="aaa"
                    >
                      <template v-slot:before >
                        <span style="font-size:10px">昵称  </span> 
                      </template>
                    </q-input>
                    <!-- 头像 -->
                    <q-input
                      filled
                      bottom-slots
                      item-aligned
                      v-model="add_chat.avatar"
                      label="头像"
                      dense
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
                      dense
                    
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
                      dense
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
            </q-card-section>

            <q-card-section style="text-align: center;margin-top:15px">
              <q-btn @click="addUserList()" color="secondary" style="margin-right: 9px" label="添加" />
              <q-btn @click="connection()" color="purple" label="连接" />
            </q-card-section>
          </q-card>
      </q-dialog>
  </q-layout>
</template>
<script>
import { date } from "quasar";
import setting from './setting.vue';
import transmission_icon from '../assets/传输助手选中.svg'
import study_icon from '../assets/我的学习.svg'
import transmission from '../components/transmission.vue'

export default {
  components: { setting,transmission },
  name: "MainLayout",
  data() {
    return {
      maximizedToggle: true,
      tool_name: "工具箱",
      tool:false,
      drawer: false,
      msg: "",
      fabCenter: false,
      contentStyle: {
        backgroundColor: 'rgba(0,0,0,0.02)',
        color: '#555'
      },
      modeChange:false,
      splitterModel: 25,
      insideModel: 80,
      submitting: false,
      public_ws_url: "ws://103.150.181.219:8005",
      chat_type: "person",
      add_chat: {
        type: "person", //会话方式:person  grounp
        name: "会话窗口1", //名称
        nickName: "ichat", //会话昵称
        avatar:  "https://cdn.quasar.dev/img/avatar.png", //头像
        status: true, //会话状态
        ws_addr: "ws://103.150.181.219:8005", //ws地址
        secret: "ichat", //通讯秘钥
        ID: "", //聊天seesion
        websocket: {}, //websocket对象
        chat_data: [//聊天数据
          
        ],
      },
      // 聊天组=私聊+群聊
      chat: [
        {
        type: "grounp", //会话方式:person  grounp
        name: "公共群聊", //名称
        nickName: "ichat", //会话昵称
        avatar: "https://cdn.quasar.dev/img/avatar.png", //头像
        status: true, //会话状态
        ws_addr: "ws://103.150.181.219:8005", //ws地址
        secret: "public_ichat", //通讯秘钥
        ID: "234234", //聊天seesion
        websocket: {}, //websocket对象
        chat_data: [//聊天数据
          
        ],
      },
      ], 
      bar: false,
    };
  },
  mounted() {
    //this.$q.sessionStorage.set("chat_arr", []);
    if (this.$q.sessionStorage.has("chat_arr")) {
      this.chat = this.$q.sessionStorage.getItem("chat_arr");
    }
  },
  created () {
    // this.$q.addressbarColor.set('#74ebd5');
    // this.$q.fullscreen.request()
    // .then(() => { // v1.5.0+
    //   // success!
    // })
    // .catch(err => { // v1.5.0+
    //   // oh, no!!!
    // })

  },
  methods: {
     show (grid) {
      this.$q.bottomSheet({
        title: '工具箱',
        grid,
        actions: [
          {
            label: '在线互传',
            img: transmission_icon,
            id: 'transmission'
          },
          {
            label: '在线自习室',
            img: study_icon,
            id: 'transmission'
          }
        ]
      }).onOk(action => {
        // 文件在线传输
        if(action.id == "transmission") {
          this.tool = !this.tool;
          this.tool_name = action.label;
        }
        // console.log('Action chosen:', action.id)
      }).onCancel(() => {
        // console.log('Dismissed')
      }).onDismiss(() => {
        // console.log('I am triggered on both OK and Cancel')
      })
    },

     onLoad (index, done) {
        if (this.chat) {
          // this.chat.push({}, {}, {}, {}, {}, {}, {})
          done()
        }

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
      if (this.chat.push(this.add_chat)) {
        this.index = this.chat.indexOf(this.add_chat);
        // 更新
        this.$q.notify({
          message: `添加[${this.add_chat.name}]会话成功!`,
          color: "purple",
          icon: "chat_bubble",
          position: "top",
        });
      }
      this.$q.sessionStorage.set("chat_arr", this.chat);
      console.log("-------1------");
      console.log(this.$q.sessionStorage.getItem("chat_arr"))
    },
    connection() {
      this.openAddChat();
      // 跳转
      this.$router.push({path: `/chat/${this.index}`})
    },
    // openAddChat()
    openAddChat() {
      this.bar = !this.bar;
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
.main {
  position: relative;
  width: 100%;
  height: 100%;

  background-color: green;
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


.fun1 {
  position: relative;
  width:100%;
  height:100vh;
  background-color:red;
}

.phone {
  width: 100%;
  height: auto;
  background-color: green;
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

.function {
  position: relative;
  width: 100%;
  height: 60px;
  /* background-color: pink; */
}
.add {
  position: absolute;
  left: 34.4%;
  width: 60px;
  height: 60px;
  margin: -20px auto;
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

.nickName {
  margin-left: -5px;
  font-size: 15px;
}

.add-chat {
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

.item-chat {
  width: 100%;
  height: 70px;
  border-bottom: 1px solid;
  border-color: rgba(0,0,0,0.12);
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
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
}
.aaa {
  width: 100%;
}
.add-some-icon:hover {
  color: #1976d2;
}

.tt {
  width: 100%;
  height: 10px;
  padding-left: 5.5%;
  margin-bottom: 40px;
  color: rgba(0,0,0,0.54);
  font-size: 10px;
  /* margin-left: 20px; */
}

.gradient-1 {
   /* background-image: linear-gradient(to bottom, #f7ecf2, #faedee, #faf0ec, #f7f2ec, #f4f5ef, #f2f5f0, #f0f6f1, #eef6f3, #ebf5f2, #e9f5f2, #e6f4f2, #e3f3f2); */

   background-image: linear-gradient(to bottom, #f7ecf2 0%, white 100%);
   /* background-image: linear-gradient(to top, #00dbde 0%, #fc00ff 100%); */
   /* background-image: linear-gradient(-20deg, #ddd6f3 0%, #faaca8 100%, #faaca8 100%); */
}
</style>
