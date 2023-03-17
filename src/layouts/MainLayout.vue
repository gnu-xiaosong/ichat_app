<template>
  <q-layout>
    <router-view></router-view>
  </q-layout>
</template>

<script>
export default {
  name: "MainLayout",
  data() {
    return {
    
   }
  },
};
</script>

<style>
.ban {
  width: 100%;
  height: 100%;

  background-color: pink;
}
 /*滚动条样式*/
#scroll::-webkit-scrollbar {
    width: 4px;    
    height: 4px;
}
#scroll::-webkit-scrollbar-thumb {
    border-radius: 10px;
    -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
    background: rgba(0,0,0,0.2);
}
#scroll::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 5px white;
    border-radius: 0;
    background: #ffffff;
}
</style>
