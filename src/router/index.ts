import { createRouter, createWebHistory } from 'vue-router'
import CountBookAPI from '../views/CountBookAPI.vue'
import GetAllBookAPI from '../views/GetAllBookAPI.vue'
import WeatherView from '../views/WeatherView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/WeatherCheck' },
    { path: '/WeatherCheck', name: 'GetWeather', component: WeatherView },
    { path: '/CountBookAPI', name: 'CountBookAPI', component: CountBookAPI },
    { path: '/GetAllBookAPI', name: 'GetAllBookAPI', component: GetAllBookAPI },
  ],
})

export default router
