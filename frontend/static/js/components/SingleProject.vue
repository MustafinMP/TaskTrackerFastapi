<script>
export default {
  props: {
    projectId: {
      type: Number,
    }
  },
  data() {
    return {
      project: null,
    }
  },
  created() {
    this.fetchData();
  },
  delimiters: ["[[", "]]"],
  compilerOptions: {
    delimiters: ["[[", "]]"]
  },
  methods: {
    fetchData() {
      fetch(`http://127.0.0.1:8000/api/v0/project/${this.projectId}`).then(response => response.json())
          .then(project => this.project = project);

    }
  }
}
</script>

<template>
  <h1>hi</h1>
  [[ project.title ]]
</template>

<style scoped>

</style>