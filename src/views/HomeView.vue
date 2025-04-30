<template>
  <div class="home-container">
    <div class="overlay">
      <h1 class="title">Jam-Date</h1>
      <p class="subtitle">Join, connect, and find your perfect match</p>
      <div class="btn-group">
        <router-link to="/login" class="btn login">Login</router-link>
        <router-link to="/register" class="btn register">Register</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage"
};
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
