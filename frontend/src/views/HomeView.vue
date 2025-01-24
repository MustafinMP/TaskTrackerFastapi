<script setup lang="ts">
import Navbar from '../components/Navbar.vue'
import PageHeader from "@/components/PageHeader.vue";
</script>

<template>
  <main class="main-with-navbar">
    <Navbar current-page="home"/>
    <div class="main-block">
      <PageHeader header-text="Home page" />
      <div class="main-content">
        <div>Content</div>

      </div>
    </div>
  </main>
</template>