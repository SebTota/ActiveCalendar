<template>
  <div class="card">
    <div class="row">
      <div class="column card-body">
        <h5>Template</h5>
        <p style="white-space: pre-line" class="card-text">
          {{this.template}}
        </p>
      </div>
      <div class="column card-body">
        <h5>Result</h5>
        <p style="white-space: pre-line">
          {{this.result}}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExampleTemplateCard',
  props: {
    template: String,
    result: String
  }
}
</script>

<style scoped>

</style>
