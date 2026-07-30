<script setup lang="ts">
import {
  Cloud,
  CloudFog,
  CloudLightning,
  CloudRain,
  LocateFixed,
  MapPin,
  Search,
  Snowflake,
  Sun,
} from 'lucide-vue-next'
import { computed, ref } from 'vue'
import {
  getWeatherByCoordinates,
  searchWeatherByCity,
  type WeatherKind,
  type WeatherResult,
} from '../services/weather'

const city = ref('')
const weatherData = ref<WeatherResult | null>(null)
const loading = ref(false)
const error = ref('')

const weatherIcon = computed(() => {
  const icons: Record<WeatherKind, typeof Sun> = {
    clear: Sun,
    cloud: Cloud,
    rain: CloudRain,
    snow: Snowflake,
    storm: CloudLightning,
    fog: CloudFog,
  }
  return icons[weatherData.value?.kind ?? 'cloud']
})

async function searchByCity() {
  const query = city.value.trim()
  if (!query) {
    error.value = 'Enter a city name to search.'
    return
  }

  await loadWeather(() => searchWeatherByCity(query))
}

async function fetchCurrentLocationWeather() {
  if (!navigator.geolocation) {
    error.value = 'Geolocation is not supported by this browser.'
    return
  }

  loading.value = true
  error.value = ''
  navigator.geolocation.getCurrentPosition(
    async ({ coords }) => {
      await loadWeather(() => getWeatherByCoordinates(coords.latitude, coords.longitude))
    },
    (geolocationError) => {
      loading.value = false
      error.value = `Unable to use current location: ${geolocationError.message}`
    },
    { enableHighAccuracy: false, timeout: 30000, maximumAge: 300000 },
  )
}

async function loadWeather(loader: () => Promise<WeatherResult>) {
  loading.value = true
  error.value = ''
  try {
    weatherData.value = await loader()
  } catch (requestError) {
    const message = requestError instanceof Error ? requestError.message : 'Weather request failed.'
    error.value = message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section>
    <header class="page-heading">
      <p class="eyebrow">External API service</p>
      <h1>Weather Check</h1>
      <p class="subtitle">Current conditions from a city search or your browser location.</p>
    </header>

    <div class="weather-layout">
      <section class="panel search-panel" aria-labelledby="search-heading">
        <h2 id="search-heading">Search weather by city</h2>
        <form class="search-form" @submit.prevent="searchByCity">
          <label class="sr-only" for="city">City name</label>
          <div class="search-field">
            <MapPin :size="19" aria-hidden="true" />
            <input
              id="city"
              v-model="city"
              type="text"
              placeholder="Clayton, AU"
              autocomplete="off"
            />
          </div>
          <button class="primary-button" type="submit" :disabled="loading">
            <Search :size="18" aria-hidden="true" />
            Search
          </button>
        </form>
        <div class="action-row">
          <button
            class="secondary-button"
            type="button"
            :disabled="loading"
            @click="fetchCurrentLocationWeather"
          >
            <LocateFixed :size="18" aria-hidden="true" />
            Use current location
          </button>
        </div>
        <p v-if="error" class="status-message" role="alert">{{ error }}</p>
      </section>

      <section class="panel weather-panel" aria-live="polite">
        <div v-if="loading" class="empty-weather">Loading current conditions...</div>
        <div v-else-if="weatherData" class="weather-result">
          <div class="weather-icon" aria-hidden="true">
            <img v-if="weatherData.iconUrl" :src="weatherData.iconUrl" alt="" />
            <component :is="weatherIcon" v-else :size="62" :stroke-width="1.5" />
          </div>
          <div>
            <p class="location-label">
              {{ weatherData.location
              }}<span v-if="weatherData.country">, {{ weatherData.country }}</span>
            </p>
            <p class="temperature">{{ weatherData.temperature }}<span>&deg;C</span></p>
            <p class="condition">{{ weatherData.description }}</p>
            <p class="provider">Data: {{ weatherData.provider }}</p>
          </div>
        </div>
        <div v-else class="empty-weather">
          <Cloud :size="42" :stroke-width="1.4" aria-hidden="true" />
          <p>Search for a city or use your current location.</p>
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.weather-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
  gap: 20px;
}

.search-panel,
.weather-panel {
  min-height: 320px;
}

.search-panel {
  padding: 28px;
}

.search-panel h2 {
  margin-bottom: 18px;
}

.search-form {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 10px;
}

.search-field {
  min-height: 44px;
  border: 1px solid #b8bcc1;
  border-radius: 5px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  gap: 9px;
  color: #6a6e73;
  background: #fff;
}

.search-field:focus-within {
  border-color: #a01d2d;
  box-shadow: 0 0 0 3px rgba(160, 29, 45, 0.12);
}

.search-field input {
  width: 100%;
  border: 0;
  outline: 0;
  color: #202124;
  background: transparent;
}

.action-row {
  margin-top: 12px;
}

.weather-panel {
  overflow: hidden;
  display: grid;
  place-items: center;
  background: #f9fafb;
}

.weather-result {
  width: 100%;
  min-height: 320px;
  padding: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
}

.weather-icon {
  width: 110px;
  height: 110px;
  border: 1px solid #f0c9ce;
  border-radius: 50%;
  display: grid;
  place-items: center;
  color: #a01d2d;
  background: #fff;
}

.weather-icon img {
  width: 94px;
  height: 94px;
}

.location-label {
  margin-bottom: 4px;
  color: #4c5055;
  font-weight: 700;
}

.temperature {
  margin-bottom: 2px;
  font-size: 3.7rem;
  font-weight: 760;
  line-height: 1;
}

.temperature span {
  font-size: 1.6rem;
  font-weight: 600;
}

.condition {
  margin-bottom: 14px;
  color: #55595e;
  text-transform: capitalize;
}

.provider {
  margin-bottom: 0;
  color: #8a8e93;
  font-size: 0.75rem;
}

.empty-weather {
  padding: 30px;
  color: #777b80;
  text-align: center;
}

.empty-weather p {
  margin: 12px 0 0;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
}

@media (max-width: 820px) {
  .weather-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 560px) {
  .search-panel {
    padding: 20px;
  }

  .search-form {
    grid-template-columns: 1fr;
  }

  .weather-result {
    min-height: 280px;
    padding: 24px;
    align-items: flex-start;
    flex-direction: column;
    gap: 18px;
  }
}
</style>
