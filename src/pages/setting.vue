<template>
  <q-page padding>
    <!-- 存储设置 -->
    <!-- 标题 -->
    <div class="seting-title">存储设置</div>
    <!-- 正文 -->
    <div class="setting-content">
        <div class="col center">
          方式: 
          <q-radio v-model="storage" val="officia" label="官方" />
          <q-radio v-model="storage" val="qiniu" label="七牛云" />
          <!-- <q-radio v-model="storage" val="aliyun" label="阿里云" /> -->
          <q-radio v-model="storage" val="customer" label="自定义" />
        </div>
        <!-- 七牛云
        <div class="col">
          <q-input v-model="qiniu.accessKey" item-aligned dense>
            <template v-slot:before>
              <span style="font-size:12px">accessKey:</span> 
            </template>
          </q-input>
           <q-input v-model="qiniu.secretKey" item-aligned dense>
            <template v-slot:before>
              <span style="font-size:12px">secretKey:</span> 
            </template>
          </q-input>
           <q-input v-model="qiniu.bucket" item-aligned dense>
            <template v-slot:before>
              <span style="font-size:12px">bucket:</span> 
            </template>
          </q-input>
        </div> -->
        <!-- <q-dialog v-model="qiniuIs" persistent>
          <q-card style="width: 300px" class="q-px-sm q-pb-md">
            <q-card-section>
              <div class="text-h6">七牛云</div>
            </q-card-section>

            <q-item-label header>accessKey</q-item-label>
            <q-item dense>
              <q-item-section avatar>
                <q-icon name="vpn_key" />
              </q-item-section>
              <q-item-section>
                 <q-input v-model="qiniu.accessKey" dense />
              </q-item-section>
            </q-item>

            <q-item-label header>secretKey</q-item-label>
            <q-item dense>
              <q-item-section avatar>
                <q-icon name="security" />
              </q-item-section>
              <q-item-section>
                <q-input v-model="qiniu.secretKey" dense />
              </q-item-section>
            </q-item>

            <q-item-label header>bucket</q-item-label>
            <q-item dense>
              <q-item-section avatar>
                <q-icon name="space_dashboard" />
              </q-item-section>
              <q-item-section>
                <q-input v-model="qiniu.bucket" dense />
              </q-item-section>
            </q-item>

             <q-item-label header></q-item-label>
             <q-item dense class="center1">
                <q-btn @click="saveQiniu()" color="primary"  label="保存" />
             </q-item>
          </q-card>
        </q-dialog> -->
    </div>
  </q-page>
</template>

<script>
export default {
  // name: 'PageName',
  data() {
    return {
      storage: 'officia',
      qiniuIs:true,
      qiniu: {
        accessKey: "WKQvTXLbnSOJePjOprnLv7m9bFwsnG0oIILyYGiF",
        secretKey: "ZdS4FqEW8-ZHKoXI55i-2SBmoWS3PQcJ8WiIXM4J",
        bucket:   "chatskj"
      }
    }
  },
  methods: {
    saveQiniu() {
      this.$q.localStorage.set("qiniu", this.qiniu);
      this.qiniuIs = !this.qiniuIs;
    }
  }
}
</script>

<style scoped>
.seting-title {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80%;
  height: 40px;
  margin:  auto;
  /* background-color: pink; */
}
.setting-content {
  width: 100%;
  height: 300px;
  /* background-color: green; */
  margin: 10px auto;
}

.center {
  display: flex;
  align-items: center;
}

.center1 {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>