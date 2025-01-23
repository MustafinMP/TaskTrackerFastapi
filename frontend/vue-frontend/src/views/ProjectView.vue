<script setup lang="ts">
import ProjectCards from '../components/projects/ProjectCards.vue'
import Navbar from "@/components/Navbar.vue";
import PageHeader from "@/components/PageHeader.vue";


</script>

<template>
  <main class="main-with-navbar">
    <Navbar current-page="projects"/>
    <div class="main-block">
      <PageHeader header-text="Projects"/>
      <div class="main-content">
        <ProjectCards/>
      </div>
    </div>
  </main>
</template>

<style scoped>
</style>