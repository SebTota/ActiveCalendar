<template>
    <div class="pb-5 border-b border-gray-200">
        <h3 class="text-lg font-semibold leading-6 text-gray-300">{{ title }}</h3>
        <p class="mt-2 max-w-4xl text-sm text-gray-300">Update your calendar template below.</p>
    </div>
    <div class="pt-5">
        <h3 class="text-md leading-6 font-medium text-gray-300 pb-2">Title</h3>
        <input type="text" name="username" id="username" autocomplete="username"
               class="block w-full py-2 resize-none bg-gray-800 text-gray-200 focus:ring-0 border border-gray-300 rounded-md text-sm"/>

        <h3 class="text-md leading-6 font-medium text-gray-300 pt-4 pb-2">Calendar Event</h3>
        <div class="min-w-0 flex-1 relative">
            <div class="border border-gray-300 rounded-lg shadow-sm overflow-hidden">
                <label for="calendarEventTemplate" class="sr-only"></label>
                <textarea rows="12" name="calendarEventTemplate" id="calendarEventTemplate"
                          class="block w-full py-3 border-0 text-gray-200 bg-gray-800 focus:ring-0 text-sm"/>
            </div>
        </div>
    </div>
    <div class="mt-6 flex items-center justify-end gap-x-6">
      <button class="rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-500">Enable</button>
      <button class="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500">Disable</button>
      <button class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500">Validate and Save</button>
    </div>
</template>

<script setup lang="ts">

import {computed} from "vue";
import {CalendarTemplateType} from "@/enums/CalendarTemplateType";

const props = defineProps<{
    templateType: CalendarTemplateType
}>()

const title = computed(() => {
    switch (props.templateType) {
        case CalendarTemplateType.ACTIVITY_SUMMARY:
            return 'Activity Template'
        case CalendarTemplateType.DAILY_SUMMARY:
            return 'Daily Summary Template'
        case CalendarTemplateType.WEEKLY_SUMMARY:
            return 'Weekly Summary Template'
        default:
            return 'Calendar Template'
    }
})

</script>