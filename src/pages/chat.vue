<template>
  <div class="chat-main">
    <q-header elevated class="bg-secondary text-white fix-top">
      <q-toolbar>
        <q-toolbar-title>
          <q-btn
            flat 
            round 
            dense
            @click="$router.go(-1)"
            icon="arrow_back_ios_new"
          />
          </q-toolbar-title>
          <q-space/>
          <q-btn-dropdown unelevated :ripple="false" style="background-color:transparent" :label="win_chat">
            <q-list>
              <q-item clickable v-close-popup @click="openChat(1)">
                <q-item-section>
                  <q-item-label>{{inline_chat.name}}</q-item-label>
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup @click="openChat(0)">
                <q-item-section>
                  <q-item-label>ai chat</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>

          <q-space/>
          <q-btn flat round dense icon="wifi_tethering"    v-if="iinline_status==0"  color="positive"  />
          <q-btn flat round @click="reconn()"  v-if="iinline_status==1" dense icon="wifi_tethering_off"  color="red"  />
          <q-spinner-ios
            v-if="iinline_status==2"
            color="purple"
            size="1.5em"
          />
        <q-btn flat round dense icon="more_vert" >
          <q-menu fit>
            <q-list style="min-width: 100px">
              <q-item clickable>
                <q-item-section @click="isBg=!isBg">样式设置</q-item-section>
              </q-item>
              <q-separator dark />
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container>
        <div class="chat">
          <!-- 聊天 -->
          <div class="scroll chat_win" id="scroll">
            <!-- 标题 -->
            <!-- <q-chat-message class="fixed-center" label="Sunday, 19th" >
              <template v-slot:default >
                <q-spinner-comment
                  color="primary"
                  size="2em"
                />
              </template>
            </q-chat-message> -->
            <q-chat-message
            
              v-for="(item, index) in chat_receive"
              :key="index"
              size="10"
              :sent="item.send"
              :label="item.label"
              text-color="white"
              bg-color="transparent"
            >
              <template v-slot:default >
                <div :class="
                item.send==true?'msg bg-white shadow-1 text-1':
                chat_mode==0?'sendmsg bg-white  shadow-1 text-1':'msg1 bg-white shadow-1 text-1'
                ">
                  <!-- 普通消息 -->
                  <div id="msg" :class=" item.send==false?'msg1-text scroll':'msg-text'" v-if="item.type=='text'" >
                      <!-- 打字机效果 -->
                      <span v-if='item.send==true' id="no1">
                        {{ item.msg }}
                      </span>
                      <div v-else-if='item.send==false && chat_mode==1' style="padding:10px;min-height:50px;">{{ item.msg }}</div>
                      
                       <vue-typed-js
                          v-else
                          class="desc"
                          :strings="[compiledMarkdown(item.msg)]"
                          :loop="false"
                          :startDelay="0"
                          :typeSpeed="30"
                          @onComplete="onComplete"
                        >
                          <span class="typing"></span>
                        </vue-typed-js>

                  </div>
                  <!-- 图片信息 -->
                  <div class="msg-pic"   v-if="item.type=='picture'">
                      <q-img
                        :src="item.msg"
                        style="width: 100%;height:100%"
                        :ratio="1"
                        basic
                        v-if="img"
                        spinner-color="white"
                        @click="fullscreen()"
                        class="rounded-borders"
                      >
                      </q-img>
                        <q-img
                        v-else
                        :src="item.msg"
                        style="width: 100%;height:100%"
                        :ratio="1"
                        basic
                        spinner-color="white"
                        @click="fullscreen()"
                        class="rounded-borders fullscreen"
                      >
                      </q-img>
                  </div>
                  <!-- 视频信息 -->
                  <div class="msg-video" v-if="item.type=='video'">
                     <video
                        id="videoA"
                        controls
                        style="width:100%;height:100%;object-fit:fill;border-radius:3px"
                        :src="item.msg" 
                      >
                       你的设备不支持视频。
                     </video>
                  </div>
                  <!-- 音频信息 -->
                  <div class="msg-audio" v-if="item.type=='audio'">
                      <div class="row">
                        <div class="col-12 center">
                            <img v-if="item.audio==false" @click="startsound(0,index, item)"  width="30px" src="../assets/Sound-wave.svg" alt="">
                            <q-spinner-bars
                              color="grey-9"
                              size="2.3em"
                              @click="startsound(1, index, item)"
                              v-else
                            />
                        </div>
                      </div>
                  </div>
                  <!-- 其他信息 -->
                  <div class="msg-other" v-else>
                       <q-spinner-comment
                          v-if="Issend==true && (chat_receive.length-1) == index"
                          color="primary"
                          size="2em"
                          class="absolute-bottom-right"  
                        />

                         <!-- <q-icon v-if="Issend == 0" name="warning" class="text-red" style="font-size: 2rem;" /> -->
                  </div>
                </div>   
              </template>
              <template v-slot:name>
                <div class="chat-name">
                  <span>{{ item.name }}</span>
                </div>
              </template>
              <template v-slot:avatar>
                <img
                  style="margin-right: 3px"
                  v-if="item.send == true"
                  class="q-message-avatar q-message-avatar--sent shadow-4"
                  src="https://cdn.quasar.dev/img/avatar4.jpg"
                />
                <img
                  v-else-if="typeof item.ai == undefined || item.ai==null"
                  style="margin-right: 3px"
                  class="q-message-avatar q-message-avatar--sent shadow-4"
                  src="https://cdn.quasar.dev/img/avatar3.jpg"
                />
                <img
                  v-else
                   style="margin-right: 3px"
                  class="q-message-avatar q-message-avatar--sent shadow-4"
                  src="../assets/robot.svg"
                />
                
              </template>
            </q-chat-message>
          </div>
        </div>
    </q-page-container>

    <q-footer elevated  class="bg-white text-white fix-bottom">
        <q-linear-progress indeterminate v-if="slider" class="q-mt-md" />
        <div class="row xs-center">
          <div class="col xs-center"> 
                <div class="row">
                  <div class="col">
                     <q-btn text-color="primary" :ripple="false" flat round @click="footerHeight=footerHeight==200?0:200"  size="17px"  icon="add_circle" />
                  </div>
                  <div class="col">
                    <q-btn text-color="primary" :ripple="false" flat round   size="17px"  icon="sentiment_very_satisfied">
                       <q-menu
                          transition-show="jump-down"
                          transition-hide="jump-up"
                        >
                          <emoji-picker  @emoji-click="handleEmojiClick"></emoji-picker>
                        </q-menu>
                    </q-btn>
                  </div>
                </div>
          </div>
          <div class="col-8 xs-center" style="padding:6px">
             <div class="text">
              <!-- 文本框 -->
              <div class="txet_input">
                <q-input
                  v-model="msg"
                  clearable
                  standout
                  bg-color="grey-4"
                  rounded 
                  outline
                  dense
                  
                  @keydown.enter="enterSend1()"
                />
                  
              </div>
            </div>
          </div>
          <div class="col-2 xs-center">
             <q-btn unelevated rounded color="primary" @click="sendMsg1()" label="发送" />
          </div>
        </div>
        <!-- 底部工具栏 -->
        <div class="footer-tool" :style="'height:'+footerHeight +'px'">
            <q-carousel
              transition-prev="slide-right"
              transition-next="slide-left"
              animated
              swipeable
              v-model="slide"
              ref="carousel"
              infinite
            >
              <q-carousel-slide :name="1">
                <div class="fun-1">
                    <div class="fun-item" @click="openItem(item)" v-for="item,index in fun" :key="index">
                      <div>
                        <q-icon
                          size="lg"
                          :name="item.icon"
                        />
                      </div>
                      <div>{{ item.name }}</div>
                    </div>
                </div>
              </q-carousel-slide>
               <q-carousel-slide :name="2">
                <div class="audio-1 bg-primary" ref="el"  @touchstart.prevent="goTouchstart" @touchend.prevent="goTouchend">
                   <img v-if="img1" src="../assets/录音.svg" width="100%" height="100%" alt="网络加载错误">
                   <img v-else src="../assets/录音1.svg" width="100%" height="100%" alt="网络加载错误">
                </div>
              </q-carousel-slide>
            </q-carousel>
        </div>
    </q-footer>

     <!-- 背景图片设置 -->
        <q-dialog v-model="isBg">
          <q-card>
            <q-toolbar>
              <q-avatar>
                <img src="../assets/logo.png">
              </q-avatar>
              <q-toolbar-title><span class="text-weight-bold">样式</span> </q-toolbar-title>
              <!-- <q-btn flat round dense icon="close" /> -->
            </q-toolbar>
            <q-card-section>
              <q-card>
                <q-tabs
                  v-model="tab1"
                  dense
                  class="text-grey"
                  active-color="primary"
                  indicator-color="primary"
                  align="justify"
                  narrow-indicator
                >
                  <q-tab name="bg" label="背景" />
                  <q-tab name="font" label="字体" />
                </q-tabs>

                <q-separator />

                <q-tab-panels v-model="tab1" animated>
                  <q-tab-panel name="bg">
                      <div class="setbg">
                        <div v-for="item,index in imgs" :key="index" @click="setBg(index, item)">
                          <img :src="item" width="100%" height="100%" alt=""/>
                        </div>
                      </div>
                  </q-tab-panel>

                  <q-tab-panel name="font">
                      <div class="q-pa-md">
                        <div class="q-gutter-sm">
                          <q-radio v-for="item,index in font_select" :class="item.className" @input="changeFont"  :key="index"  v-model="shape" checked-icon="task_alt" unchecked-icon="panorama_fish_eye" :val="item.val" :label="item.name" />
                        </div>
                      </div>
                  </q-tab-panel>
                </q-tab-panels>
              </q-card>
            </q-card-section>
          </q-card>
        </q-dialog>
  </div>
