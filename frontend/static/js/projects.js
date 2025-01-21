import {createApp} from "https://unpkg.com/vue@3/dist/vue.esm-browser.js";
import ProjectsComponent from "./components/ProjectsComponent.vue";


createApp({
    delimiters: ["[[", "]]"],
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
}).component('ProjectsComponent', ProjectsComponent).mount('#projects')
