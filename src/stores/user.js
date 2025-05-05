import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    userId: localStorage.getItem('user_id') || null,
    token: localStorage.getItem('token') || null,
    hasProfile: false
  }),
  actions: {
    setUser(data) {
      this.userId = data.user_id
      this.token = data.token
      this.hasProfile = data.has_profile

      localStorage.setItem('user_id', data.user_id)
      localStorage.setItem('token', data.token)
    },
    logout() {
      this.userId = null
      this.token = null
      this.hasProfile = false

      localStorage.removeItem('user_id')
      localStorage.removeItem('token')
    }
  }
})

