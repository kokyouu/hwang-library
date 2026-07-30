<script setup lang="ts">
import { RouterView } from 'vue-router'
import BHeader from './components/BHeader.vue'
</script>

<template>
  <div class="app-shell">
    <BHeader />
    <main class="page-shell">
      <RouterView />
    </main>
  </div>
</template>
