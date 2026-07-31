import { fetchBooks, jsonResponse } from './count.js'

const corsHeaders = {
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Origin': '*',
  'Cache-Control': 'no-store',
}

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: corsHeaders })
}

export async function onRequestGet() {
  try {
    const books = await fetchBooks()
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
      records: books.map((book) => ({
        ...book,
        recordPriceAud,
      })),
      source: 'Cloud Firestore',
      generatedAt: new Date().toISOString(),
    })
  } catch (error) {
    return jsonResponse(
      {
        success: false,
        error: error instanceof Error ? error.message : 'Unable to prepare the data marketplace.',
      },
      500,
    )
  }
}
