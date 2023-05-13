<template>
    <template v-if="showLoading">
        <LoadingSpinner/>
    </template>
    <template v-else :key="currentNavigation">
        <div class="flex h-full mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 py-6">
            <div class="w-1/3 h-full border-r-2 border-gray-700">
                <nav class="py-4 px-4" aria-label="Sidebar">
                    <a v-for="item in navigation" :key="item.name" :href="item.href"
                       :class="[item.current ? 'bg-gray-900 text-gray-300' : 'text-gray-400 hover:bg-gray-700 hover:text-white', 'group flex items-center px-3 py-2 text-sm font-medium rounded-md']"
                       :aria-current="item.current ? 'page' : undefined">
                        <span class="truncate">{{ item.name }}</span>
                    </a>
                </nav>
            </div>
        </div>
    </template>


  <!--    <template v-else-if="user && (!user.hasGoogleCalendarAuth || !user.hasStravaAuth)">-->
  <!--        <div class="flex flex-1 flex-col justify-center px-6 py-12 lg:px-8">-->
  <!--            <div class="md:mx-auto sm:w-full sm:max-w-3xl">-->
  <!--                <p class="text-center text-base text-gray-300">-->
  <!--                    Sign in to your Strava and Google Calendar account below to start creating your calendar templates.-->
  <!--                </p>-->
  <!--            </div>-->
  <!--            <div v-if="user && user.hasGoogleCalendarAuth" class="text-center mt-6">-->
  <!--                <a :href="googleCalendarAuthPath">-->
  <!--                    <img src="../assets/google_sign_in.png" class="inline" alt="Google sign in button"/>-->
  <!--                </a>-->
  <!--            </div>-->
  <!--            <div v-if="user && !user.hasStravaAuth" class="text-center mt-6">-->
  <!--                <a :href="stravaAuthPath">-->
  <!--                    <img src="../assets/btn_strava_connectwith_light.png" class="inline" alt="Strava sign in button"/>-->
  <!--                </a>-->
  <!--            </div>-->
  <!--        </div>-->
  <!--    </template>-->
</template>

<script setup lang="ts">
import type {IUser} from '@/interfaces/user';

import {useMainStore} from "@/stores/state";
import {Ref, ref} from "vue";
import {googleCalendarAuthPath, stravaAuthPath} from "@/settings";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const store = useMainStore();

const showLoading: Ref<boolean> = ref(true);
const error: Ref<string> = ref('');
const user: Ref<IUser | null> = ref(null);
const currentNavigation: Ref<string> = ref(window.location.hash || '#account');

const navigation = [
    {name: 'Account', href: '#account', current: currentNavigation.value === '#account'},
    {name: 'Activity Template', href: '#activityTemplate', current: currentNavigation.value === '#activityTemplate'},
    {name: 'Daily Template', href: '#dailyTemplate', current: currentNavigation.value === '#dailyTemplate'},
    {name: 'Weekly Template', href: '#weeklyTemplate', current: currentNavigation.value === '#weeklyTemplate'},
]

store.getMe().then((userInfo: IUser) => {
    user.value = userInfo;
    showLoading.value = false;
    console.log(user.value);
}).catch((err: Error) => {
    console.log(err);
    error.value = err.message;
    showLoading.value = false;
})
</script>