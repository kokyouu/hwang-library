import { describe, expect, it } from 'vitest'
import { describeWeatherCode } from '../services/weather'

describe('describeWeatherCode', () => {
  it('maps clear, rain, snow and storm weather codes', () => {
    expect(describeWeatherCode(0)).toEqual({ description: 'Clear sky', kind: 'clear' })
    expect(describeWeatherCode(61).kind).toBe('rain')
    expect(describeWeatherCode(75).kind).toBe('snow')
    expect(describeWeatherCode(95).kind).toBe('storm')
  })
})
