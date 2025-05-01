<template>
    <div class="container mt-5">
      <h2>Search Profiles</h2>
  
      <form @submit.prevent="search">
        <div class="row">
          <div class="col-md-3 mb-2">
            <input v-model="name" class="form-control" placeholder="Name or bio keyword" />
          </div>
          <div class="col-md-2 mb-2">
            <input v-model="birthYear" type="number" class="form-control" placeholder="Birth Year" />
          </div>
          <div class="col-md-2 mb-2">
            <select v-model="sex" class="form-select">
              <option value="">Sex</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>
          <div class="col-md-2 mb-2">
            <input v-model="race" class="form-control" placeholder="Race" />
          </div>
          <div class="col-md-3 mb-2">
            <button class="btn btn-primary w-100">Search</button>
          </div>
        </div>
      </form>
  
      <div v-if="results.length === 0 && searched" class="mt-3 text-muted">No results found.</div>
  
      <div class="row mt-4" v-if="results.length">
        <div class="col-md-4 mb-3" v-for="profile in results" :key="profile.id">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ profile.biography || 'No bio' }}</h5>
              <p class="card-text">
                <strong>Sex:</strong> {{ profile.sex }}<br />
                <strong>Race:</strong> {{ profile.race }}<br />
                <strong>Birth Year:</strong> {{ profile.birth_year }}<br />
                <strong>Parish:</strong> {{ profile.parish }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import api from '../services/api';
  
  const name = ref('');
  const birthYear = ref('');
  const sex = ref('');
  const race = ref('');
  const results = ref([]);
  const searched = ref(false);
  
  async function search() {
    try {
      const params = {
        name: name.value || undefined,
        birth_year: birthYear.value || undefined,
        sex: sex.value || undefined,
        race: race.value || undefined,
      };
  
      const res = await api.get('/search', { params });
      results.value = res.data;
      searched.value = true;
    } catch (err) {
      console.error('Search failed:', err);
      searched.value = true;
    }
  }
  </script>
  