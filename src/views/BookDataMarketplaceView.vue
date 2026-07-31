<script setup lang="ts">
import { BadgeDollarSign, Database, Download, RefreshCw, ShoppingBag } from 'lucide-vue-next'
import { ref } from 'vue'
import {
  getBookMarketplace,
  type MarketplaceOffer,
  type MarketplaceResponse,
} from '../services/libraryCloud'

const marketplace = ref<MarketplaceResponse | null>(null)
const loading = ref(false)
const error = ref('')
const selectedOffer = ref<MarketplaceOffer | null>(null)

const currency = new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD' })

async function loadMarketplace() {
  loading.value = true
  error.value = ''
  selectedOffer.value = null

  try {
    marketplace.value = await getBookMarketplace()
  } catch (requestError) {
    marketplace.value = null
    error.value =
      requestError instanceof Error
        ? requestError.message
        : 'Unable to load the Firestore catalogue.'
  } finally {
    loading.value = false
  }
}

function generateQuote(offer: MarketplaceOffer) {
  selectedOffer.value = offer
}
</script>

<template>
  <section>
    <header class="page-heading marketplace-heading">
      <div>
        <p class="eyebrow">Distinction and High Distinction extension</p>
        <h1>Book Data Marketplace</h1>
        <p class="subtitle">
          A cloud-generated commercial view of the live Firestore collection with transparent
          educational licensing.
        </p>
      </div>
      <button class="primary-button" type="button" :disabled="loading" @click="loadMarketplace">
        <RefreshCw :class="{ spin: loading }" :size="18" aria-hidden="true" />
        {{ loading ? 'Loading catalogue...' : 'Load Marketplace' }}
      </button>
    </header>

    <p v-if="error" class="status-message" role="alert">{{ error }}</p>

    <div v-if="marketplace" class="marketplace-content" aria-live="polite">
      <section class="summary-strip" aria-label="Marketplace summary">
        <div>
          <Database :size="21" aria-hidden="true" />
          <span>Live records</span>
          <strong>{{ marketplace.records.length }}</strong>
        </div>
        <div>
          <BadgeDollarSign :size="21" aria-hidden="true" />
          <span>Catalogue value</span>
          <strong>{{ currency.format(marketplace.product.catalogueValueAud) }}</strong>
        </div>
        <div>
          <Download :size="21" aria-hidden="true" />
          <span>Delivery</span>
          <strong>JSON API</strong>
        </div>
      </section>

      <section aria-labelledby="licence-heading">
        <div class="section-heading-row">
          <div>
            <p class="eyebrow">Live offers</p>
            <h2 id="licence-heading">Choose a data licence</h2>
          </div>
          <code>GET /api/books/marketplace</code>
        </div>

        <div class="offer-grid">
          <article v-for="offer in marketplace.offers" :key="offer.id" class="panel offer-card">
            <ShoppingBag :size="24" aria-hidden="true" />
            <h3>{{ offer.name }}</h3>
            <p>{{ offer.description }}</p>
            <strong>{{ currency.format(offer.priceAud) }}</strong>
            <button class="secondary-button" type="button" @click="generateQuote(offer)">
              Generate quote
            </button>
          </article>
        </div>

        <p v-if="selectedOffer" class="quote-confirmation" role="status">
          Quote ready: {{ selectedOffer.name }} at {{ currency.format(selectedOffer.priceAud) }}.
          Licence: {{ marketplace.product.licence }}.
        </p>
      </section>

      <section class="panel catalogue-panel" aria-labelledby="catalogue-heading">
        <header class="catalogue-header">
          <div>
            <p class="eyebrow">Firestore inventory</p>
            <h2 id="catalogue-heading">Priced catalogue records</h2>
          </div>
          <span>{{ marketplace.source }}</span>
        </header>
        <div class="table-scroll">
          <table>
            <thead>
              <tr>
                <th scope="col">Book</th>
                <th scope="col">ISBN</th>
                <th scope="col">Record licence</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="book in marketplace.records" :key="book.id">
                <td>{{ book.name }}</td>
                <td>
                  <code>{{ book.isbn }}</code>
                </td>
                <td>{{ currency.format(book.recordPriceAud) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <section v-else-if="!error" class="panel marketplace-empty">
      <ShoppingBag :size="46" :stroke-width="1.4" aria-hidden="true" />
      <h2>Firestore data prepared as a product</h2>
      <p>Load the marketplace to calculate live inventory, prices and licence offers.</p>
    </section>
  </section>
</template>

<style scoped>
.marketplace-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.marketplace-heading .primary-button {
  flex: 0 0 auto;
}

.marketplace-content {
  display: grid;
  gap: 28px;
}

.summary-strip {
  border-top: 1px solid #cdd0d4;
  border-bottom: 1px solid #cdd0d4;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.summary-strip div {
  min-height: 92px;
  padding: 18px 22px;
  display: grid;
  grid-template-columns: auto 1fr;
  grid-template-rows: auto auto;
  align-items: center;
  column-gap: 10px;
}

.summary-strip div + div {
  border-left: 1px solid #d8dbde;
}

.summary-strip svg {
  grid-row: 1 / 3;
  color: #8e1928;
}

.summary-strip span {
  color: #71757a;
  font-size: 0.76rem;
  text-transform: uppercase;
}

.summary-strip strong {
  color: #202124;
  font-size: 1.08rem;
}

.section-heading-row,
.catalogue-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
}

.section-heading-row h2,
.catalogue-header h2 {
  margin: 0;
}

.section-heading-row code,
.catalogue-header span {
  color: #73777c;
  font-size: 0.78rem;
}

.offer-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.offer-card {
  padding: 22px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px 16px;
}

.offer-card > svg {
  grid-column: 2;
  grid-row: 1 / 3;
  color: #8e1928;
}

.offer-card h3,
.offer-card p {
  grid-column: 1;
  margin: 0;
}

.offer-card h3 {
  color: #202124;
  font-size: 1.05rem;
}

.offer-card p {
  min-height: 46px;
  color: #64686d;
  font-size: 0.88rem;
  line-height: 1.5;
}

.offer-card > strong {
  align-self: center;
  color: #202124;
  font-size: 1.45rem;
}

.offer-card .secondary-button {
  justify-self: end;
}

.quote-confirmation {
  margin: 14px 0 0;
  border-left: 4px solid #2e6b47;
  padding: 11px 14px;
  color: #234c35;
  background: #edf5f0;
}

.catalogue-panel {
  overflow: hidden;
}

.catalogue-header {
  min-height: 78px;
  padding: 14px 20px;
  align-items: center;
}

.table-scroll {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 13px 20px;
  border-top: 1px solid #e1e3e5;
  text-align: left;
}

th {
  color: #62666b;
  background: #f7f7f8;
  font-size: 0.76rem;
  text-transform: uppercase;
}

td {
  color: #303236;
  font-size: 0.9rem;
}

.marketplace-empty {
  min-height: 320px;
  padding: 32px;
  display: grid;
  place-items: center;
  align-content: center;
  color: #777b80;
  text-align: center;
}

.marketplace-empty h2 {
  margin: 18px 0 7px;
}

.marketplace-empty p {
  max-width: 520px;
  margin: 0;
}

.spin {
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 760px) {
  .marketplace-heading {
    align-items: stretch;
    flex-direction: column;
  }

  .summary-strip,
  .offer-grid {
    grid-template-columns: 1fr;
  }

  .summary-strip div + div {
    border-top: 1px solid #d8dbde;
    border-left: 0;
  }

  .section-heading-row,
  .catalogue-header {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 520px) {
  .offer-card {
    grid-template-columns: 1fr;
  }

  .offer-card > svg,
  .offer-card h3,
  .offer-card p {
    grid-column: 1;
  }

  .offer-card > svg {
    grid-row: auto;
  }

  .offer-card .secondary-button {
    width: 100%;
    justify-self: stretch;
  }
}
</style>
