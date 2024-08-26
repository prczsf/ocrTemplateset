// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'ant-design-vue/dist/reset.css';
import Antd from 'ant-design-vue';

import CKEditor from '@mayasabha/ckeditor4-vue3';
const app = createApp(App)

app.use(router).use(ElementPlus).use(Antd).use( CKEditor )

app.mount('#app')
