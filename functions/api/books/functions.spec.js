import { afterEach, describe, expect, it, vi } from 'vitest'
import { onRequestGet as getCount } from './count.js'
import { onRequestGet as getMarketplace } from './marketplace.js'

const firestorePayload = {
  documents: [
    {
      name: 'projects/hwang-library-lab7/databases/(default)/documents/books/book-2',
      fields: {
        name: { stringValue: 'Vue.js Essentials' },
        isbn: { integerValue: '1018' },
        createdAt: { timestampValue: '2026-07-24T01:18:26.927Z' },
      },
      createTime: '2026-07-24T01:18:26.984808Z',
      updateTime: '2026-07-24T01:18:26.984808Z',
    },
    {
      name: 'projects/hwang-library-lab7/databases/(default)/documents/books/book-1',
      fields: {
        name: { stringValue: 'Mastering Cloud Firestore' },
        isbn: { integerValue: '2048' },
      },
      createTime: '2026-07-24T01:18:32.035912Z',
      updateTime: '2026-07-24T01:19:51.119139Z',
    },
  ],
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('Cloudflare Pages book functions', () => {
  it('counts books returned by Firestore and includes CORS headers', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(firestorePayload), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      ),
    )

    const response = await getCount()
    const payload = await response.json()

    expect(response.status).toBe(200)
    expect(response.headers.get('Access-Control-Allow-Origin')).toBe('*')
    expect(payload).toMatchObject({ success: true, count: 2, collection: 'books' })
  })

  it('builds priced marketplace offers from Firestore records', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(firestorePayload), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      ),
    )

    const response = await getMarketplace()
    const payload = await response.json()

    expect(payload.product.catalogueValueAud).toBe(9)
    expect(payload.offers).toHaveLength(2)
    expect(payload.records.map((book) => book.name)).toEqual([
      'Mastering Cloud Firestore',
      'Vue.js Essentials',
    ])
  })
})
