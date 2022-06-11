<template>
  <div>
    <ul class="list-group">
      <li v-for="activity in activities.slice(0, 5)" v-bind:key="activity" class="list-group-item">{{activity}}</li>
      <template v-if="showAllActivities">
        <li v-for="activity in activities.slice(5, activities.length)" v-bind:key="activity" class="list-group-item">{{activity}}</li>
      </template>
    </ul>
    <button class="mt-2 btn btn-primary" type="button"
            @click="toggleShowAllActivities()">{{this.showAllActivities ? 'Hide': 'Show All'}}</button>
  </div>
</template>

<script>
export default {
  name: 'ActivityListDisplay',
  props: {
    activities: []
  },
  data () {
    return {
      showAllActivities: false
    }
  },
  methods: {
    toggleShowAllActivities () {
      this.showAllActivities = !this.showAllActivities
    }
  }
}
</script>

<style scoped>

</style>
