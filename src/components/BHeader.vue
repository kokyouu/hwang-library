<template>
  <div class="border-bottom">
    <div class="container">
      <header class="d-flex justify-content-center py-3">
        <ul class="nav nav-pills">
          <li class="nav-item">
            <RouterLink to="/" class="nav-link" active-class="active"> Home </RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink to="/about" class="nav-link" active-class="active"> About </RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink to="/addbook" class="nav-link" active-class="active">
              Add Books
            </RouterLink>
          </li>

          <!-- Lab 5 local authentication -->
          <li v-if="!isAuthenticated" class="nav-item">
            <RouterLink to="/login" class="nav-link" active-class="active">
              Local Login
            </RouterLink>
          </li>

          <li v-else class="nav-item">
            <button type="button" class="nav-link logout-button" @click="handleLocalLogout">
              Local Logout
            </button>
          </li>

          <!-- Lab 7 Firebase authentication -->
          <li v-if="!firebaseUser" class="nav-item">
            <RouterLink to="/FireRegister" class="nav-link" active-class="active">
              Firebase Register
            </RouterLink>
          </li>

          <li v-if="!firebaseUser" class="nav-item">
            <RouterLink to="/FireLogin" class="nav-link" active-class="active">
              Firebase Login
            </RouterLink>
          </li>

          <li v-else class="nav-item">
            <RouterLink to="/FireLogout" class="nav-link" active-class="active">
              Firebase Logout
            </RouterLink>
          </li>
        </ul>
      </header>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

import { isAuthenticated, logout } from '../auth'
import { firebaseUser } from '../firebaseAuth'

const router = useRouter()

const handleLocalLogout = () => {
  logout()
  router.push('/login')
}
</script>

<style scoped>
.logout-button {
  border: 0;
  background: transparent;
}
</style>
