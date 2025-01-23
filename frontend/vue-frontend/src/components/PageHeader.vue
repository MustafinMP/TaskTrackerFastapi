<script setup lang="ts">
defineProps<{
  headerText: string
}>()
</script>

<template>
  <section class="page-header">
    <h1>{{ headerText }}</h1>
  </section>
</template>

<style scoped>
.page-header {
  margin: 3rem 7rem 3rem 7rem;
}
</style>