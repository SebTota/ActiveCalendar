import {
  defineStore
} from 'pinia'
import axios from 'axios'

export const User = defineStore('User', {
  state: () => ({
    isAuthenticated: false,
    calendar_authenticated: false,
    user_id: null,
    first_name: '',
    last_name: ''
  }),
  getters: {
  },
  actions: {
    async getUser () {
      try {
        const res = await axios.get('/api/user/me', { withCredentials: true })
        this.isAuthenticated = true
        this.calendar_authenticated = (res.data.calendar_authenticated)
        this.user_id = res.data.user_id
        this.first_name = res.data.first_name
        this.last_name = res.data.last_name
      } catch (err) {
        this.isAuthenticated = false
      }
    },
    setAuthenticated (isAuthenticated: boolean) {
      this.isAuthenticated = isAuthenticated
    },
    getName () {
      return this.first_name + ' ' + this.last_name
    },
    isAuthenticatedCalendar () {
      return this.calendar_authenticated
    },
    userIsAuthenticated () {
      return this.isAuthenticated
    }
  }
})
