<script setup lang="ts">
import { computed } from 'vue'
import authors from '../assets/json/authors.json'

const apiResponse = computed(() => ({
  success: true,
  count: authors.reduce((total, author) => total + author.famousWorks.length, 0),
  books: authors.flatMap((author) =>
    author.famousWorks.map((book) => ({
      title: book.title,
      year: book.year,
      author: author.name,
      authorId: author.id,
    })),
  ),
}))
</script>

<template>
  <section>
    <header class="page-heading">
      <p class="eyebrow">Local API service</p>
      <h1>All Books</h1>
      <p class="subtitle">Every book in the author dataset, formatted as a JSON API response.</p>
    </header>

    <section class="panel api-panel" aria-labelledby="response-heading">
      <header class="api-toolbar">
        <div>
          <h2 id="response-heading">GetAllBookAPI response</h2>
          <code>GET /GetAllBookAPI</code>
        </div>
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
  min-height: 72px;
  padding: 12px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.api-toolbar h2 {
  margin: 0 0 4px;
}

.api-toolbar code {
  color: #71757a;
  font-size: 0.78rem;
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
