import axios from 'axios'

export type WeatherKind = 'clear' | 'cloud' | 'rain' | 'snow' | 'storm' | 'fog'

export interface WeatherResult {
  location: string
  country?: string
  temperature: number
  description: string
  kind: WeatherKind
  iconUrl?: string
  provider: 'OpenWeather' | 'Open-Meteo'
}

interface OpenMeteoPlace {
  name: string
  country?: string
  country_code?: string
  latitude: number
  longitude: number
}

const openWeatherKey = import.meta.env.VITE_OPENWEATHER_API_KEY?.trim()

export function describeWeatherCode(code: number): { description: string; kind: WeatherKind } {
  if (code === 0) return { description: 'Clear sky', kind: 'clear' }
  if ([1, 2, 3].includes(code)) return { description: 'Partly cloudy', kind: 'cloud' }
  if ([45, 48].includes(code)) return { description: 'Foggy', kind: 'fog' }
  if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82)) {
    return { description: 'Rain', kind: 'rain' }
  }
  if ((code >= 71 && code <= 77) || (code >= 85 && code <= 86)) {
    return { description: 'Snow', kind: 'snow' }
  }
  if (code >= 95) return { description: 'Thunderstorm', kind: 'storm' }
  return { description: 'Cloudy', kind: 'cloud' }
}

async function fetchOpenMeteoWeather(
  latitude: number,
  longitude: number,
  location: string,
  country?: string,
): Promise<WeatherResult> {
  const response = await axios.get('https://api.open-meteo.com/v1/forecast', {
    params: {
      latitude,
      longitude,
      current: 'temperature_2m,weather_code',
      temperature_unit: 'celsius',
      timezone: 'auto',
    },
  })

  const current = response.data.current
  const details = describeWeatherCode(current.weather_code)
  return {
    location,
    country,
    temperature: Math.round(current.temperature_2m),
    description: details.description,
    kind: details.kind,
    provider: 'Open-Meteo',
  }
}

async function fetchOpenWeather(params: Record<string, string | number>): Promise<WeatherResult> {
  const response = await axios.get('https://api.openweathermap.org/data/2.5/weather', {
    params: { ...params, appid: openWeatherKey, units: 'metric' },
  })
  const data = response.data
  return {
    location: data.name,
    country: data.sys?.country,
    temperature: Math.round(data.main.temp),
    description: data.weather[0].description,
    kind: openWeatherKind(data.weather[0].id),
    iconUrl: `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`,
    provider: 'OpenWeather',
  }
}

function openWeatherKind(id: number): WeatherKind {
  if (id >= 200 && id < 300) return 'storm'
  if (id >= 300 && id < 600) return 'rain'
  if (id >= 600 && id < 700) return 'snow'
  if (id >= 700 && id < 800) return 'fog'
  if (id === 800) return 'clear'
  return 'cloud'
}

export async function searchWeatherByCity(query: string): Promise<WeatherResult> {
  if (openWeatherKey) return fetchOpenWeather({ q: query })

  const [cityName, requestedCountry] = query.split(',').map((part) => part.trim())
  const countryCode = requestedCountry?.length === 2 ? requestedCountry.toUpperCase() : undefined
  const response = await axios.get('https://geocoding-api.open-meteo.com/v1/search', {
    params: {
      name: cityName,
      count: 10,
      language: 'en',
      format: 'json',
      ...(countryCode ? { countryCode } : {}),
    },
  })
  const results = (response.data.results ?? []) as OpenMeteoPlace[]
  const countryMatch = requestedCountry
    ? results.find(
        (place) =>
          place.country_code?.toLowerCase() === requestedCountry.toLowerCase() ||
          place.country?.toLowerCase() === requestedCountry.toLowerCase(),
      )
    : undefined
  const place = countryMatch ?? results[0]
  if (!place) throw new Error(`No weather location found for "${query}".`)

  return fetchOpenMeteoWeather(
    place.latitude,
    place.longitude,
    place.name,
    place.country_code ?? place.country,
  )
}

export async function getWeatherByCoordinates(
  latitude: number,
  longitude: number,
): Promise<WeatherResult> {
  if (openWeatherKey) return fetchOpenWeather({ lat: latitude, lon: longitude })
  return fetchOpenMeteoWeather(latitude, longitude, 'Current location')
}
