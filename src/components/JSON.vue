<!-- JSON.vue - Final Version: Activities 1-13 + Task 2.2 -->
<template>
  <div class="json-lab">
    <h1>🗄️ JSON Data & Vue Directives Lab</h1>

    <!-- Activity 1 -->
    <section class="lab-section">
      <h2>Activity 1: Import JSON Files</h2>
      <p>
        This component imports <code>authors.json</code> and
        <code>bookstores.json</code> from the project assets folder.
      </p>

      <p>
        Total authors:
        <strong>{{ authors.length }}</strong>
      </p>

      <p>
        Bookstore company:
        <strong>{{ bookstores.name }}</strong>
      </p>

      <p>
        Total stores:
        <strong>{{ bookstores.totalStores }}</strong>
      </p>
    </section>

    <!-- Activities 2-5 -->
    <section class="lab-section">
      <h2>Computed Properties</h2>

      <h3>Activity 2: Get Authors Born After 1850</h3>
      <p>
        This computed property filters the authors array and returns authors
        whose birth year is after 1850.
      </p>
      <ul>
        <li v-for="author in modernAuthors" :key="'modern-' + author.id">
          {{ author.name }} ({{ author.birthYear }})
        </li>
      </ul>

      <h3>Activity 3: Get All Famous Works</h3>
      <p>
        This computed property extracts all famous works from all authors.
      </p>
      <ul>
        <li v-for="work in allFamousWorks" :key="work">
          {{ work }}
        </li>
      </ul>

      <h3>Activity 4: Find Author by Name</h3>
      <p>
        This computed property searches for the author named
        <strong>George Orwell</strong>.
      </p>
      <p v-if="orwell" class="message success">
        Finding by property: {{ orwell.name }} was born in {{ orwell.birthYear }}.
      </p>
      <p v-else class="message warning">
        George Orwell was not found.
      </p>

      <h3>Activity 5: Find Author by ID</h3>
      <p>
        This computed property searches for the author with ID 1.
      </p>
      <p v-if="austen" class="message success">
        Finding by ID 1: {{ austen.name }} was born in {{ austen.birthYear }}.
      </p>
      <p v-else class="message warning">
        Author with ID 1 was not found.
      </p>
    </section>

    <!-- Activities 6-9 -->
    <section class="lab-section">
      <h2>📚 Working with JSON Arrays</h2>
      <p>Our <code>authors.json</code> contains an array of author objects.</p>

      <h3>Activity 6: Render a List of Authors</h3>
      <p>All authors and their birth years:</p>
      <ul>
        <li v-for="author in authors" :key="'author-' + author.id">
          {{ author.name }} ({{ author.birthYear }})
        </li>
      </ul>

      <h3>Activity 7: Render Authors Born After 1850</h3>
      <p>Authors born after 1850:</p>
      <ul>
        <li v-for="author in modernAuthors" :key="'render-modern-' + author.id">
          {{ author.name }} ({{ author.birthYear }})
        </li>
      </ul>

      <h3>Activity 8: Render All Famous Works</h3>
      <p>Famous works:</p>
      <ul>
        <li v-for="work in allFamousWorks" :key="'render-work-' + work">
          {{ work }}
        </li>
      </ul>

      <h3>Activity 9: Nested Arrays/Objects</h3>
      <p>{{ austen?.name }}'s works:</p>
      <ul v-if="austen">
        <li v-for="work in austen.famousWorks" :key="'austen-work-' + work.title">
          {{ work.title }} ({{ work.year }})
        </li>
      </ul>
    </section>

    <!-- Activities 9a-12 -->
    <section class="lab-section">
      <h2>🏢 Working with JSON Objects</h2>
      <p>Our <code>bookstores.json</code> is a JSON object.</p>

      <h3>Activity 9a and 9b: Accessing Properties</h3>
      <p>
        Company:
        <strong>{{ bookstores.name }}</strong>
      </p>

      <p>
        Total Stores:
        <strong>{{ bookstores.totalStores }}</strong>
      </p>

      <h3>Activity 10: Iterating Object Properties</h3>
      <p>Store Types:</p>
      <ul>
        <li v-for="(count, type) in bookstores.storeTypes" :key="'store-type-' + type">
          {{ type }}: {{ count }}
        </li>
      </ul>

      <h3>Activity 11: Nested Objects</h3>
      <p>Opening Hours:</p>
      <ul>
        <li v-for="(hours, day) in bookstores.openingHours" :key="'hours-' + day">
          {{ day }}: {{ hours.open }} - {{ hours.close }}
        </li>
      </ul>

      <h3>Activity 12: Working with Arrays in Objects</h3>
      <p>Top sellers:</p>
      <ul>
        <li v-for="book in bookstores.topSellers" :key="'seller-' + book">
          {{ book }}
        </li>
      </ul>

      <p>
        We operate in:
        <strong>{{ bookstores.countries.join(', ') }}</strong>
      </p>

      <p>
        Our #1 seller:
        <strong>{{ bookstores.topSellers[0] }}</strong>
      </p>
    </section>

    <!-- Activity 13 -->
    <section class="lab-section">
      <h2>Activity 13: v-if and v-else</h2>
      <p>Toggle the message visibility when the button is clicked.</p>

      <button @click="showMessage = !showMessage">
        Toggle Message
      </button>

      <p v-if="showMessage" class="message success">
        ✨ You're a Vue superstar! ✨
      </p>

      <p v-else class="message">
        Click the button to see a message.
      </p>
    </section>

    <!-- Task 2.2 -->
    <section class="lab-section">
      <h2>Task 2.2: Attribute, Class and Style Binding with <code>v-bind</code></h2>
      <p>
        George Orwell is highlighted using attribute binding, class binding and style binding.
      </p>

      <ul>
        <li
          v-for="author in authors"
          :key="'highlight-' + author.id"
          :title="isGeorgeOrwell(author) ? 'Highlighted author: George Orwell' : 'Regular author'"
          :class="{ 'highlighted-author': isGeorgeOrwell(author) }"
          :style="isGeorgeOrwell(author) ? highlightedStyle : {}"
        >
          {{ author.name }} ({{ author.birthYear }})
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import authors from '../assets/json/authors.json'
import bookstores from '../assets/json/bookstores.json'

