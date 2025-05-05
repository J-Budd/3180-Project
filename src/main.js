import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// FontAwesome Icons
import { library } from '@fortawesome/fontawesome-svg-core'
import { faHeart as fasHeart } from '@fortawesome/free-solid-svg-icons'
import { faHeart as farHeart } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(fasHeart, farHeart)

// Axios base URL (adjust to match your backend port)
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// Add token to all requests if available
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(pinia)

// Register FontAwesome globally
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
