<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="/">
      <img src="@/assets/logo_black.png" height="40" alt="">
    </a>
    <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse"
            data-target="#navbarNavDropdown" aria-controls="navbarNavAltMarkup" aria-expanded="false"
            aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a v-if="this.retrievedUser && this.user.userIsAuthenticated()" class="nav-link" href="/profile">{{ this.user.getName() }} - Profile</a>
        </li>
      </ul>
    </div>
  </nav>
  <div>
    <CalendarAuthSetupModal
      v-if="this.retrievedUser && this.user.userIsAuthenticated() && !this.user.isAuthenticatedCalendar()"/>
  </div>
</template>

<script lang="ts">

import { User } from '@/store/user'
import { defineComponent } from 'vue'
import CalendarAuthSetupModal from '@/components/CalendarAuthSetupModal.vue'

export default defineComponent({
  data () {
    return {
      retrievedUser: false,
      user: User()
    }
  },
  components: {
    CalendarAuthSetupModal
  },
  async created () {
    const user = User()
    await user.getUser()
    this.user = user
    this.retrievedUser = true
  },
  methods: {}
})

</script>
