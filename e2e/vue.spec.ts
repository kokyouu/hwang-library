import { test, expect } from '@playwright/test'

test('opens the Lab 9 book counter and marketplace routes', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('h1')).toHaveText('Book Counter')
  await expect(page.getByRole('button', { name: 'Get Book Count' })).toBeVisible()

  await page.getByRole('link', { name: 'Data Marketplace' }).click()
  await expect(page.locator('h1')).toHaveText('Book Data Marketplace')
  await expect(page.getByRole('button', { name: 'Load Marketplace' })).toBeVisible()
})
