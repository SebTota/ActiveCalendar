<template>
    <div class="h-full px-2 sm:px-6">

        <div class="container mx-auto flex px-2 py-24 md:flex-row flex-col items-center max-w-7xl text-gray-300">
            <div class="items-center text-center">
                <h1 class="title-font sm:text-4xl text-3xl mb-4 font-medium text-left">Active Calendar</h1>
                <p class="mb-8 leading-relaxed">Track all your activities, right in your Google Calendar. Get per activity, daily, and weekly
                    activity summaries to track your total mileage.</p>
                <div class="flex">
                    <button @click="navigateGetStarted" class="ml-4 inline-flex text-gray-700 bg-gray-100 border-0 py-2 px-6 focus:outline-none hover:bg-gray-200 rounded text-lg">
                        Get Started
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import {useMainStore} from "@/stores/state";

const mainStore = useMainStore();

function navigateGetStarted() {
    if (mainStore.isLoggedIn) {
        mainStore.redirectToSettings();
    } else {
        mainStore.redirectToLogin();
    }
}

</script>