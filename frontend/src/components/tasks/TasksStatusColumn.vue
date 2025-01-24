<script lang="ts">

export default {
  data() {
    return {
      status_id: 0,
      status_title: '',
      tasks: [],
    }
  },
  created() {
    this.fetchData();
    console.log(this.tasks)
  },
  methods: {
    fetchData() {
      fetch('http://127.0.0.1:8000/api/v0/tasks').then(response => response.json())
          .then(tasks => this.tasks = tasks);
    }
  }
}
</script>

<template>

</template>

<style scoped>

</style>