import { test, expect } from '@playwright/test'

test('opens the weather page from the project root', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveURL(/\/WeatherCheck$/)
  await expect(page.getByRole('heading', { name: 'Weather Check' })).toBeVisible()
  await expect(page.getByRole('button', { name: 'Search' })).toBeVisible()
})
