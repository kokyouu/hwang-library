<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-md-7 col-lg-6 mx-auto">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h1 class="text-center mb-2">Firebase Registration</h1>

            <p class="text-center text-muted mb-4">Create an account for Hwang Library.</p>

            <form @submit.prevent="handleRegistration">
              <div class="mb-3">
                <label for="firebase-register-email" class="form-label"> Email address </label>
                <input
                  id="firebase-register-email"
                  v-model.trim="email"
                  type="email"
                  class="form-control"
                  autocomplete="email"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="firebase-register-password" class="form-label"> Password </label>
                <input
                  id="firebase-register-password"
                  v-model="password"
                  type="password"
                  class="form-control"
                  autocomplete="new-password"
                  minlength="6"
                  required
                />
                <div class="form-text">Use at least six characters.</div>
              </div>

              <div class="mb-3">
                <label for="firebase-register-role" class="form-label"> Library role </label>
                <select id="firebase-register-role" v-model="role" class="form-select">
                  <option>Member</option>
                  <option>Librarian</option>
                </select>
              </div>

              <div v-if="errorMessage" class="alert alert-danger" role="alert">
                {{ errorMessage }}
              </div>

              <div v-if="successMessage" class="alert alert-success" role="status">
                {{ successMessage }}
              </div>

              <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
                {{ isSubmitting ? 'Creating account...' : 'Register' }}
              </button>
            </form>

            <p class="text-center mt-4 mb-0">
              Already registered?
              <RouterLink to="/FireLogin"> Sign in to Firebase </RouterLink>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createUserWithEmailAndPassword } from 'firebase/auth'

import { auth } from '../firebase'
import { saveFirebaseRole } from '../firebaseAuth'

const email = ref('')
const password = ref('')
const role = ref('Member')
const errorMessage = ref('')
const successMessage = ref('')
const isSubmitting = ref(false)

const handleRegistration = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isSubmitting.value = true

  try {
    const credential = await createUserWithEmailAndPassword(auth, email.value, password.value)

    saveFirebaseRole(credential.user.email, role.value)

    console.log('Firebase current user after registration:', credential.user)

    successMessage.value =
      `Registration completed for ${credential.user.email}. ` + `Assigned role: ${role.value}.`
  } catch (error) {
    errorMessage.value = error.message
    console.error('Firebase registration error:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>
