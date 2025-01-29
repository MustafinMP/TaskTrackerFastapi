<script lang="ts">
import axios from 'axios'

export default {
  data() {
    return {
      projects: [],
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:8000/api/v0/projects/all', { withCredentials: true })
          .then(response => this.projects = response.data)
          .catch(error => console.error('Error fail:', error));
    }
  }
}
</script>

<template>
  <a v-for="project in projects" class="white-filled border-1r project-card" :href="project.id">
    <h6>Project title{{ project.title }}</h6>
    <div class="member-block">
      <div class="member-images">

      </div>
      <div class="member-count">
      </div>
    </div>
    <div class="tasks">team tasks count</div>
  </a>
</template>

<style scoped>
.project-card {
  display: block;
  padding: 1.2rem 2rem;
  margin-top: 2rem;
}

.project-card h6 {
  font-size: 1.5rem;
}

.member-block {
  display: grid;
  grid-template-columns: minmax(2.5rem, 10.5rem) 1fr;
  height: 2.5rem;
  margin-top: 1rem;
}

.member-images {
  height: 2.5rem;
}

.member-images img {
  width: 2.5rem;
  height: 2.5rem;
  border: 1px solid var(--color-secondary);
  border-radius: 0.25rem;
  position: relative;
}

.member-count {
  height: 2.5rem;
  padding-top: 0.4rem;
}

.member-count-num {
  font-size: 1.2rem;
  font-weight: 600;
}
</style>