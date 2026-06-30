<script setup>
import authors from '../assets/json/authors.json'
import bookstores from '../assets/json/bookstores.json'
</script>

<template>
  <main class="page-container">
    <h1>Library Application</h1>

    <section class="activity-section">
      <h2>Activity 1: Imported JSON Data</h2>
      <p>
        This Vue application imports data from authors.json and bookstores.json.
      </p>

      <div class="summary-card">
        <h3>Total Authors</h3>
        <p>{{ authors.length }}</p>
      </div>

      <div class="summary-card">
        <h3>Total Bookstores</h3>
        <p>{{ bookstores.length }}</p>
      </div>
    </section>
  </main>
</template>

<style scoped>
.page-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
  font-family: Arial, Helvetica, sans-serif;
  color: #222;
}

.activity-section {
  margin-bottom: 32px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

.summary-card {
  margin-top: 16px;
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f8f8f8;
}

.summary-card h3 {
  margin-top: 0;
}

.summary-card p {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}
</style>