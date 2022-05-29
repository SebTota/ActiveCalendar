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
      summaryType: this.summary_type
    }
  },
  methods: {
    enableSummary () {
      const body = {
        summary_type: this.summaryType,
        enabled: 'true'
      }
      axios.post('/api/summary/template/update', body, { withCredentials: true }).then(() => {
        this.summaryEnabled = false
      })
    },
    disableSummary () {
      const body = {
        summary_type: this.summaryType,
        enabled: 'false'
      }
      axios.post('/api/summary/template/update', body, { withCredentials: true }).then(() => {
        this.summaryEnabled = false
      })
    },
    showValidationError () {
      return this.validationErrorMessage.length > 0
    },
    saveTemplate () {
      this.validationErrorMessage = ''
      const body = {
        summary_type: this.summaryType,
        enabled: 'true',
        title_template: (this.$refs.titleTemplateBuilderInput as any).value,
        description_template: (this.$refs.templateBuilderInput as any).value
      }
      console.log(body)
      const url = '/api/summary/template/update'
      axios.post(url, body, { withCredentials: true }).catch((err) => {
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
