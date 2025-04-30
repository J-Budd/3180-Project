<template>
  <div class="favourites-view-container">
    <h2>Matched Profiles</h2>

    <div v-if="matchedProfiles.length" class="matched-cards">
      <div v-for="match in matchedProfiles" :key="match.id" class="match-card">
        <p><strong>Name:</strong> {{ match.name }}</p>
        <p><strong>Parish:</strong> {{ match.parish }}</p>
        <p><strong>Age:</strong> {{ getAge(match.birth_year) }} years old</p>
        <p><strong>Height:</strong> {{ match.height }} m</p>
        <p><strong>Fav Cuisine:</strong> {{ match.fav_cuisine }}</p>
        
      </div>
    </div>

    <div v-else>
      <p>No matched profiles found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const matchedProfiles = ref([]);

// Function to calculate age from birth year
const getAge = (birthYear) => {
  const currentYear = new Date().getFullYear();
  return currentYear - birthYear;
};

// Fetch matched profiles based on selected profile
const fetchMatches = async () => {
  const token = localStorage.getItem('token');
  const profileId = route.query.profile_id;

  const res = await fetch(`/api/profiles/matches/${profileId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await res.json();
  matchedProfiles.value = data; // Store matched profiles
};

onMounted(() => {
  fetchMatches();
});
</script>

<style scoped>
.favourites-view-container {
  padding: 2rem;
}

.matched-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.match-card {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 12px;
  width: 200px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
}
</style>
