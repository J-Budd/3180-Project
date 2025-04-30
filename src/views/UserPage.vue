<template>
  <div>
    <AppHeader />
    <div class="sub-navbar">
      <router-link :to="`/users/${userId}`">My Profile</router-link>
      <button @click="logoutUser">Logout</button>
    </div>
    <div class="search-section">
      <input v-model="query" placeholder="Search..." @input="handleSearch" />
      <div class="filter-buttons">
        <button @click="setFilter('name')">Name</button>
        <button @click="setFilter('birth')">Birth</button>
        <button @click="setFilter('sex')">Sex</button>
        <button @click="setFilter('race')">Race</button>
      </div>
    </div>
    <div class="profile-list">
      <div v-for="profile in profiles" :key="profile.id" class="profile-card">
      <img v-if="profile.photo" :src="`/uploads/${profile.photo}`" alt="User Photo" />

        
        <p>{{ profile.name }}</p>
        <p>{{ profile.parish }}</p>

        <!-- View More button -->
        <router-link :to="`/profiles/${profile.id}`" class="view-more-button">
          View More</router-link>
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';



const profiles = ref([]);
const query = ref('');
const filter = ref('name');
const userId = ref(localStorage.getItem('user_id'));  //gets user id from local storage

const logoutUser = () => {
  localStorage.removeItem('token');
  window.location.href = '/login'; // redirect to login
};

const fetchProfiles = async () => {
  const token = localStorage.getItem('token');
  const res = await fetch('/api/profiles?limit=4', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await res.json();
  profiles.value = data;
};

const handleSearch = async () => {
  const token = localStorage.getItem('token');
  const res = await fetch(`/api/profiles/search?${filter.value}=${query.value}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await res.json();
  profiles.value = data;
};

const setFilter = (type) => {
  filter.value = type;
};

onMounted(() => {
  fetchProfiles();
});
</script>

<style scoped>
.search-section {
  margin: 2rem auto;
  text-align: center;
  max-width: 600px;
}

.search-section input {
  width: 80%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 12px;
  margin-bottom: 1rem;
  font-size: 16px;
}

.filter-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.filter-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background-color: #ffa500; /* orange-yellow */
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.filter-buttons button:hover {
  background-color: #ff8c00;
}

.profile-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  padding: 1rem;
}

.profile-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
  width: 160px;
  padding: 1rem;
  text-align: center;
  transition: transform 0.2s ease;
}

.profile-card:hover {
  transform: translateY(-5px);
}

.profile-card img {
  width: 100%;
}

.sub-navbar {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 10px 20px;
  background-color: #ffcc66;
  border-bottom: 1px solid #e0a800;
  font-weight: bold;
}

.sub-navbar a {
  color: #333;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.sub-navbar a:hover {
  background-color: #ffd27f;
}

.sub-navbar button {
  padding: 6px 12px;
  border: none;
  background-color: #ff7e5f;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.sub-navbar button:hover {
  background-color: #eb5e3d;
}
.view-more-button {
  display: inline-block;
  margin-top: 10px;
  padding: 6px 12px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.view-more-button:hover {
  background-color: #45a049;
}

</style>
