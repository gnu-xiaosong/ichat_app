<template>
  <div class="transmission">
    <!-- <q-card class="bg-primary text-white" style="width: 700px; max-width: 80vw;margin:50px auto"> -->
      <q-card-section class="q-pt-none" style="margin-top:70px">
        <div class="add-chat">
          <div class="row">
              <!-- 名称 -->
              <q-input
                filled
                bottom-slots
                item-aligned
                v-model="add_chat.nickName"
                dense
                class="aaa"
              >
                <template v-slot:before >
                  <span style="font-size:10px">名称</span> 
                </template>
              </q-input>

              <!-- 传输秘钥秘钥 -->
              <q-input
                filled
                bottom-slots
                v-model="add_chat.secret"
                dense
                item-aligned
                class="aaa"
              >
                <template v-slot:before >
                  <span style="font-size:10px">配对密钥</span> 
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
              <!-- 服务器地址 -->
              <q-input
                filled
                item-aligned
                bottom-slots
                v-model="add_chat.ws_addr"
                dense
                class="aaa"
                label="默认全局"
              >
                <template v-slot:before>
                  <span style="font-size:10px">服务器 </span> 
                </template>
              </q-input>
          </div>
        </div>
      </q-card-section>

      <q-card-section style="text-align: center;margin-top:15px">
        <q-btn @click="valid_key()"   
        round  size="xl"  color="purple" icon="connect_without_contact"/>
        <q-btn  
        round 
        :loading="loading1"
        :percentage="percentage1"
        @click="startComputing(1)"
        style="margin-left:10px" 
        color="secondary" 
        size="xl" 
        icon="send" />
      </q-card-section>

      <q-card-section style="text-align: center; height:auto">
           <div class="radar" id="radar"></div>
      </q-card-section>
      
      <!-- 接受文件进度显示 -->
      <q-card-section v-if="isShow">
         <q-slider
            v-model="percentage"
            :min="0"
            :max="100"
            label
            color="light-green"
          />
      </q-card-section>

    <!-- </q-card> -->
  </div>
</template>

<script>
import radar from '../assets/lottie/animation-bluetooth.json';
import lottie from 'lottie-web';
import download1 from 'src/utils/download';

