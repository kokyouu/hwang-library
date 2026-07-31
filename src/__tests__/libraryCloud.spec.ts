import axios from 'axios'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { getBookCount, getBookMarketplace } from '../services/libraryCloud'

vi.mock('axios')

const mockedAxios = vi.mocked(axios)

describe('library cloud service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('requests the cloud book-count endpoint', async () => {
    mockedAxios.get.mockResolvedValueOnce({
      data: {
        success: true,
        count: 3,
        collection: 'books',
        source: 'Cloud Firestore',
        projectId: 'hwang-library-lab7',
        generatedAt: '2026-07-31T00:00:00.000Z',
      },
    })

    await expect(getBookCount()).resolves.toMatchObject({ count: 3 })
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/books/count', { timeout: 15000 })
  })

  it('requests the Firestore marketplace endpoint', async () => {
    mockedAxios.get.mockResolvedValueOnce({
      data: {
        success: true,
        product: { catalogueValueAud: 13.5 },
        offers: [],
        records: [],
        source: 'Cloud Firestore',
        generatedAt: '2026-07-31T00:00:00.000Z',
      },
    })

    await expect(getBookMarketplace()).resolves.toMatchObject({ success: true })
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/books/marketplace', { timeout: 15000 })
  })
})
