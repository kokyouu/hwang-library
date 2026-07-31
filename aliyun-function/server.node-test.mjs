import assert from 'node:assert/strict'
import { describe, it } from 'node:test'
import { handleRequest } from './server.mjs'

const firestorePayload = {
  documents: [
    {
      name: 'projects/hwang-library-lab7/databases/(default)/documents/books/book-2',
      fields: {
        name: { stringValue: 'Vue.js Essentials' },
        isbn: { integerValue: '1018' },
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

const firestoreFetch = async () =>
  new Response(JSON.stringify(firestorePayload), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })

describe('Alibaba Cloud Function Compute web function', () => {
  it('reports its health without contacting Firestore', async () => {
    const response = await handleRequest(new Request('http://localhost/health'), () => {
      throw new Error('Firestore should not be called')
    })
    assert.equal(response.status, 200)
    assert.deepEqual(await response.json(), {
      success: true,
      service: 'fit5032-lab9-hwang-library',
      platform: 'Alibaba Cloud Function Compute',
    })
  })

  it('counts Firestore books', async () => {
    const response = await handleRequest(
      new Request('http://localhost/api/books/count'),
      firestoreFetch,
    )
    const payload = await response.json()
    assert.equal(response.status, 200)
    assert.equal(response.headers.get('Access-Control-Allow-Origin'), '*')
    assert.equal(payload.count, 2)
    assert.equal(payload.collection, 'books')
  })

  it('builds the marketplace from Firestore records', async () => {
    const response = await handleRequest(
      new Request('http://localhost/api/books/marketplace'),
      firestoreFetch,
    )
    const payload = await response.json()
    assert.equal(payload.product.catalogueValueAud, 9)
    assert.equal(payload.offers.length, 2)
    assert.deepEqual(
      payload.records.map((book) => book.name),
      ['Mastering Cloud Firestore', 'Vue.js Essentials'],
    )
  })
})
