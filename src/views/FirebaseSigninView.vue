<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-md-7 col-lg-6 mx-auto">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h1 class="text-center mb-2">Firebase Sign In</h1>

            <p class="text-center text-muted mb-4">Sign in with a registered library account.</p>

            <form @submit.prevent="handleSignIn">
              <div class="mb-3">
                <label for="firebase-login-email" class="form-label"> Email address </label>
                <input
                  id="firebase-login-email"
                  v-model.trim="email"
                  type="email"
                  class="form-control"
                  autocomplete="email"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="firebase-login-password" class="form-label"> Password </label>
                <input
                  id="firebase-login-password"
                  v-model="password"
                  type="password"
                  class="form-control"
                  autocomplete="current-password"
                  minlength="6"
                  required
                />
              </div>

              <div v-if="errorMessage" class="alert alert-danger" role="alert">
                {{ errorMessage }}
              </div>

              <div v-if="successMessage" class="alert alert-success" role="status">
                {{ successMessage }}
              </div>

              <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
                {{ isSubmitting ? 'Signing in...' : 'Sign in' }}
              </button>
            </form>

            <p class="text-center mt-4 mb-0">
              New to Hwang Library?
              <RouterLink to="/FireRegister"> Create a Firebase account </RouterLink>
            </p>
          </div>
        </div>

        <div v-if="firebaseUser" class="alert alert-info mt-4">
          Signed in as <strong>{{ firebaseUser.email }}</strong> with the
          <strong>{{ firebaseRole }}</strong> role.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { signInWithEmailAndPassword } from 'firebase/auth'

import { auth } from '../firebase'
import { firebaseRole, firebaseUser } from '../firebaseAuth'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isSubmitting = ref(false)

const handleSignIn = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isSubmitting.value = true

  try {
    const credential = await signInWithEmailAndPassword(auth, email.value, password.value)

    console.log('Firebase current user after sign in:', credential.user)

    successMessage.value =
      `Welcome back, ${credential.user.email}. ` + `Role: ${firebaseRole.value}.`
  } catch (error) {
    errorMessage.value = error.message
    console.error('Firebase sign-in error:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>
