import Vue from 'vue'
import App from './App.vue' // 🔥 Ensure this import exists
import vuetify from './plugins/vuetify' // Ensure Vuetify is imported

Vue.config.productionTip = false;

new Vue({
  vuetify,
  render: h => h(App), // Ensure App is used correctly
}).$mount('#app');
