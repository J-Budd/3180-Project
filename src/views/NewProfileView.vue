<template>
  <form @submit.prevent="submitProfile">
    <input v-model="profile.description" placeholder="Description" required />
    <input v-model="profile.parish" placeholder="Parish" required />
    <textarea v-model="profile.biography" placeholder="Biography" required></textarea>

    <select v-model="profile.sex" required>
      <option value="Male">Male</option>
      <option value="Female">Female</option>
    </select>

    <input v-model="profile.race" placeholder="Race" required />
    <input v-model.number="profile.birth_year" type="number" placeholder="Birth Year" required />
    <input v-model.number="profile.height" type="number" step="0.01" placeholder="Height (e.g., 1.75)" required />

    <input v-model="profile.fav_cuisine" placeholder="Favourite Cuisine" required />
    <input v-model="profile.fav_color" placeholder="Favourite Color" required />
    <input v-model="profile.fav_school_subject" placeholder="Favourite Subject" required />

    <label>
      Political:
      <input type="checkbox" v-model="profile.political" />
    </label>

    <input v-model="profile.religion" placeholder="Religion" required />

    <label>
      Family Oriented:
      <input type="checkbox" v-model="profile.family_oriented" />
    </label>

    <button type="submit">Create Profile</button>
    <p v-if="error">{{ error }}</p>
  </form>
</template>

<script>
export default {
  data() {
    return {
      profile: {
        description: '',
        parish: '',
        biography: '',
        sex: '',
        race: '',
        birth_year: null,
        height: null,
        fav_cuisine: '',
        fav_color: '',
        fav_school_subject: '',
        political: false,
        religion: '',
        family_oriented: false
      },
      error: ''
    };
  },
  methods: {
    async submitProfile() {
      try {
        const token = localStorage.getItem('token'); //get the token stored from the login process
        if (!token) {
          this.error = 'No token found. Please log in first.';
          return;
        }

        const res = await fetch('/api/profiles', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}` // using JWT
          },
          body: JSON.stringify(this.profile)
        });

        const data = await res.json();

        if (!res.ok) {
          this.error = data.error || 'Failed to create profile';
        } else {
          alert('Profile created successfully!');
          this.$router.push('/user-page'); // redirect to profile page
        }
      } catch (err) {
        this.error = 'An error occurred while creating the profile';
      }
    }
  }
};
</script>

<style scoped>
form {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: auto;
  font-family: 'Arial', sans-serif;
  transition: all 0.3s ease-in-out;
}

form input, form textarea, form select {
  display: block;
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  transition: border 0.3s ease;
}

form input:focus, form textarea:focus, form select:focus {
  border-color: #00c6ff;
  outline: none;
}

form textarea {
  resize: vertical;
  height: 100px;
}

form button {
  width: 100%;
  padding: 14px;
  background-color: #00c6ff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 16px;
}

form button:hover {
  background-color: #0096cc;
}

form label {
  font-size: 16px;
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

form input[type="checkbox"] {
  margin-right: 10px;
}

form p {
  color: red;
  font-size: 14px;
  margin-top: 1rem;
  text-align: center;
}

form .checkbox-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

form .checkbox-group label {
  font-weight: normal;
}

form select {
  background-color: #f9f9f9;
}

@media (max-width: 768px) {
  form {
    padding: 1.5rem;
    width: 90%;
  }
}
</style>

