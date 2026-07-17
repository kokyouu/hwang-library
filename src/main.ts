import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Import Bootstrap CSS and JavaScript
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Import global CSS
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')