import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

createApp({
    data() {
        return {
            name: '',
            email: '',
            password: '',
            password_again: ''
        }
    },
    delimiters: ["[[", "]]"],
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    methods: {
        sendForm(name, email, password, password_again) {
            fetch('http://localhost:8000/api/v0/auth/register', {
                method: 'POST',
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password,
                    password_again: password_again
                }),
                headers: {'Content-Type': 'application/json'}
            });
            {

            }
        }
    }
}).mount('#form')