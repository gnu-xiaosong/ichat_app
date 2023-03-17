/*
 * @Author: xskj
 * @Date: 2023-03-01 18:06:12
 * @LastEditors: xskj
 * @LastEditTime: 2023-03-17 22:03:41
 * @Description: 
 */
import Vue from 'vue'
import axios from 'axios'
import Contextmenu from "vue-contextmenujs"
Vue.use(Contextmenu);
import VueTypedJs from 'vue-typed-js'
Vue.use(VueTypedJs)
//axois设置
const instance = axios.create({
    baseURL: '/api',
    // baseURL: '/public/index.php',
    timeout: 100000,
    headers: {
        'X-Custom-Header': 'foobar',
    }
});

//axois设置
const instance1 = axios.create({
    // baseURL: '/file',
    // baseURL: 'http://10.181.20.176:5000',
    timeout: 100000,
    headers: {
        'X-Custom-Header': 'foobar',
    }
});

Vue.prototype.$axios = instance
Vue.prototype.$axios1 = instance1

