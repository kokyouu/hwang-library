<script setup>
import BHeader from './components/BHeader.vue'
</script>

<template>
  <div class="app-container">
    <BHeader />

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}

html,
body,
#app {
  min-height: 100%;
  margin: 0;
}

body {
  font-family:
    Arial,
    Helvetica,
    sans-serif;
}

.main-content {
  padding-bottom: 4rem;
}
</style>