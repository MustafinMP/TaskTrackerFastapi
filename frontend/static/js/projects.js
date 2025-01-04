import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'


createApp({
    data() {
        return {
            projects: null,
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
}).mount('#projects')