<template>
  <div class="container">
    <h1>Template Builder Instructions</h1>
    <p>Templates allow you to customize your calendar events to have all the data that you need! Use per event
    template tags for creating the title and description template you want to use for each new Strava event,
    and use the summary event tags for creating your daily and weekly summary templates.</p>
    <div class="pb-4">
      <h2>Tags</h2>
      <p>Tags are the core of all event templates and specify what information you want to display from the
        activity.</p>
      <div class="row">
        <div class="tags-column column col-sm-6">
          <h4>Per Event Template Tags</h4>
          <TagsTable class="tag-table" :tags="this.perActivityTemplateTags"/>
        </div>
        <div class="tags-column column col-sm-6">
          <h4>Summary Event Template Tags</h4>
          <TagsTable class="tag-table" :tags="this.summaryActivityTemplateTags"/>
        </div>
      </div>
    </div>
    <div class="pb-4">
      <h2>Activities</h2>
      <p>If you track multiple types of activities and want to separate the information for each activity type
      in your calendar events, use activity types to customize your template even more by separating each activities data.</p>
      <ActivityListDisplay :activities="activityTypes" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Constants from '@/constants/constants'
import TagsTable from '@/components/TagsTable.vue'
import ActivityListDisplay from '@/components/ActivityListDisplay.vue'

export default defineComponent({
  name: 'template-builder-help',
  data () {
    return {
      perActivityTemplateTags: Constants.PER_EVENT_TEMPLATE_TAGS,
      summaryActivityTemplateTags: Constants.SUMMARY_TEMPLATE_TAGS,
      activityTypes: Constants.ACTIVITY_TYPES
    }
  },
  components: {
    TagsTable,
    ActivityListDisplay
  },
  methods: {}
})
</script>

<style>
* {
  box-sizing: border-box;
}

.row {
  margin-left:-5px;
  margin-right:-5px;
}

.column {
  float: left;
  width: 50%;
  padding: 5px;
}

/* Clearfix (clear floats) */
.row::after {
  content: "";
  clear: both;
  display: table;
}

table {
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
}

@media screen and (max-width: 1000px) {
  .column {
    max-width: 100%;
    width: 100%;
    flex: 100%;
  }
}
</style>