const showMessage = ref(false)

// Activity 2: Get authors born after 1850
const modernAuthors = computed(() => {
  return authors.filter((author) => author.birthYear > 1850)
})

// Activity 3: Get all famous works
const allFamousWorks = computed(() => {
  return authors.flatMap((author) =>
    author.famousWorks.map((work) => `${work.title} (${work.year})`)
  )
})

// Activity 4: Find author by name
const orwell = computed(() => {
  return authors.find((author) => author.name === 'George Orwell')
})

// Activity 5: Find author by ID
const austen = computed(() => {
  return authors.find((author) => author.id === 1)
})

// Task 2.2: Highlight George Orwell
const isGeorgeOrwell = (author) => {
  return author.name.trim().toLowerCase() === 'george orwell'
}

const highlightedStyle = {
  backgroundColor: '#fff3cd',
  border: '2px solid #f0ad4e',
  fontWeight: 'bold',
  fontSize: '20px',
  padding: '10px',
  borderRadius: '6px',
  display: 'inline-block'
}
</script>

<style scoped>
.json-lab {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  max-width: 80vw;
  margin: 0 auto;
  padding: 20px;
  background-color: #f4f4f4;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1,
h2 {
  color: #333;
}

h1 {
  text-align: center;
}

.lab-section {
  background-color: white;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message {
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
}

.success {
  background-color: #e7faf3;
  color: #42b883;
  border: 1px solid #42b883;
}

.warning {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #f0ad4e;
}

.highlighted-author {
  background-color: #fff3cd;
  border: 2px solid #f0ad4e;
  font-weight: bold;
  font-size: 20px;
  padding: 10px;
  border-radius: 6px;
  display: inline-block;
}

code {
  background-color: #e0e0e0;
  padding: 2px 5px;
  border-radius: 4px;
  font-family: "Courier New", Courier, monospace;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #f0f0f0;
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
}

button {
  padding: 8px 14px;
  border: none;
  border-radius: 5px;
  background-color: #42b883;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #36966f;
}
</style>