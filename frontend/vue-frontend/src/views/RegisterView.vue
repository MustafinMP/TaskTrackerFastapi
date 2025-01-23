<script setup lang="ts">

</script>

<template>
  <form action="http://localhost:8000/api/v0/auth/register" method="post" class="auth-form needs-validation white-filled"
        enctype="multipart/form-data">
    <h1>Регистрация</h1>
    <div>
      Name<br>
      <input v-model="name" name="name" placeholder="Enter name" class="form-control"/><br>
    </div>
    <div>
      Email<br>
      <input v-model="email" name="email" placeholder="Enter email" class="form-control" type="email"/><br>
    </div>
    <div>
      Password<br>
      <input v-model="password" name="password" placeholder="Enter password" class="form-control"
             type="password"/><br>
    </div>
    <div>
      Password<br>
      <input v-model="password_again" name="password_again" placeholder="Enter password again" class="form-control"
             type="password"/><br>
    </div>
    <button class="form-button primary-filled" @click="sendForm(name, email, password, password_again)">
      Зарегистрироваться
    </button>
    <hr width="100%" size="2">
    <a href="/auth/login" class="login-a light-filled">
      Войти в Lite Tracker
    </a>
  </form>
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