<template>
  <div class="profile-detail-container" v-if="profile">
    <AppHeader />
    <div class="profile-detail-card">
      <img v-if="profile.photo" :src="`/uploads/${profile.photo}`" alt="User Photo" />
      <h2>{{ profile.description || 'No description' }}</h2>
      <p><strong>Parish:</strong> {{ profile.parish }}</p>
      <p><strong>Biography:</strong> {{ profile.biography }}</p>
      <p><strong>Sex:</strong> {{ profile.sex }}</p>
      <p><strong>Race:</strong> {{ profile.race }}</p>
      <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
      <p><strong>Height:</strong> {{ profile.height }} m</p>
      <p><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
      <p><strong>Favourite Color:</strong> {{ profile.fav_color }}</p>
      <p><strong>Favourite Subject:</strong> {{ profile.fav_school_subject }}</p>
      <p><strong>Political:</strong> {{ profile.political ? 'Yes' : 'No' }}</p>
      <p><strong>Religion:</strong> {{ profile.religion }}</p>
      <p><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>

      <div class="action-buttons">
        <button @click="emailProfile">Email Profile</button>
        <button @click="markFavorite">Mark as Favourite</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';

const route = useRoute();
const profile = ref(null);

const fetchProfile = async () => {
  const token = localStorage.getItem('token');
  const res = await fetch(`/api/profiles/${route.params.profile_id}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  const data = await res.json();
  profile.value = data;
};

onMounted(() => {
  fetchProfile();
});
</script>

<style scoped>
.profile-detail-container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
}

.profile-detail-card {
  background-color: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.profile-detail-card img {
  max-width: 200px;
  margin-bottom: 1rem;
  border-radius: 12px;
}

.action-buttons {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
}

.action-buttons button {
  display: flex;
  justify-content: center;  
  margin-top: 1.5rem; /* optional spacing from content above */  
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  background-color: #ffa500;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-buttons button:hover {
  background-color: #ff8c00;
}



</style>
