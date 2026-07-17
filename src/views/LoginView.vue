<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-md-6 col-lg-5 mx-auto">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h1 class="text-center mb-4">
              Member Login
            </h1>

            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label
                  for="login-username"
                  class="form-label"
                >
                  Username
                </label>

                <input
                  id="login-username"
                  v-model="username"
                  type="text"
                  class="form-control"
                />
              </div>

              <div class="mb-3">
                <label
                  for="login-password"
                  class="form-label"
                >
                  Password
                </label>

                <input
                  id="login-password"
                  v-model="password"
                  type="password"
                  class="form-control"
                />
              </div>

              <div
                v-if="errorMessage"
                class="alert alert-danger"
              >
                {{ errorMessage }}
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
              >
                Login
              </button>
            </form>

            <div class="mt-4 text-muted small">
              <div>Lab credentials:</div>
              <div>Username: libraryUser</div>
              <div>Password: Library123!</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  useRoute,
  useRouter
} from 'vue-router'

import { login } from '../auth'

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const route = useRoute()
const router = useRouter()

const handleLogin = () => {
  const loginSucceeded = login(
    username.value,
    password.value
  )

  if (!loginSucceeded) {
    errorMessage.value =
      'Invalid username or password.'
    return
  }

  errorMessage.value = ''

  const redirectPath =
    route.query.redirect || '/about'

  router.push(redirectPath)
}
</script>