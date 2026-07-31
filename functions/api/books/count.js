const FIREBASE_PROJECT_ID = 'hwang-library-lab7'
const FIREBASE_API_KEY = 'AIzaSyCcNlpMxOUqD8x2DLmI3GFMlE4PC_hUqUo'
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

export function jsonResponse(payload, status = 200) {
  return new Response(JSON.stringify(payload, null, 2), {
    status,
    headers: {
      ...corsHeaders,
      'Content-Type': 'application/json; charset=utf-8',
    },
  })
}

export async function fetchBooks() {
  const response = await fetch(`${BOOKS_ENDPOINT}?key=${FIREBASE_API_KEY}`, {
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

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: corsHeaders })
}

export async function onRequestGet() {
  try {
    const books = await fetchBooks()
    return jsonResponse({
      success: true,
      count: books.length,
      collection: 'books',
      source: 'Cloud Firestore',
      projectId: FIREBASE_PROJECT_ID,
      generatedAt: new Date().toISOString(),
    })
  } catch (error) {
    return jsonResponse(
      {
        success: false,
        error: error instanceof Error ? error.message : 'Unable to count Firestore books.',
      },
      500,
    )
  }
}
