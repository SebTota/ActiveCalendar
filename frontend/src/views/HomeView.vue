<template>
<div class="w-100 h-100">
    <div id="intro-container" class="container w-100 h-100">
        <div class="row" style="height: 100%;">
            <div class="col-sm-8 home-page-column home-page-column-left">
              <div>
                <div>
                  <p id="intro-statement">Activity Calendar allows you to stay on top of your training at a quick glance.</p>
                </div>
                <div v-if="retrievedUser && !isLoggedIn()">
                  <button @click="login()">
                    <img src="@/assets/strava/btn_strava_connectwith_orange@2x.png" />
                  </button>
                </div>
              </div>
            </div>
            <div class="col-sm-4 home-page-column home-page-column-right">
                <img class="into-example-calendar-img" src="@/assets/mock_one.png" />
            </div>
        </div>
    </div>
    <div class="navbar fixed-bottom">
      <img class="compatible-with-strava mx-auto" src="@/assets/strava/api_logo_cptblWith_strava_horiz_light.png"/>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { User } from '@/store/user'
import Constants from '@/constants/constants'

export default defineComponent({
  name: 'HomeView',
  data () {
    return {
      retrievedUser: false,
      user: User()
    }
  },
  async created () {
    const user = User()
    await user.getUser()
    this.user = user
    this.retrievedUser = true
  },
  methods: {
    isLoggedIn () {
      return this.user.isAuthenticated
    },
    login () {
      if (this.user.isAuthenticated) {
        console.log('User is already logged in: ' + this.user.user_id)
      } else {
        window.location.href = Constants.API_BASE_PATH + '/api/auth/strava'
      }
    }
  }
})
</script>

<style scoped>

#intro-container {
    padding-top: 70px;
    padding-bottom: 30px;
    height: 100%;
}

#intro-statement {
    font-size: 20pt;
    font-weight: bolder
}

.home-page-column {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

@media (max-width: 900px) {
  .home-page-column-right {
    display: none;
  }
  .home-page-column-left {
    width: 100%;
  }
}

.into-example-calendar-img {
  max-width: 100%;
  max-height: 80%;
}

.compatible-with-strava {
  max-width: 250px;
}
</style>
