import axios from 'axios'

const functionBaseUrl = (import.meta.env.VITE_LIBRARY_FUNCTION_BASE_URL ?? '').replace(/\/$/, '')

export interface BookCountResponse {
  success: boolean
  count: number
  collection: string
  source: string
  projectId: string
  generatedAt: string
}

export interface MarketplaceOffer {
  id: string
  name: string
  priceAud: number
  description: string
}

export interface MarketplaceRecord {
  id: string
  isbn: number
  name: string
  createdAt: string
  updatedAt: string
  recordPriceAud: number
}

export interface MarketplaceResponse {
  success: boolean
  product: {
    name: string
    edition: string
    currency: string
    catalogueValueAud: number
    licence: string
  }
  offers: MarketplaceOffer[]
  records: MarketplaceRecord[]
  source: string
  generatedAt: string
}

export async function getBookCount(): Promise<BookCountResponse> {
  const response = await axios.get<BookCountResponse>(`${functionBaseUrl}/api/books/count`, {
    timeout: 15000,
  })
  return response.data
}

export async function getBookMarketplace(): Promise<MarketplaceResponse> {
  const response = await axios.get<MarketplaceResponse>(
    `${functionBaseUrl}/api/books/marketplace`,
    { timeout: 15000 },
  )
  return response.data
}
