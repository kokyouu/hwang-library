import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import App from '../App.vue'
import router from '../router'

describe('App', () => {
  it('renders the Lab 10 weather route and API navigation', async () => {
    await router.push('/WeatherCheck')
    await router.isReady()

    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    })

    expect(wrapper.get('h1').text()).toBe('Weather Check')
    expect(wrapper.text()).toContain('Book Stats API')
    expect(wrapper.text()).toContain('All Books API')
  })
})
