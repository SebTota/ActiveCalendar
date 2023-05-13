<template>
    <div class="flex flex-1 flex-col justify-center px-6 py-4 lg:px-8">
        <div class="pb-5 border-b border-gray-200">
            <h3 class="text-lg leading-6 font-medium text-gray-300">Job Postings</h3>
            <p class="mt-2 max-w-4xl text-sm text-gray-300">Sign in with your Strava and Google calendar accounts below to
            start syncing your activities.</p>
        </div>
        <div v-if="user && !user.hasGoogleCalendarAuth" class="text-center mt-6">
            <a :href="googleCalendarAuthPath">
                <img src="../assets/google_sign_in.png" class="inline" alt="Google sign in button"/>
            </a>
        </div>
        <div v-if="user && !user.hasStravaAuth" class="text-center mt-6">
            <a :href="stravaAuthPath">
                <img src="../assets/btn_strava_connectwith_light.png" class="inline" alt="Strava sign in button"/>
            </a>
        </div>
    </div>
</template>

<script setup lang="ts">
import type {IUser} from '@/interfaces/user';

import {useMainStore} from "@/stores/state";
import {googleCalendarAuthPath, stravaAuthPath} from "@/settings";

const mainStore = useMainStore();

defineProps<{
    user: IUser
}>()

</script>