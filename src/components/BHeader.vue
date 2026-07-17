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
        </ul>
      </header>
    </div>
  </div>
</template>