import axios from 'axios'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { describeWeatherCode, searchWeatherByCity } from '../services/weather'

vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
  },
}))

const mockedGet = vi.mocked(axios.get)

beforeEach(() => {
  mockedGet.mockReset()
})

describe('describeWeatherCode', () => {
  it('maps clear, rain, snow and storm weather codes', () => {
    expect(describeWeatherCode(0)).toEqual({ description: 'Clear sky', kind: 'clear' })
    expect(describeWeatherCode(61).kind).toBe('rain')
    expect(describeWeatherCode(75).kind).toBe('snow')
    expect(describeWeatherCode(95).kind).toBe('storm')
  })
})

describe('searchWeatherByCity', () => {
  it('separates an optional country code from the city name', async () => {
    mockedGet
      .mockResolvedValueOnce({
        data: {
          results: [
            {
              name: 'Clayton',
              country: 'Australia',
              country_code: 'AU',
              latitude: -37.92,
              longitude: 145.12,
            },
          ],
        },
      })
      .mockResolvedValueOnce({
        data: { current: { temperature_2m: 18.4, weather_code: 2 } },
      })

    const result = await searchWeatherByCity('Clayton, AU')

    expect(mockedGet).toHaveBeenNthCalledWith(1, 'https://geocoding-api.open-meteo.com/v1/search', {
      params: {
        name: 'Clayton',
        count: 10,
        language: 'en',
        format: 'json',
        countryCode: 'AU',
      },
    })
    expect(result).toMatchObject({
      location: 'Clayton',
      country: 'AU',
      temperature: 18,
      provider: 'Open-Meteo',
    })
  })
})
