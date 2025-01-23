<script lang="ts">
import router from "@/router";

export default{
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    sendForm(email: any, password: string) {
      let data = {
        email: email,
        password: password
      };
      console.log(data);
      fetch('http://localhost:8000/api/v0/auth/login', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'}
      });
      router.push('/');
    }
  }
}
</script>

<template>
  <div class="auth-form needs-validation white-filled">
    <h1>Вход</h1>
    <div>
      Email<br>
      <input v-model="email" name="email" placeholder="Enter email" class="form-control" type="email"/><br>
    </div>
    <div>
      Password<br>
      <input v-model="password" name="password" placeholder="Enter password" class="form-control"
             type="password"/><br>
    </div>
    <button class="form-button primary-filled" @click="sendForm(email, password)">Войти</button>
    <hr width="100%" size="2">
    <a href="/auth/register" class="register-a light-filled">
      Зарегистрироваться
    </a>
    <section class="social-login">
      <a href="" class="yandex-login-a light-filled">
        <div></div>
        <img src="../assets/yandex_logo.png" alt="Yandex"
             style="width: 2rem; height: 2rem; border-radius: 50%; pointer-events: none; margin: 0;"/>
        <div></div>
      </a>
    </section>
  </div>
</template>

<style scoped>
.auth-form {
  width: 30%;
  margin: 10rem 35% 0 35%;
  background: var(--color-white);
  padding: 4rem;
}

.form-button {
  display: block;
  height: 3.5rem;
  width: 100%;
  font-size: 1.4rem;
  padding: 0.7rem;
  margin: 1rem 0;
  border: none;
  border-radius: 0.5rem;
  color: var(--color-light) !important;
}

.register-a, .login-a {
  display: block;
  height: 3.5rem;
  text-decoration: none;
  text-align: center;
  font-size: 1.4rem;
  padding: 0.7rem;
  margin: 1rem 0;
  border-radius: 0.5rem;
}

.load-image-block {
  display: grid;
  grid-template-columns: 1fr 3.5rem;
  height: 3.5rem;
  gap: 1rem;
}

.load-image-block * {
  margin: 0;
}

.social-login {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  margin: 1rem 0;
  gap: 1rem;
  border-radius: 0.5rem;
}

.yandex-login-a {
  display: grid;
  grid-template-columns: 1fr 2rem 1fr;
  height: 3.5rem;
  text-decoration: none;
  margin-bottom: 1rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
}

body {
  background: var(--color-light) !important;
}
</style>