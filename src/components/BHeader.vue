<script setup lang="ts">
import { BookOpenCheck, Braces, CloudSun, ShoppingBag } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'
</script>

<template>
  <header class="site-header">
    <div class="header-inner">
      <RouterLink class="brand" to="/BookCounter" aria-label="Hwang Library Cloud Lab">
        <span class="brand-mark">HL</span>
        <span>
          <strong>Hwang Library</strong>
          <small>Cloud Lab</small>
        </span>
      </RouterLink>

      <nav aria-label="Primary navigation">
        <RouterLink to="/BookCounter">
          <BookOpenCheck :size="18" aria-hidden="true" />
          <span>Book Counter</span>
        </RouterLink>
        <RouterLink to="/DataMarketplace">
          <ShoppingBag :size="18" aria-hidden="true" />
          <span>Data Marketplace</span>
        </RouterLink>
        <RouterLink to="/GetAllBookAPI">
          <Braces :size="18" aria-hidden="true" />
          <span>All Books API</span>
        </RouterLink>
        <RouterLink to="/WeatherCheck">
          <CloudSun :size="18" aria-hidden="true" />
          <span>Weather</span>
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  border-bottom: 1px solid #dadce0;
  background: #fff;
}

.header-inner {
  width: min(1120px, calc(100% - 40px));
  min-height: 72px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #202124;
  text-decoration: none;
}

.brand-mark {
  width: 38px;
  height: 38px;
  border-radius: 5px;
  display: grid;
  place-items: center;
  color: #fff;
  background: #a01d2d;
  font-size: 0.85rem;
  font-weight: 800;
}

.brand strong,
.brand small {
  display: block;
  letter-spacing: 0;
}

.brand strong {
  font-size: 0.96rem;
}

.brand small {
  margin-top: 2px;
  color: #71757a;
  font-size: 0.75rem;
}

nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

nav a {
  min-height: 40px;
  border-radius: 5px;
  padding: 0 12px;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: #55595e;
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
}

nav a:hover {
  color: #202124;
  background: #f1f2f3;
}

nav a.router-link-active {
  color: #8e1928;
  background: #faecee;
}

@media (max-width: 720px) {
  .header-inner {
    width: 100%;
    min-height: auto;
    padding: 12px;
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
  }

  nav {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  nav a {
    min-width: 0;
    height: 48px;
    padding: 0 5px;
    justify-content: center;
    font-size: 0.76rem;
    text-align: center;
  }

  nav a span {
    line-height: 1.15;
    white-space: normal;
  }
}
</style>
