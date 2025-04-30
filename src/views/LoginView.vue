<template>
  <div class="login-container">
    <div class="form-box">
      <h2 class="title">Jam-Date</h2>
      <form @submit.prevent="loginUser">
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
        <p class="error" v-if="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async loginUser() {
      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });

        const data = await response.json(); // this is the response body, contains whether they have profile or not

        if (!response.ok) {
          this.error = data.error || 'Login failed';
        } else {
          alert(data.message);
          // Optional: store user ID or token if needed
          localStorage.setItem('user_id', data.user_id); // store user ID
          localStorage.setItem('token', data.token); // storetoken

          if (data.has_profile) {
            this.$router.push('/user-page');
          } else {
            this.$router.push('/profiles/new');
          }
        }
      } catch (err) {
        this.error = 'An error occurred while logging in.';
      }
    }
  }
}
</script>


<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to bottom right, #ffecd2, #fcb69f); /* peach to coral */
}

.form-box {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 320px;
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
  background-color: #ff7e5f;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color: #eb5e3d;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