</template>

<script>
import { date } from "quasar";
import 'emoji-picker-element';
import Recorder from 'js-audio-recorder';
// import VueMarkdown from 'vue-markdown'
// import { QMarkdown } from '@quasar/quasar-ui-qmarkdown'
// import Prism from "prismjs";
import bg1 from '../assets/bg/bg1.jpg'
import bg2 from '../assets/bg/bg2.jpg'
import bg3 from '../assets/bg/bg3.jpg'
import bg4 from '../assets/bg/bg4.jpg'
import bg5 from '../assets/bg/bg5.jpg'
import bg6 from '../assets/bg/bg6.jpg'
import bg7 from '../assets/bg/bg7.jpg'
import bg8 from '../assets/bg/bg8.jpg'
import bg9 from '../assets/bg/bg9.jpg'
import bg10 from '../assets/bg/bg10.jpg'

import marked from 'marked'
export default {
  name: "MainLayout",
   components: {
    // QMarkdown
  },
  data() {
    return {
      font_select:[
        {
          name: "东方大楷",
          val: 0,
          className: "text-family-1"
        },
        {
          name: "进步字体",
          val: 1,
          className: "text-family-dd"
        },
        {
          name: "数黑字体",
          val: 2,
          className: "text-family-ali"
        },
        {
          name: "正常",
          val: 3,
          className: "text-normal"
        },
      ],
      shape:3,
      tab1:'bg',
      imgs:[
        bg1,
        bg2,
        bg3,
        bg4,
        bg5,
        bg6,
        bg7,
        bg8,
        bg9,
        bg10,
      ],
      isBg:false,
      type_is:true,
      Issend:false,
      img1: false,
      model: null,
      options: [
        'Google', 'Facebook', 'Twitter', 'Apple', 'Oracle'
      ],
      timer:null,
      img:true,
      slider:false,
      fun: [
        {
          label: "picture",
          name: "图片",
          icon:"add_photo_alternate "
        },
         {
          label: "video",
          name: "视频",
          icon:"video_library"
        },
         {
          label: "audio",
          name: "翻译",
          icon:"translate"
        },
      ],
      slide: 1,
      footerHeight:0,
      audioSrc:"", //音频地址
      soundIs:true,
      iinline_status:0,  //0 开 1 关 2 等待
      online_chat: {
        type: "person", //会话方式:person  grounp
        name: "会话窗口", //名称
        nickName: "", //会话昵称
        avatar: "account_circle", //头像
        status: true, //会话状态
        ws_addr: "ws://10.181.21.119:8005", //ws地址
        secret: "xskj", //通讯秘钥
        ID: "234234", //聊天seesion
        chat_data: [//聊天数据
          
        ],
      },
      msgType: 'audio' ,  //消息类型: 普通消息-text 视频-video 音频-audio 图片-picture
      chat_arr:[{
        type: "person", //会话方式:person  grounp
        name: "会话窗口", //名称
        nickName: "", //会话昵称
        avatar: "account_circle", //头像
        status: true, //会话状态
        ws_addr: "ws://10.181.21.119:8005", //ws地址
        secret: "xskj", //通讯秘钥
        ID: "234234", //聊天seesion
        websocket: {}, //websocket对象
        chat_data: [//聊天数据
          
        ],
      }
      ],
      win_chat:"",
      img:false,
      chat_receive:[],
      msg: "",
      fabCenter: false,
      splitterModel: 25,
      insideModel: 80,
      submitting: false,
      public_ws_url: "ws://localhost:8005",
      chat_type: "person",
      bar: false,

      chat_mode: 1 //0 常规聊天 1 ai聊天
    };
  },
  mounted() {
     // 获取chat对象数组的index，索引
    this.index = this.$route.params.index;

    // 获取目标chat：活跃chat
    this.chat_arr = this.$q.sessionStorage.getItem("chat_arr");
    
    this.$nextTick(() => {
      this.inline_chat = this.$q.sessionStorage.getItem("chat_arr")[this.index];
      this.win_chat = this.$q.sessionStorage.getItem("chat_arr")[this.index].name;
      // 连接会话
      this.conn_chat();
    });

  },
  methods: {
    changeFont(index) {
      console.log(this.font_select[index]);
      this.$nextTick(() => {
        let ele = document.getElementById("msg");
        let ele2 = document.getElementById("no1");
        let ele1 = document.getElementsByClassName("desc")[0];
        ele.className = `msg-text ${this.font_select[index].className}`;
        ele1.className = `${this.font_select[index].className}`;
        ele2.className = `${this.font_select[index].className}`;
        // ele.classList.add(this.font_select[index].className);
      })
    },
    setBg(index,item){
      let es = document.querySelectorAll(".setbg>div");
      for(let i=0; i<es.length ;i++){
        es[i].style.border = "none";
      }
      es[index].style.border = "2px solid blue";

      let s = document.getElementById("scroll");
      s.style.background = `url(${item}) center center `;
      s.style.backgroundSize = '100% 100%'
    },
    compiledMarkdown : function (data) {
      let outHtml = marked.parse(data)
      // 代码处理
      outHtml = outHtml.replace("<pre>", "<pre style='padding:5px;border-radius:5px;background-color:black;font-weight:600;color:white'>")
      // console.log(outHtml);
      return outHtml;
    },
    onStart() {
      alert("ok");
      this.type_is = !this.type_is;
      this.scrollFooter();
    },
    onComplete() {
      // alert("ok")
      this.type_is = !this.type_is;
      this.scrollFooter();
    },
    recover() {
      this.img = !this.img;
    },
    // 开始长按
    goTouchstart() {
        // 获取对象
      let el = this.$refs.el; 
      el.className = "audio-1 bg-primary border";
      this.img1 = !this.img1;
      if (el.type == "click") {
        return;
      }
      let _this = this;
      this.timer = setTimeout(() => {
        console.log("长按事件");
        _this.recorder = new Recorder({
                sampleBits: 16,                 // 采样位数，支持 8 或 16，默认是16
                sampleRate: 16000,              // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
                numChannels: 1,                 // 声道，支持 1 或 2， 默认是1
        });
        //  开始录音
        console.log("start recorder.......");
        _this.recorder.start();
      }, 500);
    },
    // 长按结束
    goTouchend() {
      let el = this.$refs.el; 
      el.className = "audio-1 bg-primary";
      this.img1 = !this.img1;
      // 结束录音
      this.recorder.stop();
      console.log("recorder end!");
      let wav = this.recorder.getWAVBlob();
      console.log("录音数据:");
      // 上传
      this.uploadWav(wav, "audio");
      console.log(wav);
      this.timer = null;
    },
    fullscreen() {
      this.img = !this.img;
    },
    // 上传到官方存储
    uploadFile(type) {
        let fileEle = document.createElement("input");
        fileEle.type = "file";
        // 点击获取文件
        fileEle.click();
        this.slider = true;
        // 上传文件获取连接
        fileEle.onchange = () => {  
          console.log(fileEle.files[0]);
          let fileData = new FormData();
          fileData.append("file", fileEle.files[0]);
          this.slider = true;
          this.$axios1.post("http://103.150.181.219:5000/uploadFile", fileData).then((res) => {
            this.msgType = type;
            this.msg = res.data;
            this.slider = false;
            this.send1();
            this.msg = "";
            this.scrollFooter();
          })
        }
    },
     // 上传到官方存储
    uploadWav(wav, type) {
          let fileData = new FormData();
          fileData.append("file", wav);
          this.slider = true;
          this.$axios1.post("http://103.150.181.219:5000/uploadFile", fileData).then((res) => {
            this.msgType = type;
            this.msg = res.data;
            this.slider = false;
            this.send1();
            this.msg = "";
            this.scrollFooter();
          }).catch((e) => {
            this.slider = false;
         })
    },
    // chat窗口打开
    openChat(i) {
      if (i == 0) {
        // ai chat
        this.win_chat = "AI chat";
        this.chat_mode = 0;
      } else if (i == 1) {
        // 常规聊天
        this.win_chat = this.inline_chat.name;
        this.chat_mode = 1;
      }
    },
    // 打开功能
    openItem(item) {
      if (item.label == "picture") {
        // 上传文件(包括图片文件压缩包等)
        this.uploadFile(item.label);
      } else if (item.label == "video") {
        this.uploadFile(item.label);
      }else if (item.label == "audio") {
        this.goTouchstart();
      }
    },
    handleEmojiClick(e) {
      this.msg += e.detail.unicode;
      console.log(e);
    },
    insert(emoji) {
      this.input += emoji
    },
    startsound(i,index, item) {
      let url = item.msg;

      if (i == 0) {
        // 播放
        this.audioObj = new Audio(url);
        this.chat_receive[index].audio = !this.chat_receive[index].audio;
        /* 音频可以播放；如果权限允许则播放 */
        let playPromise = this.audioObj.play();
        if (playPromise !== undefined) {
            playPromise.then(() => {
                audio.play()
            }).catch(()=> {
              console.log("窗户错了")
            })
        }
      } else {
        // 暂停
        this.audioObj.pause();
        this.audioObj = null;
        this.chat_receive[index].audio = !this.chat_receive[index].audio;
      }
      
    },
    reconn() {
      this.iinline_status = 2;
      this.cron_chat(this.inline_chat);
    },
    conn_chat() {
      // 连接
      this.iinline_status = 1;
      this.cron_chat(this.inline_chat);
    },
    // 监听聊天信息
    cron_chat(chat_item) {
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
            _this.iinline_status = 0;
            _this.aliveWebsocket = ws;
          } else if (data.type == "config") {
            console.log("配置设置:");
            console.log(data.msg);
          } else {

            console.log("返回消息:");
            console.log(data.type);
            // 正常会话  
            // 添加进会话聊天数组中
            _this.inline_chat.chat_data.push({
              type: data.type, //消息类型: 普通消息-text 视频-video 音频-audio 图片-picture
              audio: false,
              name: data.nickName, //昵称
              time: data.send_time, //时间
              send: false, //是否为发送者：false or true
              msg:  data.msg, //消息内容
              label: "", //标签
            });

            console.log("有新消息了!");
            console.log(data);
            _this.audioSrc = data.msg;
            _this.chat_receive.push({
              type: data.type, //
              audio: false,
              name: data.nickName, //昵称
              time: data.send_time, //时间
              send: false, //是否为发送者：false or true
              msg: data.msg, //消息内容
              label: "", //标签
            });
            // 更新session存储
            
          let new_chat = _this.$q.sessionStorage.getItem("chat_arr");
          _this.chat_arr = new_chat;
          new_chat[_this.index] = _this.inline_chat;
          _this.$q.sessionStorage.set("chat_arr", new_chat);
          }
          _this.scrollFooter();
        };
        ws.onclose = function () {
          _this.iinline_status = 1;
          // 关闭 websocket
          _this.$q.notify({
            message: `与[${chat_item.name}]服务器连接中断!`,
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
    sendMsg1() {
      this.send_text();
      this.audioSrc = this.msg;
      this.msg = "";
      this.scrollFooter();
    },
    scrollFooter() {
      this.$nextTick(() => {
        var div = document.getElementById('scroll');;
        div.scrollTop = div.scrollHeight;
      });
    },
    enterSend1() {
      this.send_text();
      this.scrollFooter();
      this.msg = "";
    },
    send_text() {
      this.msgType = 'text';
      this.send1();
    },
    // 请求ai
    async getAiChat(data) {
      const timeStamp = Date.now();
      let send_time = date.formatDate(timeStamp, "YYYY-MM-DD HH:mm:ss");
      let key = "xskj666";
      let _res={};
      await this.$axios1.get(`http://chat.xskj.store/chat?key=${key}&q=${data}`).then((res) => {
        _res = res.data;
      }).catch((err) => {
        this.Issend = 0;
      });
      console.log("ai result:");
      console.log(_res);

      let send_msg = {
          type: "text",
          audio: true,
          name: "AI chat", //昵称
          time: send_time, //时间
          ai:"ok",
          send: false, //是否为发送者：false or true  0 AI
          msg: _res.content, //消息内容
          label: "", //标签
        };
      // push进消息队列
      this.inline_chat.chat_data.push(send_msg);
      this.chat_receive.push(send_msg);
      // 更新session存储
      let new_chat = this.$q.sessionStorage.getItem("chat_arr");
      new_chat[this.index] = this.inline_chat;
      this.chat_arr = new_chat;
      this.$q.sessionStorage.set("chat_arr", new_chat);
      this.Issend = false;
    },
    send1() {
       // 发送时间
      const timeStamp = Date.now();
      let send_time = date.formatDate(timeStamp, "YYYY-MM-DD HH:mm:ss");
      if (this.chat_mode == 0) {
        this.Issend = true;
        this.iinline_status = 2;
        // ai chat 
        let data = this.msg;
        // 封装数据
        let send_msg = {
          type: "text",
          audio: true,
          name: this.inline_chat.nickName, //昵称
          time: send_time, //时间
          send: true, //是否为发送者：false or true
          msg: data, //消息内容
          label: "", //标签
        };
        // push进消息队列
        this.inline_chat.chat_data.push(send_msg);
        this.chat_receive.push(send_msg);
        // 更新session存储
        let new_chat = this.$q.sessionStorage.getItem("chat_arr");
        new_chat[this.index] = this.inline_chat;
        this.chat_arr = new_chat;
        this.$q.sessionStorage.set("chat_arr", new_chat);

        // 请求数据
        this.getAiChat(data);
        this.scrollFooter();
        this.msg = ""
        this.iinline_status=0
      } else {
        // 常规聊天      
        let authentication = "";
        let msg_obj = `{"type":"${this.msgType}","data":"${this.msg}","authentication": "${authentication}"}`;
        console.log(msg_obj);
        let send_msg = {
          type: this.msgType,
          audio: false,
          name: this.inline_chat.nickName, //昵称
          time: send_time, //时间
          send: true, //是否为发送者：false or true
          msg: this.msg, //消息内容
          label: "", //标签
        };
        // push进消息队列
        this.inline_chat.chat_data.push(send_msg);
        console.log("------发送数据--------");
        console.log(this.inline_chat);
        this.chat_receive.push(send_msg);
        // 更新session存储
        let new_chat = this.$q.sessionStorage.getItem("chat_arr");
        new_chat[this.index] = this.inline_chat;
        this.chat_arr = new_chat;
        this.$q.sessionStorage.set("chat_arr", new_chat);
        // 检测
        console.log("------------websocket--------------")
        console.log(this.aliveWebsocket);
        // 发送   
        try {
          this.aliveWebsocket.send(msg_obj);
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
      }
    },
  },
};
</script>

<style scoped>
.chat-main {
  position: relative;
  width: 100%;
  height: 100vh;

  background-color: #f1f3f4;
}

.fun {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 60px;
  background-color: red;
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
  width: 100%;
  height: calc(100vh - 10vh);
  margin: auto;
  /* background-color: green; */
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
  
  padding-bottom: 15vh;
  /* background-color: pink; */
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


.footer-tool {
  width: 100%;
  background-color: pink;
}
.txet_input {
  width: 100%;
  height: 80%;
  padding-left: 9px;
  color:black;
  /* background-color: pink; */
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
  /* background-color: red; */
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

.fix-bottom{
  position:fixed;
  bottom: 0;
}
.fix-top{
  position:fixed;
  top: 0;
}


.xs-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.xs-center-right{
  display: flex;
  justify-content:right;
  align-items: center;
}

.xs-center-left {
  display: flex;
  justify-content:left;
  align-items: center;
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


/* 消息样式 */
.msg1 {
  float: left;
  display: flex;
  align-items: center;
  width: 50%;
  height: auto;
  border-radius: 4px;
  /* background-color: red; */
}


.msg {
  float: right;
  display: flex;
  align-items: center;
  width: 50%;
  height: auto;
  border-radius: 5px 25px 0  5px;
  /* background-color: red; */
}
.sendmsg{
  display: flex;
  align-items: center;
  width: auto;
  height: auto;
  border-radius: 10px;
  padding: 7px;
}

/* 普通消息 */
.msg-text{
   display: flex;
  align-items: center;
  justify-content:left;
  min-height: 50px;
  padding: 8px;
 
}
.msg-audio{
  width: auto;
  height: 40px;
  display: flex;
  justify-content:center;
  align-items: center;
}

.msg-video{
  width: 100%;
  height: 200px;
  display: flex;
  justify-content:right;
  align-items: center;
}

.fun-item{
  width: 49px;
  height: 50px;
  /* background-color: pink; */
  float: left;
  
  margin: 15px;
  margin-left: 26px;
}

.fun-item >div:nth-child(1){
  width: 100%;
  height: 80%;
  display: flex;
  align-items: center;
  color: #1976d2;
  justify-content: center;
  /* background-color: pink; */
}

.fun-item >div:nth-child(2){
  width: 100%;
  height: 20%;
  text-align: center;
  color: black;
  /* background-color: red; */
}


.fun-1{
  width: 80%;
  height: 80%;
  margin: auto;
  /* background-color: green; */
}

.center {
  width: 50%;
  height: 100%;
  display: flex;
  margin-left: 10px;
  justify-content: center;
  align-items: center;
  /* background-color: pink; */
}
.msg-pic{
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 200px;
}

.chat-name{
  margin-top:10px;
}

emoji-picker {
  width: 100%;
  height: 300px;
}

.audio-1 {
  width: 100px;
  height: 100px;
  padding: 20px;
  border-radius:50px;
  background-color: pink;
  margin: 30px auto;
}

.border {
  border: 6px solid rgb(197, 202, 233);;
}

.hightCode {
  width:200px;
  height:300px;

  background-color: black;
}

.setbg{
  width:100%;
  height:auto;
  /* background-color: pink; */
}

.setbg >div {
  float: left;
  width: 80px;
  height: 100px;
  /* background-color:red; */
  margin-left:11px;
  margin-bottom:10px;
  border-radius: 5px;
}



/* 特殊字体 */
.text-1 {
  color:black;
}
</style>



