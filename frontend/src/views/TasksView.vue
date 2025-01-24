<script lang="ts">

import Navbar from "@/components/Navbar.vue";
import PageHeader from "@/components/PageHeader.vue";
import ProjectCards from "@/components/projects/ProjectCards.vue";

export default {
  components: {ProjectCards, PageHeader, Navbar}

}
</script>

<template>
  <main class="main-with-navbar">
    <Navbar current-page="projects"/>
    <div class="main-block">
      <PageHeader header-text="Projects"/>
      <div class="main-content grid-3">

      </div>
    </div>
  </main>
</template>

<style scoped>
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
</style>