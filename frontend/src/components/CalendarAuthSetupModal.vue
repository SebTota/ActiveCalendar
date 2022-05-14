<template>
  <div class="modal fade" id="calendarAuthSetupModal" tabindex="-1" role="dialog" aria-labelledby="calendarAuthSetupModalTitle" aria-hidden="true" data-backdrop="static" data-keyboard="false">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="calendarAuthSetupModalTitle">Connect a Calendar</h5>
        </div>
        <div class="modal-body">
          To finish setting up your account, please connect a Google Calendar.
        </div>
        <div class="modal-footer">
          <button @click="loginGoogleCalendar()">
            <img src="@/assets/google/btn_google_signin_dark_normal_web@2x.png" />
          </button>
        </div>
      </div>
    </div>
  </div>
  <div id="script-div"></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'CalendarAuthSetupModal',
  props: {
    msg: String
  },
  mounted () {
    this.showModal()
  },
  methods: {
    loginGoogleCalendar () {
      window.location.href = 'http://localhost:5500' + '/auth/googleCalendar'
    },
    showModal () {
      const node = document.createElement('script')
      node.innerHTML = '$("#calendarAuthSetupModal").modal("show")'
      document.getElementById('script-div')!.appendChild(node)
    }
  }
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.modal-footer {
  display: flex;
  justify-content: center;
}
</style>
