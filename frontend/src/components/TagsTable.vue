<template>
  <div class="table-container">
    <table class="table">
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
table {
  width: 100%;
}

.table-container {
  max-height: 450px;
  overflow-y: scroll;
  border: 1px solid #ddd;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

th, td {
  padding: 16px;
}
</style>
