<script lang="ts">
export default {
  data() {
    return {
      projects: [],
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
      fetch('http://127.0.0.1:8000/api/v0/projects/all').then(response => response.json())
          .then(projects => this.projects = projects);

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