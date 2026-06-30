<script setup>
import { ref, computed } from 'vue'
import authors from '../assets/json/authors.json'
import bookstores from '../assets/json/bookstores.json'

const showBookstores = ref(true)
const showMessage = ref(false)

const getWorkTitle = (work) => {
  if (typeof work === 'string') {
    return work
  }

  return work.title
}

const getBookstoreLocation = (store) => {
  return store.location || store.address || store.city || 'Location not provided'
}

const modernAuthors = computed(() =>
  authors.filter((author) => author.birthYear > 1850)
)

const allFamousWorks = computed(() =>
  authors.flatMap((author) =>
    author.famousWorks.map((work) => getWorkTitle(work))
  )
)

const searchedAuthor = computed(() =>
  authors.find((author) => author.name === 'George Orwell')
)

const authorById = computed(() =>
  authors.find((author) => author.id === 1)
)
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

    <section class="activity-section">
      <h2>Activity 2: Authors Born After 1850</h2>
      <p>
        This section uses a computed property to filter authors born after 1850.
      </p>

      <ul>
        <li v-for="author in modernAuthors" :key="author.id">
          {{ author.name }} ({{ author.birthYear }})
        </li>
      </ul>
    </section>

    <section class="activity-section">
      <h2>Activity 3: All Famous Works</h2>
      <p>
        This section uses a computed property to collect all famous works.
      </p>

      <ul>
        <li v-for="work in allFamousWorks" :key="work">
          {{ work }}
        </li>
      </ul>
    </section>

    <section class="activity-section">
      <h2>Activity 4: Search Author by Name</h2>
      <p>
        This section searches for the author named George Orwell.
      </p>

      <p v-if="searchedAuthor" class="result-box">
        {{ searchedAuthor.name }} was born in {{ searchedAuthor.birthYear }}.
      </p>

      <p v-else class="warning-box">
        George Orwell was not found.
      </p>
    </section>

    <section class="activity-section">
      <h2>Activity 5: Search Author by ID</h2>
      <p>
        This section searches for the author with ID 1.
      </p>

      <p v-if="authorById" class="result-box">
        Author ID 1: {{ authorById.name }} ({{ authorById.birthYear }})
      </p>

      <p v-else class="warning-box">
        Author ID 1 was not found.
      </p>
    </section>

    <section class="activity-section">
      <h2>Activity 6: Render All Authors with v-for</h2>
      <p>
        This section uses v-for to render all authors and their birth years.
      </p>

      <ul>
        <li v-for="author in authors" :key="author.id">
          {{ author.name }} ({{ author.birthYear }})
        </li>
      </ul>
    </section>

    <section class="activity-section">
      <h2>Activity 7: Render Authors Born After 1850</h2>
      <p>
        This section renders the computed property modernAuthors using v-for.
      </p>

      <ul>
        <li v-for="author in modernAuthors" :key="author.id">
          {{ author.name }} ({{ author.birthYear }})
        </li>
      </ul>
    </section>

    <section class="activity-section">
      <h2>Activity 8: Render All Famous Works</h2>
      <p>
        This section renders the computed property allFamousWorks using v-for.
      </p>

      <ul>
        <li v-for="work in allFamousWorks" :key="work">
          {{ work }}
        </li>
      </ul>
    </section>

    <section class="activity-section">
      <h2>Activity 9: Render Bookstores</h2>
      <p>
        This section uses v-for to display bookstore data.
      </p>

      <ul>
        <li v-for="store in bookstores" :key="store.id">
          {{ store.name }} - {{ getBookstoreLocation(store) }}
        </li>
      </ul>
    </section>

    <section class="activity-section">
      <h2>Activity 10: Nested v-for - Authors and Famous Works</h2>
      <p>
        This section uses nested v-for to display each author and their famous works.
      </p>

      <div
        v-for="author in authors"
        :key="author.id"
        class="author-card"
      >
        <h3>{{ author.name }}</h3>

        <ul>
          <li
            v-for="work in author.famousWorks"
            :key="author.id + '-' + getWorkTitle(work)"
          >
            {{ getWorkTitle(work) }}
          </li>
        </ul>
      </div>
    </section>

    <section class="activity-section">
      <h2>Activity 11: v-if - Search Result Display</h2>
      <p>
        This section uses v-if and v-else to display whether the searched author exists.
      </p>

      <div v-if="searchedAuthor" class="result-box">
        Search successful:
        <strong>{{ searchedAuthor.name }}</strong>
        is available in the dataset.
      </div>

      <div v-else class="warning-box">
        The searched author is not available in the dataset.
      </div>
    </section>

    <section class="activity-section">
      <h2>Activity 12: v-show - Toggle Bookstore List</h2>
      <p>
        This section uses v-show to show or hide the bookstore list.
      </p>

      <button class="primary-button" @click="showBookstores = !showBookstores">
        Toggle Bookstores
      </button>

      <div v-show="showBookstores" class="bookstore-box">
        <ul>
          <li v-for="store in bookstores" :key="store.id">
            {{ store.name }} - {{ getBookstoreLocation(store) }}
          </li>
        </ul>
      </div>
    </section>

    <section class="activity-section">
      <h2>Activity 13: v-if and v-else - Toggle Message</h2>
      <p>
        This section uses v-if and v-else to toggle message visibility.
      </p>

      <button class="primary-button" @click="showMessage = !showMessage">
        Toggle Message
      </button>

      <p v-if="showMessage" class="message success">
        ✨ You're a Vue superstar! ✨
      </p>

      <p v-else class="message">
        Click the button to see a message.
      </p>
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
  line-height: 1.6;
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

.result-box {
  padding: 12px;
  border: 1px solid #42b883;
  border-radius: 6px;
  background-color: #e8f7ef;
}

.warning-box {
  padding: 12px;
  border: 1px solid #f0ad4e;
  border-radius: 6px;
  background-color: #fff3cd;
}

.author-card {
  margin-bottom: 16px;
  padding: 14px;
  border: 1px solid #d0d0d0;
  border-radius: 8px;
  background-color: #fafafa;
}

.primary-button {
  margin-top: 8px;
  margin-bottom: 12px;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  background-color: #35495e;
  color: white;
  cursor: pointer;
  font-size: 15px;
}

.bookstore-box {
  margin-top: 12px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #f8f8f8;
}

.message {
  margin-top: 16px;
  font-size: 18px;
}

.success {
  color: #2f7d4e;
  background-color: #e8f7ef;
  border: 1px solid #42b883;
  padding: 12px;
  border-radius: 6px;
}

li {
  margin-bottom: 8px;
}
</style>