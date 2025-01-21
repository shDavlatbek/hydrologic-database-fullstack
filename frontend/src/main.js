import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import "@tabler/core/dist/css/tabler.min.css"
import '@tabler/core/dist/js/tabler.min.js';
import './style/main.css'
import VueApexCharts from "vue3-apexcharts";
import themePlugin from "./plugins/themePlugin";
import PrimeVue from 'primevue/config';
import { GlobalPreset } from './prime-preset';

createApp(App).use(PrimeVue, {
  theme: {
    preset: GlobalPreset,
    options: {
      darkModeSelector: '.dark-theme',
    }
  },
  locale: {
    monthNames: ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avgust', 'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr'],
    monthNamesShort: ['Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyun', 'Iyul', 'Avg', 'Sen', 'Okt', 'Noy', 'Dek'],
  }
}).use(router).use(themePlugin).use(VueApexCharts).mount("#app");