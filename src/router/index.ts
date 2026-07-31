import { createRouter, createWebHistory } from 'vue-router'
import BookDataMarketplaceView from '../views/BookDataMarketplaceView.vue'
import CountBookAPI from '../views/CountBookAPI.vue'
import GetAllBookAPI from '../views/GetAllBookAPI.vue'
import GetBookCountView from '../views/GetBookCountView.vue'
import WeatherView from '../views/WeatherView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/BookCounter' },
    { path: '/BookCounter', name: 'BookCounter', component: GetBookCountView },
    {
      path: '/DataMarketplace',
      name: 'DataMarketplace',
      component: BookDataMarketplaceView,
    },
    { path: '/WeatherCheck', name: 'GetWeather', component: WeatherView },
    { path: '/CountBookAPI', name: 'CountBookAPI', component: CountBookAPI },
    { path: '/GetAllBookAPI', name: 'GetAllBookAPI', component: GetAllBookAPI },
  ],
})

export default router
