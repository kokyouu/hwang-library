<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-md-7 mx-auto text-center">
        <div class="alert alert-warning p-5">
          <h1>Access Denied</h1>

          <p class="lead mt-3">
            You must log in before accessing the
            members-only About page.
          </p>

          <RouterLink
            :to="loginDestination"
            class="btn btn-primary mt-3"
          >
            Go to Login
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const loginDestination = computed(() => ({
  path: '/login',
  query: {
    redirect:
      route.query.redirect || '/about'
  }
}))
</script>