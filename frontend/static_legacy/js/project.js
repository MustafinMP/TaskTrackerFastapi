import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'
import SingleProject from "./components/SingleProject.vue";


createApp({
    components: {
        SingleProject
    }
}).mount('#projects')