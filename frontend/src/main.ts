import { createApp } from 'vue'
import App from './App.vue'
import VueCookies from 'vue-cookies'
import router from './router'
import { createPinia } from 'pinia'
import axios from 'axios'

const pinia = createPinia()

createApp(App).use(router).use(VueCookies).use(pinia).mount('#app')
