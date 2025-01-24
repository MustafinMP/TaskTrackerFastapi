<script setup lang="ts">
import {RouterLink} from 'vue-router'

defineProps(['currentPage'])
</script>

<template>
  <aside class="aside-navbar white-filled">
    <nav class="container-navbar">
      <RouterLink to="/profile" id="aside-navbar-profile" class="navbar-item"
                  :class="[ currentPage == 'profile' ? 'dark-filled' : 'white-filled-with-hover' ]">
        <i class="bi bi-person-circle"></i>
        <div class="">Profile</div>
      </RouterLink>
      <RouterLink to="/" id="aside-navbar-home" class="navbar-item"
                  :class="[ currentPage == 'home' ? 'dark-filled' : 'white-filled-with-hover']">
        <i class="bi bi-house"></i>
        <div class="">Home</div>
      </RouterLink>
      <RouterLink to="/projects" id="aside-navbar-projects" class="navbar-item"
                  :class="[ currentPage == 'projects' ? 'dark-filled' : 'white-filled-with-hover']">
        <i class="bi bi-people"></i>
        <div class="">Projects</div>
      </RouterLink>
      <RouterLink to="/tasks" id="aside-navbar-tasks" class="navbar-item"
                  :class="[ currentPage == 'tasks' ? 'dark-filled' : 'white-filled-with-hover']">
        <i class="bi bi-list-task"></i>
        <div class="">Tasks</div>
      </RouterLink>
      <RouterLink to="/" id="aside-navbar-create" class="navbar-item"
                  :class="[ currentPage == 'create' ? 'dark-filled' : 'white-filled-with-hover']">
        <i class="bi bi-plus-circle"></i>
        <div class="">Create task</div>
      </RouterLink>
    </nav>
  </aside>
</template>

<style scoped>
.aside-navbar {
  height: 100vh;
  width: 20rem;
  position: sticky;
  top: 0;
  margin: 0;
  padding: 15rem 2rem 2rem;
}

.container-navbar {
  height: 30rem;
}

.aside-navbar {
  display: grid;
  gap: 1rem;
}

.navbar-item {
  display: grid;
  grid-template-columns: 1fr 5fr 1fr;
  height: 3.5rem;
  text-decoration: none;
  margin: 1.5rem 0 1rem 1rem;
  border-radius: 0.5rem;
  position: sticky;
}

.navbar-item * {
  padding: 1rem;
  font-size: 1.1rem;
}



</style>