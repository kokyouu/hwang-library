<template>
  <div class="container py-5">
    <div class="page-heading mb-4">
      <p class="section-label mb-2">Assessed Lab 8</p>
      <h1 class="mb-2">Firestore Book Manager</h1>
      <p class="text-muted mb-0">Add a book, then manage the filtered Firestore results.</p>
    </div>

    <div class="book-layout">
      <section class="book-form-panel" aria-labelledby="add-book-heading">
        <h2 id="add-book-heading" class="h4 mb-3">Add a book</h2>

        <form data-testid="add-book-form" @submit.prevent="addBook">
          <div class="mb-3">
            <label for="book-isbn" class="form-label">ISBN</label>
            <input
              id="book-isbn"
              v-model.number="isbn"
              class="form-control"
              type="number"
              min="1"
              step="1"
              placeholder="For example, 9780132350884"
              required
            />
            <div class="form-text">ISBN is saved to Firestore as a number.</div>
          </div>

          <div class="mb-4">
            <label for="book-name" class="form-label">Book name</label>
            <input
              id="book-name"
              v-model.trim="name"
              class="form-control"
              type="text"
              maxlength="120"
              placeholder="Enter the book title"
              required
            />
          </div>

          <button
            type="submit"
            class="btn btn-primary w-100"
            :disabled="isSubmitting"
            data-testid="add-book-button"
          >
            {{ isSubmitting ? 'Adding book...' : 'Add book' }}
          </button>
        </form>

        <div v-if="successMessage" class="alert alert-success mt-3 mb-0" role="status">
          {{ successMessage }}
        </div>

        <div v-if="errorMessage" class="alert alert-danger mt-3 mb-0" role="alert">
          {{ errorMessage }}
        </div>
      </section>

      <BookList :refresh-key="refreshKey" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { addDoc, collection, serverTimestamp } from 'firebase/firestore'

import BookList from '../components/BookList.vue'
import { db } from '../firebase/init'

const isbn = ref('')
const name = ref('')
const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const refreshKey = ref(0)

const addBook = async () => {
  const isbnNumber = Number(isbn.value)

  successMessage.value = ''
  errorMessage.value = ''

  if (!Number.isInteger(isbnNumber) || isbnNumber <= 0) {
    errorMessage.value = 'Enter a valid positive ISBN number.'
    return
  }

  isSubmitting.value = true

  try {
    await addDoc(collection(db, 'books'), {
      isbn: isbnNumber,
      name: name.value.trim(),
      createdAt: serverTimestamp()
    })

    successMessage.value = `Added "${name.value.trim()}" to Firestore.`
    isbn.value = ''
    name.value = ''
    refreshKey.value += 1
  } catch (error) {
    errorMessage.value = error.message
    console.error('Error adding book:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.page-heading {
  max-width: 760px;
}

.section-label {
  color: #b42318;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.book-layout {
  display: grid;
  grid-template-columns: minmax(260px, 0.72fr) minmax(0, 1.7fr);
  gap: 1.5rem;
  align-items: start;
}

.book-form-panel {
  padding: 1.25rem;
  border: 1px solid #d7dde5;
  border-radius: 6px;
  background: #ffffff;
}

@media (max-width: 900px) {
  .book-layout {
    grid-template-columns: 1fr;
  }
}
</style>
