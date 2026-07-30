<script setup lang="ts">
import { computed } from 'vue'
import authors from '../assets/json/authors.json'

const apiResponse = computed(() => ({
  success: true,
  data: {
    authorsCount: authors.length,
    totalBooks: authors.reduce((total, author) => total + author.famousWorks.length, 0),
    authors: authors.map((author) => ({
      name: author.name,
      bookCount: author.famousWorks.length,
    })),
  },
}))
</script>

<template>
  <section>
    <header class="page-heading">
      <p class="eyebrow">Local API service</p>
      <h1>Author and Book Statistics</h1>
      <p class="subtitle">A JSON response calculated from the Lab 2 author dataset.</p>
    </header>

    <section class="panel api-panel" aria-labelledby="response-heading">
      <header class="api-toolbar">
        <h2 id="response-heading">CountBookAPI response</h2>
        <span class="success-badge">200 OK</span>
      </header>
      <pre class="json-output">{{ JSON.stringify(apiResponse, null, 2) }}</pre>
    </section>
  </section>
</template>

<style scoped>
.api-panel {
  overflow: hidden;
}

.api-toolbar {
  min-height: 58px;
  padding: 0 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.api-toolbar h2 {
  margin: 0;
}

.success-badge {
  border: 1px solid #82b596;
  border-radius: 4px;
  padding: 4px 8px;
  color: #17653a;
  background: #eaf6ee;
  font-family: 'Cascadia Code', Consolas, monospace;
  font-size: 0.78rem;
  font-weight: 700;
}
</style>
