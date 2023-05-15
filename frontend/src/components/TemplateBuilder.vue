<template>
    <template v-if="isLoading">
        <LoadingSpinner/>
    </template>
    <template v-else-if="calendarTemplate">
        <div class="pb-5 border-b border-gray-200">
            <h3 class="text-lg font-bold leading-6 text-gray-300">{{ title }}</h3>
            <p class="mt-2 max-w-4xl text-sm text-gray-300">Update your calendar template below.</p>
        </div>
        <div class="pt-5">
            <h3 class="text-md leading-6 font-semibold text-gray-300 pb-2">Title</h3>
            <input type="text" name="calendarTemplateTitle" id="calendarTemplateTitle"
                   :value="calendarTemplate.title_template"
                   class="block w-full py-2 resize-none bg-gray-800 text-gray-200 focus:ring-0 border border-gray-300 rounded-md text-sm font-medium"/>
            <h3 class="text-md leading-6 font-medium text-gray-300 pt-4 pb-2">Calendar Event</h3>
            <div class="min-w-0 flex-1 relative">
                <div class="border border-gray-300 rounded-lg shadow-sm overflow-hidden">
                    <label for="calendarEventTemplate" class="sr-only"></label>
                    <textarea rows="10" name="calendarEventTemplate" id="calendarEventTemplate"
                              :value="calendarTemplate.body_template"
                              class="block w-full py-3 border-0 text-gray-200 bg-gray-800 focus:ring-0 text-sm font-medium"/>
                </div>
            </div>
        </div>
        <div v-if="errorMessage" class="mt-3 p-3 rounded-lg shadow-sm border-4 border-red-600">
            <p class="text-md font-semibold text-red-600">{{ errorMessage }}</p>
        </div>
        <div class="mt-6 flex items-center justify-end gap-x-6">
            <button @click="loadTemplates"
                    class="rounded-md bg-yellow-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-yellow-500">
                Reset Changes
            </button>
            <template v-if="calendarTemplate.status === CalendarTemplateStatus.ACTIVE">
                <button @click="disableTemplate"
                        class="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500">
                    Disable
                </button>
                <button @click="updateTemplate"
                        class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500">
                    Validate and Save
                </button>
            </template>
            <template v-else>
                <button @click="enableTemplate"
                        class="rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-500">
                    Enable
                </button>
            </template>
        </div>
    </template>
</template>

<script setup lang="ts">

import {computed, Ref, ref} from "vue";
import {CalendarTemplateType} from "@/enums/CalendarTemplateType";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import {useMainStore} from "@/stores/state";
import type {ICalendarTemplate} from "@/interfaces/calendarTemplate";
import {CalendarTemplateStatus} from "@/enums/CalendarTemplateStatus";

const isLoading: Ref<boolean> = ref(true);
const errorMessage: Ref<string | null> = ref(null);
const calendarTemplate: Ref<ICalendarTemplate | null> = ref(null);

const store = useMainStore();

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

function loadTemplates() {
    isLoading.value = true;
    errorMessage.value = null;
    store.getCalendarTemplate(props.templateType).then((calendarTemplateResponse: ICalendarTemplate) => {
        calendarTemplate.value = calendarTemplateResponse;
        isLoading.value = false;
    }).catch((error: Error) => {
        errorMessage.value = error.message;
        isLoading.value = false;
    });
}

function enableTemplate() {
    calendarTemplate.value!.status = CalendarTemplateStatus.ACTIVE;
    _updateTemplate();
}

function disableTemplate() {
    calendarTemplate.value!.status = CalendarTemplateStatus.DISABLED;
    _updateTemplate();
}

function updateTemplate() {
    calendarTemplate.value!.title_template = document.getElementById('calendarTemplateTitle')!.value;
    calendarTemplate.value!.body_template = document.getElementById('calendarEventTemplate')!.value;
    _updateTemplate();
}

function _updateTemplate() {
    if (!calendarTemplate.value) return;
    isLoading.value = true;
    errorMessage.value = null;

    store.updateCalendarTemplate(calendarTemplate.value!.id, calendarTemplate.value!).then((calendarTemplateResponse: ICalendarTemplate) => {
        calendarTemplate.value = calendarTemplateResponse;
        isLoading.value = false;
    }).catch((error: Error) => {
        errorMessage.value = error.message;
        isLoading.value = false;
    });
}

loadTemplates();

</script>