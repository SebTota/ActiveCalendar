<template>
  <div>
    <h4>{{ title }}</h4>
    <hr>
    <div v-if="summaryEnabled" class="input-group pb-3">
      <div class="w-100 mb-2">
        <div class="mb-4">
          <h5>Title Template</h5>
          <input ref="titleTemplateBuilderInput" id="titleTemplateBuilderInput" type="text" class="form-control"
                 aria-label="calendar event title template" aria-describedby="basic-addon1"
                 v-model="this.titleTemplate">
        </div>
        <div>
          <h5>Calendar Event Template</h5>
          <textarea ref="templateBuilderInput" class="form-control" aria-label="summary text area" rows="7" v-model="this.descriptionTemplate"></textarea>
        </div>
        <a href="https://strava.sebtota.com/help/templateBuilder" target="_blank">Need help making a template?</a>
      </div>
    </div>
    <div>
      <div v-if="!summaryEnabled">
        <button v-if="!toggleTemplateEnabledButtonsLoading" @click="enableSummary()" type="button" class="btn btn-info">Enable</button>
        <button v-else class="btn btn-info" type="button" disabled>
          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          Loading...
        </button>
      </div>
      <div v-else>
        <div v-if="showValidationError()" class="alert alert-danger" role="alert">{{ this.validationErrorMessage }}</div>
        <button v-if="!saveButtonLoading" type="button" class="btn btn-info" @click="saveTemplate()">Save</button>
        <button v-else class="btn btn-info" type="button" disabled>
          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          Loading...
        </button>
        <button v-if="!toggleTemplateEnabledButtonsLoading" type="button" @click="disableSummary()" class="btn btn-warning ml-3">Disable</button>
        <button v-else class="btn btn-warning ml-3" type="button" disabled>
          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          Loading...
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  props: {
    title: String,
    summary_enabled: Boolean,
    title_template: String,
    description_template: String,
    summary_type: String
  },
  data () {
    return {
      readyToSave: false,
      validationErrorMessage: '',
      summaryEnabled: this.summary_enabled,
      titleTemplate: this.title_template,
      descriptionTemplate: this.description_template,
      summaryType: this.summary_type,
      saveButtonLoading: false,
      toggleTemplateEnabledButtonsLoading: false
    }
  },
  methods: {
    enableSummary () {
      this.toggleTemplateEnabledButtonsLoading = true
      const body = {
        summary_type: this.summaryType,
        enabled: 'true'
      }
      axios.post('/api/summary/template/update', body, { withCredentials: true }).then(() => {
        this.summaryEnabled = true
        this.toggleTemplateEnabledButtonsLoading = false
      })
    },
    disableSummary () {
      this.toggleTemplateEnabledButtonsLoading = true
      const body = {
        summary_type: this.summaryType,
        enabled: 'false'
      }
      axios.post('/api/summary/template/update', body, { withCredentials: true }).then(() => {
        this.summaryEnabled = false
        this.toggleTemplateEnabledButtonsLoading = false
      })
    },
    showValidationError () {
      return this.validationErrorMessage.length > 0
    },
    saveTemplate () {
      this.validationErrorMessage = ''
      this.saveButtonLoading = true
      const body = {
        summary_type: this.summaryType,
        enabled: 'true',
        title_template: (this.$refs.titleTemplateBuilderInput as any).value,
        description_template: (this.$refs.templateBuilderInput as any).value
      }

      axios.post('/api/summary/template/update', body, { withCredentials: true }).catch((err) => {
        this.saveButtonLoading = false
        if (err.response.status === 400) {
          const invalidKeys = err.response.data.invalid_keys
          this.validationErrorMessage = 'Invalid keys: ' + invalidKeys.join(', ')
        }
      }).then(() => {
        // Always executed
        this.saveButtonLoading = false
      })
    }
  }
})

</script>

<style scoped>

</style>
