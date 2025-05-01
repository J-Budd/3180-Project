<template>
  <div class="register-container">
    <div class="form-box">
      <h2 class="title">Jam-Date</h2>
      <form @submit.prevent="registerUser">
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <input v-model="name" type="text" placeholder="Full Name" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <input type="file" @change="handleFileUpload" />
        <button type="submit">Register</button>
        <p class="error" v-if="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      name: '',
      email: '',
      profile: null,
      error: ''
    };
  },
  methods: {
    handleFileUpload(event) {
      this.profile = event.target.files[0];
    },
    async registerUser() {
      try {
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('password', this.password);
        formData.append('name', this.name);
        formData.append('email', this.email);
        if (this.profile) {
          formData.append('profile', this.profile);
        }

        const response = await fetch('http://localhost:5000/api/register', {
          method: 'POST',
          body: formData
        });

        alert(response.data.message);
        this.$router.push('/login');
      } catch (err) {
        this.error = err.response?.data?.error || 'Registration failed';
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to bottom right, #c2e9fb, #a1c4fd);
}

.form-box {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 320px; /* Keeps the form box narrow */
  text-align: center;
}

.title {
  font-size: 24px;
  margin-bottom: 1rem;
  font-weight: bold;
}

form input {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 12px;
  font-size: 14px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #00c6ff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color: #0096cc;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>