export default {
  // name: 'ComponentName',
  data () {
    return {
      timer:null,
      isShow:false,
      percentage:0,
      radar,
      loading1: false,
      percentage1: 0,
      iinline_status: 1,
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
    }
  },
  mounted() {
  },
  beforeDestroy () {
    clearInterval(this.interval1);
  },
  methods: {
     // 文件下载
    download(file_url) {
      let file_name = file_url.split('/')[file_url.split('/').length-1]
      console.log(file_name);
       this.$q.dialog({
        title: '是否接受对方文件',
        message: `${file_name}`,
        ok: {
          push: true,
          label: "下载"
        },
        cancel: {
          push: true,
          label: "取消",
          color: 'negative'
        },
        persistent: true
      }).onOk(() => {
        console.log('>>>> OK');
        // this.downloadZip(file_url, file_name);
        // download1(file_url, file_name, "text/plain");
        let e = document.createElement("a");
        e.href = file_url;
        e.target = '_blank';
        e.click();
      }).onCancel(() => {
        console.log('>>>> Cancel');
        return true;
      }).onDismiss(() => {
      });
    },
    startComputing(id) {
      let fileEle = document.createElement("input");
      fileEle.type = "file";
      fileEle.onchange = () => {  
        console.log(fileEle.files[0]);
        let fileData = new FormData();
        fileData.append("file", fileEle.files[0]);
        this.$axios1.post("http://103.150.181.219:5000/uploadFile", fileData).then((res) => {
          this.send_file(res.data);
        })
        this[`loading${id}`] = true
        this[`percentage${id}`] = 0
      }
      // 点击获取文件
      fileEle.click();
      
      // 上传成功以后
      this[`interval${id}`] = setInterval(() => {
        this[`percentage${id}`] += Math.floor(Math.random() * 8 + 10)
        if (this[`percentage${id}`] >= 100) {
          clearInterval(this[`interval${id}`])
          this[`loading${id}`] = false
        }
      }, 700)
    },
    generat() {
      var secret = new Date().getTime() + Math.random().toString(36).substr(2);
      this.add_chat.secret = secret;
    },
    conn() {
        var ws = new WebSocket(this.add_chat.ws_addr);
        // 连接成功回调处理
        let _this = this;
        ws.onopen = function () {
          let config = `{"secret_key":"transmission-${_this.add_chat.secret}","nickName": "${_this.add_chat.nickName}"}`;
          // 设置会话秘钥,
          ws.send(config);
          _this.ws = ws;
        };

        // 监听数据-->接收数据
        ws.onmessage = function (evt) {
          var a = evt.data.replace(/'/g, '"');
          var data = JSON.parse(a);

          if (data.type == "connect") {
            // 连接成功
            console.log("连接状态:");
            console.log(data.msg);
            _this.iinline_status = 0;
          } else if (data.type == "config") {
            console.log("配置设置:");
            console.log(data.msg);

            let authentication = "";
            // 循环发送配对请求
            clearInterval(_this.timer);
            _this.timer = setInterval(() => {
              console.log("发送配对请求");
              // 接受配对请求命令
              let msg_obj = `{"type":"valid_key","data":"transmission-${_this.add_chat.secret}","authentication": "${authentication}"}`;
              _this.ws.send(msg_obj);
            }, 500);
          } else if (data.type == "valid_key") {
            // 正常消息
            console.log("配对结果:");
            console.log(data);
            if (data.msg.replace(/^transmission-/, '') == _this.add_chat.secret) {
              // 配对成功 销毁动画
              _this.radar_animation.destroy();
              _this.$nextTick(() => {
                let e = document.getElementById("radar");
                e.innerHTML = `<span>已配对用户:${data.nickName}</span>`;
              });
              let authentication = "";
              // 发送配对请求成功信息
              let msg_obj = `{"type":"valid_conn_success","data":"与${_this.add_chat.nickName}配对成功","authentication": "${authentication}"}`;
              _this.ws.send(msg_obj);
              // alert("ok")
            }
          } else if(data.type == "transmission") {
            // 正常传输文件
            console.log("接受文件:")
            console.log(data);
            // alert(data.msg);
            _this.isShow = true;
            _this.download(data.msg.replace(/url-/,''));
          } else if(data.type == "valid_conn_success") {
            // 配对成功请求
            
            console.log("配对成功请求");
            window.clearInterval(_this.timer);
            _this.timer = null;
            
            console.log(data);
            // alert("ok")
          }
        }

        ws.onclose = function () {
          _this.iinline_status = 1;
          // 关闭 websocket
        };
    },
    // 发起配对请求验证连接
    valid_key() {
      // 显示动画
      this.$nextTick(() => {
        this.radar_animation = lottie.loadAnimation({
          container: document.getElementById('radar'), // 绑定dom节点
          renderer: 'svg', // 渲染方式:svg、canvas
          loop: true, // 是否循环播放，默认：false
          autoplay: true, // 是否自动播放, 默认true
          animationData: radar // AE动画使用bodymovie导出为json数据
        });
        this.radar_animation.setSpeed(2);
      });
      // 连接
      this.conn();
    },
    send_file(data) {
      let authentication = "";
      // 接受配对请求命令
      let msg_obj = `{"type":"transmission","data":"url-${data}","authentication": "${authentication}"}`;
      try {
        this.ws.send(msg_obj);
        this.$q.notify({
          message: '传输成功!',
          icon: 'announcement'
        })
      } catch (error) {
        this.$q.notify({
          message: "传输失败！",
          icon: 'announcement'
        })
      }

      this.loading1 = false;
      this.percentage1 = 0;
    },
    // 开始传输
    transmission() {
      let data = "http://www.xskj.store";
      this.send_file(data);
    }
  }
}
</script>


<style scoped>
.transmission {
  margin:5px;
}



.radar {
  width:100%;
  height: 200px;
  /* background-color: pink; */
}

.aaa {
  width: 90%;
}
</style>
