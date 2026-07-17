<template>
  <div class="border-bottom">
    <div class="container">
      <header
        class="d-flex justify-content-center py-3"
      >
        <ul class="nav nav-pills">
          <li class="nav-item">
            <RouterLink
              to="/"
              class="nav-link"
              active-class="active"
            >
              Home (Week 5)
            </RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink
              to="/about"
              class="nav-link"
              active-class="active"
            >
              About
            </RouterLink>
          </li>

          <li
            v-if="!isAuthenticated"
            class="nav-item"
          >
            <RouterLink
              to="/login"
              class="nav-link"
              active-class="active"
            >
              Login
            </RouterLink>
          </li>

          <li
            v-else
            class="nav-item"
          >
            <button
              type="button"
              class="nav-link logout-button"
              @click="handleLogout"
            >
              Logout
            </button>
          </li>
        </ul>
      </header>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

import {
  isAuthenticated,
  logout
} from '../auth'

const router = useRouter()

const handleLogout = () => {
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