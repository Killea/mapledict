import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'

import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'

import axios from 'axios'
Vue.prototype.$http = axios;



// 设置语言
locale.use(lang)

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')
