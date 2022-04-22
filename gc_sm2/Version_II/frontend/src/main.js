import { createApp } from 'vue'
import App from './App.vue'
import router from "./router";
import "./assets/index.css";
import GcShow from "./plugins/gc-show";
import axios from 'axios'
import VueAxios from 'vue-axios'

const appInstance = createApp(App);
appInstance.use(VueAxios,axios)
appInstance.use(router);
appInstance.use(GcShow);
appInstance.mount("#app");


