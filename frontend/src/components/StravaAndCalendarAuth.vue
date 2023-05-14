<template>
    <div class="pb-5 border-b border-gray-200">
        <h3 class="text-lg leading-6 font-semibold text-gray-300">Account</h3>
        <p class="mt-2 max-w-4xl text-sm text-gray-300">Sign in with your Strava and Google calendar accounts below
            to
            start syncing your activities.</p>
    </div>
    <template v-if="user.hasGoogleCalendarAuth && user.hasStravaAuth">
        <p class="mt-2 max-w-4xl text-sm text-gray-300">You're all set here!</p>
    </template>
    <template v-else>
        <div v-if="!user.hasGoogleCalendarAuth" class="text-center mt-6">
            <a :href="googleCalendarAuthPath">
                <img src="../assets/google_sign_in.png" class="inline" alt="Google sign in button"/>
            </a>
        </div>
        <div v-if="!user.hasStravaAuth" class="text-center mt-6">
            <a :href="stravaAuthPath">
                <img src="../assets/btn_strava_connectwith_light.png" class="inline" alt="Strava sign in button"/>
            </a>
        </div>
    </template>
</template>

<script setup lang="ts">
import type {IUser} from '@/interfaces/user';
import {googleCalendarAuthPath, stravaAuthPath} from "@/settings";

const props = defineProps<{
    user: IUser
}>()
</script>