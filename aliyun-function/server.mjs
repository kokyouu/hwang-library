import http from 'node:http'
import { pathToFileURL } from 'node:url'

const FIREBASE_PROJECT_ID = process.env.FIREBASE_PROJECT_ID ?? 'hwang-library-lab7'
const FIREBASE_API_KEY = process.env.FIREBASE_API_KEY ?? 'AIzaSyCcNlpMxOUqD8x2DLmI3GFMlE4PC_hUqUo'
const BOOKS_ENDPOINT = `https://firestore.googleapis.com/v1/projects/${FIREBASE_PROJECT_ID}/databases/(default)/documents/books`

const corsHeaders = {
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Origin': '*',
  'Cache-Control': 'no-store',
}

function readFirestoreValue(value = {}) {
  if ('stringValue' in value) return value.stringValue
  if ('integerValue' in value) return Number(value.integerValue)
  if ('doubleValue' in value) return Number(value.doubleValue)
  if ('timestampValue' in value) return value.timestampValue
  if ('booleanValue' in value) return value.booleanValue
  return null
}

function jsonResponse(payload, status = 200) {
  return new Response(JSON.stringify(payload, null, 2), {
    status,
    headers: {
      ...corsHeaders,
      'Content-Type': 'application/json; charset=utf-8',
    },
  })
}

export async function fetchBooks(fetchImpl = fetch) {
  const response = await fetchImpl(`${BOOKS_ENDPOINT}?key=${FIREBASE_API_KEY}`, {
    headers: { Accept: 'application/json' },
  })

  if (!response.ok) {
    throw new Error(`Firestore request failed with status ${response.status}`)
  }

  const payload = await response.json()
  return (payload.documents ?? [])
    .map((document) => {
      const fields = document.fields ?? {}
      return {
        id: document.name.split('/').pop(),
        isbn: readFirestoreValue(fields.isbn),
        name: readFirestoreValue(fields.name),
        createdAt: readFirestoreValue(fields.createdAt) ?? document.createTime,
        updatedAt: readFirestoreValue(fields.updatedAt) ?? document.updateTime,
      }
    })
    .sort((a, b) => String(a.name).localeCompare(String(b.name)))
}

async function countBooks(fetchImpl) {
  const books = await fetchBooks(fetchImpl)
  return jsonResponse({
    success: true,
    count: books.length,
    collection: 'books',
    source: 'Cloud Firestore via Alibaba Cloud Function Compute',
    projectId: FIREBASE_PROJECT_ID,
    generatedAt: new Date().toISOString(),
  })
}

async function buildMarketplace(fetchImpl) {
  const books = await fetchBooks(fetchImpl)
  const recordPriceAud = 4.5
  const catalogueValueAud = Number((books.length * recordPriceAud).toFixed(2))

  return jsonResponse({
    success: true,
    product: {
      name: 'Hwang Library Curated Books Dataset',
      edition: `Firestore live edition - ${books.length} records`,
      currency: 'AUD',
      catalogueValueAud,
      licence: 'Single-project educational data licence',
    },
    offers: [
      {
        id: 'snapshot',
        name: 'Snapshot',
        priceAud: catalogueValueAud,
        description: 'One JSON export of the current Firestore collection.',
      },
      {
        id: 'semester',
        name: 'Semester Feed',
        priceAud: Number((catalogueValueAud * 2.4).toFixed(2)),
        description: 'Live API access for one teaching semester.',
      },
    ],
    records: books.map((book) => ({ ...book, recordPriceAud })),
    source: 'Cloud Firestore via Alibaba Cloud Function Compute',
    generatedAt: new Date().toISOString(),
  })
}

export async function handleRequest(request, fetchImpl = fetch) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders })
  }

  if (request.method !== 'GET') {
    return jsonResponse({ success: false, error: 'Method not allowed.' }, 405)
  }

  const { pathname } = new URL(request.url)

  try {
    if (pathname === '/health') {
      return jsonResponse({
        success: true,
        service: 'fit5032-lab9-hwang-library',
        platform: 'Alibaba Cloud Function Compute',
      })
    }
    if (pathname === '/api/books/count') return await countBooks(fetchImpl)
    if (pathname === '/api/books/marketplace') return await buildMarketplace(fetchImpl)
    return jsonResponse({ success: false, error: 'Route not found.' }, 404)
  } catch (error) {
    return jsonResponse(
      {
        success: false,
        error: error instanceof Error ? error.message : 'Unable to process the request.',
      },
      500,
    )
  }
}

export function createServer(fetchImpl = fetch) {
  return http.createServer(async (request, response) => {
    const host = request.headers.host ?? '127.0.0.1'
    const webResponse = await handleRequest(
      new Request(`http://${host}${request.url}`, { method: request.method }),
      fetchImpl,
    )

    response.writeHead(webResponse.status, Object.fromEntries(webResponse.headers.entries()))
    response.end(Buffer.from(await webResponse.arrayBuffer()))
  })
}

const isMainModule = process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href
if (isMainModule) {
  const port = Number(process.env.FC_SERVER_PORT ?? 9000)
  createServer().listen(port, '0.0.0.0', () => {
    console.log(`FIT5032 Lab 9 function listening on port ${port}`)
  })
}
