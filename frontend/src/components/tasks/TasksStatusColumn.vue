<script lang="ts">

import axios from "axios";

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
      axios.get('http://localhost:8000/api/v0/tasks', { withCredentials: true })
          .then(response => this.tasks = response.data);
    }
  }
}
</script>

<template>

</template>

<style scoped>

</style>