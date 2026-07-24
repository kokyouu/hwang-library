<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-md-7 col-lg-6 mx-auto">
        <div class="card shadow-sm">
          <div class="card-body p-4 text-center">
            <h1 class="mb-3">Firebase Logout</h1>

            <p v-if="firebaseUser" class="mb-4">
              You are currently signed in as
              <strong>{{ firebaseUser.email }}</strong>
              ({{ firebaseRole }}).
            </p>

            <p v-else class="mb-4">There is no Firebase user currently signed in.</p>

            <button
              type="button"
              class="btn btn-danger"
              :disabled="!firebaseUser || isSubmitting"
              @click="handleLogout"
            >
              {{ isSubmitting ? 'Signing out...' : 'Sign out' }}
            </button>

            <div v-if="successMessage" class="alert alert-success mt-4 mb-0" role="status">
              {{ successMessage }}
            </div>

            <div v-if="errorMessage" class="alert alert-danger mt-4 mb-0" role="alert">
              {{ errorMessage }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { signOut } from 'firebase/auth'

import { auth } from '../firebase/init'
import { firebaseRole, firebaseUser } from '../firebaseAuth'

const successMessage = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

const handleLogout = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    await signOut(auth)
    console.log('Firebase current user after logout:', auth.currentUser)
    successMessage.value = 'You have been signed out. Current Firebase user: null.'
  } catch (error) {
    errorMessage.value = error.message
    console.error('Firebase sign-out error:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>
