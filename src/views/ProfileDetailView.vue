<template>
  <div class="profile-detail-container" v-if="profile">
    <AppHeader />

    <div class="profile-card">
      <div class="left-column">
        <img
          v-if="profile.photo"
          :src="`/uploads/${profile.photo}`"
          alt="Profile Photo"
          class="profile-photo"
        />
        <div class="basic-info">
          <h2>{{ profile.description || 'No description' }}</h2>
          <p><strong>Parish:</strong> {{ profile.parish || 'N/A' }}</p>
          <p><strong>Sex:</strong> {{ profile.sex || 'N/A' }}</p>
          <p><strong>Race:</strong> {{ profile.race || 'N/A' }}</p>
          <p><strong>Birth Year:</strong> {{ profile.birth_year || 'N/A' }}</p>
        </div>
      </div>

      <div class="right-column">
        <div class="bio-section">
          <h4>Biography</h4>
          <p>{{ profile.biography || 'No biography available.' }}</p>
        </div>

        <div class="details-grid">
          <div>
            <strong>Height:</strong>
            <p>{{ profile.height ? profile.height + ' m' : 'N/A' }}</p>
          </div>
          <div>
            <strong>Favourite Cuisine:</strong>
            <p>{{ profile.fav_cuisine || 'N/A' }}</p>
          </div>
          <div>
            <strong>Favourite Color:</strong>
            <p>{{ profile.fav_color || 'N/A' }}</p>
          </div>
          <div>
            <strong>Favourite Subject:</strong>
            <p>{{ profile.fav_school_subject || 'N/A' }}</p>
          </div>
          <div>
            <strong>Religion:</strong>
            <p>{{ profile.religion || 'N/A' }}</p>
          </div>
          <div>
            <strong>Political:</strong>
            <p>{{ profile.political ? 'Yes' : 'No' }}</p>
          </div>
          <div>
            <strong>Family Oriented:</strong>
            <p>{{ profile.family_oriented ? 'Yes' : 'No' }}</p>
          </div>
        </div>

        <div class="action-buttons">
          <button @click="emailProfile">Send Message</button>
          <button @click="markFavorite">Add to Favourites</button>
        </div>
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
  try {
    const res = await fetch(`/api/profiles/${route.params.profile_id}`);
    if (!res.ok) throw new Error('Failed to load profile');
    profile.value = await res.json();
  } catch (err) {
    alert(err.message);
  }
};

const emailProfile = () => {
  alert(`Pretend to email user ID: ${profile.value.user_id}`);
};

const markFavorite = async () => {
  try {
    await fetch('/api/favourites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ fav_user_id: profile.value.user_id })
    });
    alert('Added to favourites!');
  } catch (err) {
    alert('Failed to favourite profile.');
  }
};

onMounted(fetchProfile);
</script>


<style scoped>
.profile-detail-container {
  padding: 2rem;
  background-color: #f2f2f2;
  min-height: 100vh;
}

.profile-card {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  max-width: 1000px;
  margin: auto;
}

.left-column {
  flex: 1;
  min-width: 250px;
  text-align: center;
}

.profile-photo {
  max-width: 100%;
  border-radius: 16px;
  object-fit: cover;
  height: 300px;
}

.basic-info {
  margin-top: 1rem;
  font-size: 0.95rem;
}

.right-column {
  flex: 2;
  min-width: 300px;
}

.bio-section {
  margin-bottom: 1rem;
}

.bio-section h4 {
  margin-bottom: 0.5rem;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
  font-size: 0.95rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.action-buttons button {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  background-color: #ff5c5c;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-buttons button:hover {
  background-color: #ff2c2c;
}
</style>
