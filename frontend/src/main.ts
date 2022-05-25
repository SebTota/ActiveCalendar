import { createApp } from 'vue'
import App from './App.vue'
import VueCookies from 'vue-cookies'
import router from './router'
import { createPinia } from 'pinia'
import axios from 'axios'
import Constants from '@/constants/constants'

const pinia = createPinia()

if (process.env.NODE_ENV === 'development') {
  axios.defaults.baseURL = Constants.API_BASE_PATH
}

createApp(App).use(router).use(VueCookies).use(pinia).mount('#app')
