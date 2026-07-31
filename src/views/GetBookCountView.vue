<script setup lang="ts">
import { BookOpenCheck, Cloud, Database, RefreshCw } from 'lucide-vue-next'
import { ref } from 'vue'
import { getBookCount, type BookCountResponse } from '../services/libraryCloud'

const result = ref<BookCountResponse | null>(null)
const loading = ref(false)
const error = ref('')

async function loadBookCount() {
  loading.value = true
  error.value = ''

  try {
    result.value = await getBookCount()
  } catch (requestError) {
    result.value = null
    error.value =
      requestError instanceof Error ? requestError.message : 'Unable to reach the cloud function.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section>
    <header class="page-heading">
      <p class="eyebrow">Assessed Lab 9</p>
      <h1>Book Counter</h1>
      <p class="subtitle">
        A Vue client calling a Cloudflare Pages Function that counts live records in Firestore.
      </p>
    </header>

    <div class="counter-layout">
      <section class="panel action-panel" aria-labelledby="counter-action-heading">
        <div class="section-icon" aria-hidden="true">
          <Cloud :size="30" :stroke-width="1.7" />
        </div>
        <h2 id="counter-action-heading">Run cloud function</h2>
        <p>
          Request the current number of documents in the Firestore <code>books</code> collection.
        </p>
        <button class="primary-button" type="button" :disabled="loading" @click="loadBookCount">
          <RefreshCw v-if="loading" class="spin" :size="18" aria-hidden="true" />
          <BookOpenCheck v-else :size="18" aria-hidden="true" />
          {{ loading ? 'Counting books...' : 'Get Book Count' }}
        </button>
        <code class="endpoint">GET /api/books/count</code>
      </section>

      <section class="panel result-panel" aria-live="polite">
        <div v-if="result" class="count-result">
          <div class="result-label">
            <Database :size="20" aria-hidden="true" />
            Live Firestore result
          </div>
          <p class="count-number">{{ result.count }}</p>
          <p class="count-caption">Total number of books: {{ result.count }}</p>
          <dl>
            <div>
              <dt>Cloud source</dt>
              <dd>{{ result.source }}</dd>
            </div>
            <div>
              <dt>Collection</dt>
              <dd>{{ result.collection }}</dd>
            </div>
            <div>
              <dt>Project</dt>
              <dd>{{ result.projectId }}</dd>
            </div>
          </dl>
        </div>
        <div v-else-if="error" class="empty-result error-result" role="alert">
          <p>error</p>
          <span>{{ error }}</span>
        </div>
        <div v-else class="empty-result">
          <Database :size="42" :stroke-width="1.4" aria-hidden="true" />
          <p>Cloud result ready on request.</p>
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.counter-layout {
  display: grid;
  grid-template-columns: minmax(300px, 0.82fr) minmax(0, 1.18fr);
  gap: 20px;
}

.action-panel,
.result-panel {
  min-height: 360px;
}

.action-panel {
  padding: 28px;
}

.section-icon {
  width: 52px;
  height: 52px;
  margin-bottom: 22px;
  border: 1px solid #d2d5d9;
  border-radius: 6px;
  display: grid;
  place-items: center;
  color: #8e1928;
  background: #f7f7f8;
}

.action-panel h2 {
  margin-bottom: 10px;
}

.action-panel p {
  margin-bottom: 24px;
  color: #62666b;
  line-height: 1.55;
}

.action-panel .primary-button {
  width: 100%;
}

.endpoint {
  margin-top: 18px;
  display: block;
  color: #71757a;
  font-size: 0.78rem;
  text-align: center;
}

.result-panel {
  display: grid;
  place-items: center;
  background: #f9fafb;
}

.count-result {
  width: min(100%, 500px);
  padding: 32px;
}

.result-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #5c6065;
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
}

.count-number {
  margin: 22px 0 0;
  color: #17181a;
  font-size: 5rem;
  font-weight: 760;
  line-height: 1;
}

.count-caption {
  margin: 5px 0 28px;
  color: #323438;
  font-size: 1.05rem;
  font-weight: 650;
}

dl {
  margin: 0;
  border-top: 1px solid #d9dcdf;
}

dl div {
  min-height: 44px;
  border-bottom: 1px solid #e4e6e8;
  display: grid;
  grid-template-columns: 120px minmax(0, 1fr);
  align-items: center;
  gap: 12px;
}

dt {
  color: #73777c;
  font-size: 0.78rem;
}

dd {
  min-width: 0;
  margin: 0;
  overflow-wrap: anywhere;
  color: #25272a;
  font-family: 'Cascadia Code', Consolas, monospace;
  font-size: 0.82rem;
}

.empty-result {
  padding: 32px;
  color: #777b80;
  text-align: center;
}

.empty-result p {
  margin: 14px 0 0;
}

.error-result p {
  color: #8e1928;
  font-size: 1.2rem;
  font-weight: 700;
}

.error-result span {
  max-width: 460px;
  margin-top: 8px;
  display: block;
}

.spin {
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 820px) {
  .counter-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  .action-panel,
  .count-result {
    padding: 22px;
  }

  .count-number {
    font-size: 4rem;
  }

  dl div {
    grid-template-columns: 96px minmax(0, 1fr);
  }
}
</style>
