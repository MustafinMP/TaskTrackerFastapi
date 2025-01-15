import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

createApp({
    data() {
        return {
            email: '',
            password: '',
        }
    },
    delimiters: ["[[", "]]"],
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    methods: {
        sendForm(email, password) {
            fetch('http://localhost:8000/api/v0/auth/login', {
                method: 'POST',
                body: JSON.stringify({
                    email: email,
                    password: password
                }),
                headers: {'Content-Type': 'application/json'}
            });
            {

            }
        }
    }
}).mount('#form')