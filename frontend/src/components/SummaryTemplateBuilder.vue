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
                 v-model="this.summaryTitleTemplate">
        </div>
        <div>
          <h5>Calendar Event Template</h5>
          <textarea ref="templateBuilderInput" class="form-control" aria-label="summary text area" rows="7" v-model="this.summaryTemplate"></textarea>
        </div>
      </div>
    </div>
    <div>
      <button v-if="!summaryEnabled" @click="enableSummary()" type="button" class="btn btn-info">Enable</button>
      <div v-else>
        <div v-if="showValidationError()" class="alert alert-danger" role="alert">{{ this.validationErrorMessage }}</div>
        <button type="button" class="btn btn-info" @click="saveTemplate()">Save</button>
        <button type="button" @click="disableSummary()" class="btn btn-warning ml-3">Disable</button>
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
    summary_title_template: String,
    summary_template: String,
    summary_type: String
  },
  data () {
    return {
      readyToSave: false,
      validationErrorMessage: '',
      summaryEnabled: this.summary_enabled,
      summaryTitleTemplate: this.summary_title_template,
      summaryTemplate: this.summary_template,
      summaryType: this.summary_type
    }
  },
  methods: {
    enableSummary () {
      axios.post(`/api/summary/template/update?summary_type=${this.summaryType}&enabled=true`, {}, { withCredentials: true }).then(() => {
        this.summaryEnabled = true
      })
    },
    disableSummary () {
      const body = {
        enabled: 'false'
      }
      axios.post(`/api/summary/template/update?summary_type=${this.summaryType}&enabled=false`, {}, { withCredentials: true }).then(() => {
        this.summaryEnabled = false
      })
    },
    showValidationError () {
      return this.validationErrorMessage.length > 0
    },
    saveTemplate () {
      this.validationErrorMessage = ''
      const titleTemplateVal = (this.$refs.titleTemplateBuilderInput as any).value
      const summaryTemplateVal = (this.$refs.templateBuilderInput as any).value
      const url = `/api/summary/template/update?summary_type=${this.summaryType}&enabled=true&title_template=${titleTemplateVal}&summary_template=${summaryTemplateVal}`
      axios.post(url, {}, { withCredentials: true }).catch((err) => {
        if (err.response.status === 400) {
          const invalidKeys = err.response.data.invalid_keys
          this.validationErrorMessage = 'Invalid keys: ' + invalidKeys.join(', ')
        }
      })
    }
  }
})

</script>

<style scoped>

</style>
