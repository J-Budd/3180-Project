<template>
  <div class="home-container">
    <div class="overlay">
      <div class="hero-content text-center text-white">
        <h1 class="display-4 fw-bold mb-2">Jam-Date</h1>
        <p class="lead mb-4">Young, vibrant dating with purpose 💘</p>

        <div class="card form-card p-4 mx-auto">
          <h4 class="mb-3">Quick Register</h4>
          <form @submit.prevent="register">
            <input v-model="username" class="form-control mb-2" placeholder="Username" />
            <input v-model="email" type="email" class="form-control mb-2" placeholder="Email" />
            <input v-model="password" type="password" class="form-control mb-3" placeholder="Password" />
            <button class="btn btn-danger w-100">Register</button>
          </form>
          <RouterLink to="/login" class="btn btn-link mt-2">Already have an account? Login</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../services/api';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const name = ref('');
const file = ref(null);  // for profile photo

async function register() {
  const formData = new FormData();
  formData.append('username', username.value);
  formData.append('email', email.value);
  formData.append('password', password.value);
  formData.append('name', name.value);
  if (file.value) {
    formData.append('profile', file.value);
  }

  try {
    await api.post('/register', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    alert('Registered successfully!');
    router.push('/login');
  } catch (error) {
    console.error(error);
    alert('Registration failed: ' + (error.response?.data?.error || 'Unknown error'));
  }
}
</script>


<style scoped>
.home-container {
  background-image: url("/images/homepage1.jpg");
  background-size: cover;
  background-position: center;
  height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.overlay {
  background-color: rgba(0, 0, 0, 0.5); /* dark overlay */
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  color: white;
  max-width: 90%;
}

.title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.btn-group {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn {
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: 0.3s;
}

.login {
  background-color: white;
  color: #333;
}

.register {
  background-color: #ff5c5c;
  color: white;
}

.btn:hover {
  opacity: 0.85;
}
</style>
