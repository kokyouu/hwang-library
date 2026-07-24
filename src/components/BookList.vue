<template>
  <section class="book-list-panel" aria-labelledby="book-list-heading">
    <div class="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-3">
      <div>
        <h2 id="book-list-heading" class="h4 mb-1">Books with ISBN greater than 1000</h2>
        <p class="text-muted small mb-0">Up to five books, ordered by ISBN.</p>
      </div>

      <button
        type="button"
        class="btn btn-outline-secondary btn-sm"
        :disabled="isLoading"
        data-testid="refresh-books-button"
        @click="fetchBooks"
      >
        Refresh
      </button>
    </div>

    <div class="query-summary mb-3" aria-label="Firestore query constraints">
      <code>where('isbn', '&gt;', 1000)</code>
      <code>orderBy('isbn', 'asc')</code>
      <code>limit(5)</code>
    </div>

    <div v-if="actionMessage" class="alert alert-success py-2" role="status">
      {{ actionMessage }}
    </div>

    <div v-if="errorMessage" class="alert alert-danger py-2" role="alert">
      {{ errorMessage }}
    </div>

    <div v-if="isLoading" class="text-muted py-4 text-center">Loading Firestore books...</div>

    <div v-else-if="books.length === 0" class="empty-state">No books match the current query.</div>

    <div v-else class="table-responsive">
      <table class="table align-middle mb-0" data-testid="book-table">
        <thead>
          <tr>
            <th scope="col">ISBN</th>
            <th scope="col">Book name</th>
            <th scope="col" class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id" :data-testid="`book-row-${book.id}`">
            <template v-if="editingId === book.id">
              <td>
                <input
                  v-model.number="editIsbn"
                  class="form-control form-control-sm"
                  type="number"
                  min="1"
                  step="1"
                  :aria-label="`ISBN for ${book.name}`"
                />
              </td>
              <td>
                <input
                  v-model.trim="editName"
                  class="form-control form-control-sm"
                  type="text"
                  maxlength="120"
                  :aria-label="`Book name for ISBN ${book.isbn}`"
                />
              </td>
              <td class="text-end text-nowrap">
                <button
                  type="button"
                  class="btn btn-success btn-sm me-2"
                  @click="saveBook(book.id)"
                >
                  Save
                </button>
                <button type="button" class="btn btn-outline-secondary btn-sm" @click="cancelEdit">
                  Cancel
                </button>
              </td>
            </template>

            <template v-else>
              <td class="isbn-cell">{{ book.isbn }}</td>
              <td>{{ book.name }}</td>
              <td class="text-end text-nowrap">
                <button
                  type="button"
                  class="btn btn-outline-primary btn-sm me-2"
                  :aria-label="`Edit ${book.name}`"
                  @click="startEdit(book)"
                >
                  Edit
                </button>
                <button
                  type="button"
                  class="btn btn-outline-danger btn-sm"
                  :aria-label="`Delete ${book.name}`"
                  @click="removeBook(book)"
                >
                  Delete
                </button>
              </td>
            </template>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import {
  collection,
  deleteDoc,
  doc,
  getDocs,
  limit,
  orderBy,
  query,
  serverTimestamp,
  updateDoc,
  where
} from 'firebase/firestore'

import { db } from '../firebase/init'

const props = defineProps({
  refreshKey: {
    type: Number,
    default: 0
  }
})

const books = ref([])
const isLoading = ref(false)
const actionMessage = ref('')
const errorMessage = ref('')
const editingId = ref('')
const editIsbn = ref('')
const editName = ref('')

const fetchBooks = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const booksQuery = query(
      collection(db, 'books'),
      where('isbn', '>', 1000),
      orderBy('isbn', 'asc'),
      limit(5)
    )
    const snapshot = await getDocs(booksQuery)

    books.value = snapshot.docs.map((bookDocument) => ({
      id: bookDocument.id,
      ...bookDocument.data()
    }))
  } catch (error) {
    errorMessage.value = error.message
    console.error('Error fetching books:', error)
  } finally {
    isLoading.value = false
  }
}

const startEdit = (book) => {
  editingId.value = book.id
  editIsbn.value = book.isbn
  editName.value = book.name
  actionMessage.value = ''
}

const cancelEdit = () => {
  editingId.value = ''
}

const saveBook = async (bookId) => {
  const isbnNumber = Number(editIsbn.value)

  if (!Number.isInteger(isbnNumber) || isbnNumber <= 0 || !editName.value.trim()) {
    errorMessage.value = 'Enter a valid ISBN and book name before saving.'
    return
  }

  try {
    await updateDoc(doc(db, 'books', bookId), {
      isbn: isbnNumber,
      name: editName.value.trim(),
      updatedAt: serverTimestamp()
    })

    editingId.value = ''
    actionMessage.value = `Updated "${editName.value.trim()}" in Firestore.`
    await fetchBooks()
  } catch (error) {
    errorMessage.value = error.message
    console.error('Error updating book:', error)
  }
}

const removeBook = async (book) => {
  try {
    await deleteDoc(doc(db, 'books', book.id))
    actionMessage.value = `Deleted "${book.name}" from Firestore.`
    await fetchBooks()
  } catch (error) {
    errorMessage.value = error.message
    console.error('Error deleting book:', error)
  }
}

watch(() => props.refreshKey, fetchBooks)
onMounted(fetchBooks)
</script>

<style scoped>
.book-list-panel {
  min-width: 0;
  padding: 1.25rem;
  border-top: 3px solid #3156d9;
  background: #ffffff;
}

.query-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.query-summary code {
  padding: 0.3rem 0.5rem;
  border: 1px solid #cfd7e3;
  border-radius: 4px;
  color: #26344d;
  background: #f4f6f9;
  font-size: 0.78rem;
}

.empty-state {
  padding: 2rem;
  border: 1px dashed #bbc3cf;
  color: #5c6675;
  text-align: center;
}

.isbn-cell {
  font-family: Consolas, 'Courier New', monospace;
  font-size: 0.9rem;
}

th {
  color: #4b5563;
  font-size: 0.78rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
</style>
