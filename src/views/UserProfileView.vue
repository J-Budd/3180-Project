<template>
  <div class="user-profile-container">
    <div class="user-info">
      <img v-if="user.photo" :src="`/uploads/${user.photo}`" alt="User Photo" />
      <div class="details">
        <h2>{{ user.name }}</h2>
        <p><strong>Description:</strong> {{ mainProfile?.description || 'No description' }}</p>
        <p><strong>Joined:</strong> {{ formatDate(user.date_joined) }}</p>
      </div>
      <div v-if="showCreateButton" class="create-profile-button">
        <button @click="goToCreateProfile" class="createB">+ Create New Profile</button>
      </div>
    </div>

    <div v-if="profiles.length" class="profile-cards">
      <h3>Other Profiles</h3>
      <div class="cards">
        <div v-for="profile in profiles" :key="profile.id" class="card">
          <p><strong>Parish:</strong> {{ profile.parish }}</p>
          <p><strong>Sex:</strong> {{ profile.sex }}</p>
          <p><strong>Race:</strong> {{ profile.race }}</p>
          <router-link :to="`/profiles/${profile.id}`" class="view-more-button">
          View More</router-link>
          <button @click="goToMatchMe(profile.id)">Match Me</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const user = ref({});
const profiles = ref([]);
const mainProfile = ref(null);


const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString();
};

const fetchProfileData = async () => {
  const token = localStorage.getItem('token');
  const userId = localStorage.getItem('user_id');

  const res = await fetch(`/api/users/${userId}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  const data = await res.json();
  user.value = data.user;
  profiles.value = data.profiles || [];

  // optional: pick first profile as main
  mainProfile.value = profiles.value[0] || null;
};

onMounted(() => {
  fetchProfileData();
});

const showCreateButton = computed(() => profiles.value.length < 3);

const goToCreateProfile = () => {
  router.push('/profiles/new');
};

// Redirect to Favourites page with profile id
const goToMatchMe = (profileId) => {
  router.push('/profiles/favourites');
};

</script>

<style scoped>
.user-profile-container {
  max-width: 800px;
  margin: auto;
  padding: 2rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 2rem;
}

.user-info img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ccc;
}

.details {
  flex-grow: 1;
}

.profile-cards {
  margin-top: 2rem;
}

.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.card {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 12px;
  width: 200px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
}

.card button {
  margin-top: 1rem;
  padding: 6px 12px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
.create-profile-button {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.createB {
  background: linear-gradient(to right, #4facfe, #00f2fe);
  color: white;
  padding: 10px 18px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 123, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}

.createB:hover { 
  background: linear-gradient(to right, #00f2fe, #4facfe);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 123, 255, 0.3);
}
</style>
