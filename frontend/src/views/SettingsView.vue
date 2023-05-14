<template>
    <template v-if="showLoading">
        <LoadingSpinner/>
    </template>
    <template v-else>
        <div class="flex h-full mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 py-6">
            <!--This is the navigation bar-->
            <div class="w-1/3 h-full border-r-2 border-gray-700">
                <nav class="py-4 px-4" aria-label="Sidebar">
                    <a v-for="item in navigation" :key="item.name" :href="item.href"
                       :class="[currentNavigation === item.href ? 'bg-gray-900 text-gray-300' : 'text-gray-400 hover:bg-gray-700 hover:text-white', 'group flex items-center px-3 py-2 text-sm font-medium rounded-md']"
                       :aria-current="currentNavigation === item.href ? 'page' : undefined">
                        <span class="truncate">{{ item.name }}</span>
                    </a>
                </nav>
            </div>
            <!--This is the content-->
            <div class="w-2/3 h-full" v-if="user && currentNavigation === '#account'">
                <StravaAndCalendarAuth :user="user"/>
            </div>
        </div>
    </template>

</template>

<script setup lang="ts">
import type {IUser} from '@/interfaces/user';

import {useMainStore} from "@/stores/state";
import {Ref, ref} from "vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import StravaAndCalendarAuth from "@/components/StravaAndCalendarAuth.vue";

const store = useMainStore();

const showLoading: Ref<boolean> = ref(true);
const error: Ref<string> = ref('');
const user: Ref<IUser | null> = ref(null);
const currentNavigation: Ref<string> = ref(window.location.hash !== '' ? window.location.hash : '#account');

const navigation = [
    {name: 'Account', href: '#account'},
    {name: 'Activity Template', href: '#activityTemplate'},
    {name: 'Daily Template', href: '#dailyTemplate'},
    {name: 'Weekly Template', href: '#weeklyTemplate'},
]

onhashchange = (event) => {
    currentNavigation.value = window.location.hash;
};

store.getMe().then((userInfo: IUser) => {
    user.value = userInfo;
    if (userInfo.hasStravaAuth && userInfo.hasGoogleCalendarAuth) {
        currentNavigation.value = '#activityTemplate';
    }
    showLoading.value = false;
}).catch((err: Error) => {
    console.log(err);
    error.value = err.message;
    showLoading.value = false;
})
</script>