<template>
  <div>
    <table class="table table-sm">
      <div style="height: 400px; overflow: scroll">
        <thead>
        <tr>
          <th scope="col">Tag Name</th>
          <th scope="col">Description</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(k, v) in tags" v-bind:key="(k, v)">
          <th scope="row">{{ v }}</th>
          <td>{{ k }}</td>
        </tr>
        </tbody>
      </div>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    tags: {}
  },
  data () {
    return {}
  },
  methods: {}
})

</script>

<style scoped>

</style>
