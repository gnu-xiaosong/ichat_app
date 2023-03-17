<template>
<div>
     <!-- 桌面端 -->
    <div v-if="$q.platform.is.desktop" class="ban">
       <desktop></desktop>
    </div>
    <!-- 移动端 -->
    <div v-if="$q.platform.is.mobile" >
      <mobile></mobile>
    </div>
</div>
</template>

<script>
import Desktop from 'src/pages/desktop.vue';
import Mobile from 'src/pages/mobile.vue';
export default {
  name: "MainLayout",
  components: {
    Desktop,
    Mobile 
  },
  data() {
    return {
    };
  },
};
</script>



