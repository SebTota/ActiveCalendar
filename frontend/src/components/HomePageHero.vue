<template>
  <div class="hero h-full">
    <div class="hero-content h-full flex-col lg:flex-row-reverse">
      <div>
        <img src="/src/assets/mock_one.png" alt="Phone mock with calendar view" class="max-w-100 sm:max-w-sm rounded-lg shadow-2xl" />
      </div>
      <div>
        <h1 class="text-5xl font-bold">Active Calendar</h1>
        <p class="py-6">Track all your activities, right in your Google Calendar. Get per activity, daily, and weekly
          activity summaries to track your total mileage.
        </p>
        <button class="btn btn-primary" @click="navigateGetStarted">Get Started</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {useMainStore} from "@/stores/state";

const mainStore = useMainStore();

function navigateGetStarted() {
    if(mainStore.isLoggedIn) {
        mainStore.redirectToSettings();
    } else {
        mainStore.redirectToLogin();
    }
}

</script>