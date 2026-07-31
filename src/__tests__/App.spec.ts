import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import App from '../App.vue'
import router from '../router'

describe('App', () => {
  it('renders the Lab 9 book counter and cloud navigation', async () => {
    await router.push('/BookCounter')
    await router.isReady()

    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    })

    expect(wrapper.get('h1').text()).toBe('Book Counter')
    expect(wrapper.text()).toContain('Data Marketplace')
    expect(wrapper.text()).toContain('Get Book Count')
  })
})
