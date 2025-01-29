<script lang="ts">
import axios from "axios";

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
          .then(response => this.projects = response.data);
    }
  }

}
</script>

<template>
<!--  <section>-->
    <article class="white-filled border-1r">Мои проекты!</article>
<!--    <a v-for="projects in projects" class="white-filled border-1r projects-card" :href="[[ projects.id ]]">-->
<!--      <h6>Project title[[ projects.title ]]</h6>-->
<!--      <div class="member-block">-->
<!--        <div class="member-images">-->

<!--        </div>-->
<!--        <div class="member-count">-->
<!--        </div>-->
<!--      </div>-->
<!--      <div class="tasks">team tasks count</div>-->
<!--    </a>-->
<!--  </section>-->

</template>

<style scoped>
#aside-navbar-projects {
  @extend .dark-filled;
}
</style>