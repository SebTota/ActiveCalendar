<template>
    <template v-if="showLoading">
        <LoadingSpinner/>
    </template>
    <template v-else>
        <div class="flex flex-col sm:flex-row h-full mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 py-6">
            <!--This is the navigation bar on desktop-->
            <div class="w-1/3 h-full border-r-2 border-gray-700 hidden sm:inline">
                <nav class="py-4 px-4" aria-label="Sidebar">
                    <a v-for="item in navigation" :key="item.name" :href="item.href"
                       :class="[currentNavigation === item.href ? 'text-white underline' : 'text-gray-400 hover:bg-gray-700 hover:text-white', 'group flex items-center px-3 py-2 text-sm font-medium rounded-md']"
                       :aria-current="currentNavigation === item.href ? 'page' : undefined">
                        <span class="truncate">{{ item.name }}</span>
                    </a>
                </nav>
            </div>

            <!--This is the navigation bar on mobile-->
            <div class="w-full flex-1 flex-col border-b-2 border-gray-700 inline sm:hidden">
                <nav class="py-2 px-4 overflow-auto whitespace-nowrap" aria-label="Sidebar">
                    <a v-for="item in navigation" :key="item.name" :href="item.href"
                       :class="[currentNavigation === item.href ? 'text-white underline' : 'text-gray-400 hover:bg-gray-700 hover:text-white', 'group inline-block px-3 py-2 text-sm font-medium rounded-md']"
                       :aria-current="currentNavigation === item.href ? 'page' : undefined">
                        <span class="truncate">{{ item.name }}</span>
                    </a>
                </nav>
            </div>

            <!--This is the content-->
            <div class="w-full h-full">
                <div class="flex flex-1 flex-col justify-center px-6 py-4 lg:px-8">
                    <StravaAndCalendarAuth :user="user" v-if="user && currentNavigation === '#account'"/>
                    <TemplateBuilder v-if="user && currentNavigation === '#activityTemplate'"
                                     :template-type="CalendarTemplateType.ACTIVITY_SUMMARY"/>
                    <TemplateBuilder v-if="user && currentNavigation === '#dailyTemplate'"
                                     :template-type="CalendarTemplateType.DAILY_SUMMARY"/>
                    <TemplateBuilder v-if="user && currentNavigation === '#weeklyTemplate'"
                                     :template-type="CalendarTemplateType.WEEKLY_SUMMARY"/>
                </div>
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
import TemplateBuilder from "@/components/TemplateBuilder.vue";
import {CalendarTemplateType} from "@/enums/CalendarTemplateType";
import {Listbox, ListboxButton, ListboxOption, ListboxOptions} from "@headlessui/vue";

const store = useMainStore();

const showLoading: Ref<boolean> = ref(true);
const error: Ref<string> = ref('');
const user: Ref<IUser | null> = ref(null);
const currentNavigation: Ref<string> = ref(window.location.hash !== '' ? window.location.hash : '#account');

const navigation = [
    {name: 'Account', href: '#account'}
]

const templateNavigation = [
    {name: 'Activity Template', href: '#activityTemplate'},
    {name: 'Daily Template', href: '#dailyTemplate'},
    {name: 'Weekly Template', href: '#weeklyTemplate'}
]

function showTemplateNavFunc() {
    navigation.push(...templateNavigation);
}

function setNav(navHash: string) {
    currentNavigation.value = navHash;
    window.location.hash = navHash;
}

onhashchange = (event) => {
    if (user.value && user.value?.hasStravaAuth && user.value?.hasGoogleCalendarAuth) {
        currentNavigation.value = window.location.hash;
    } else {
        setNav('#account');
    }
};

store.getMe().then((userInfo: IUser) => {
    user.value = userInfo;
    if (userInfo.hasStravaAuth && userInfo.hasGoogleCalendarAuth) {
        showTemplateNavFunc();
        if (window.location.hash === '') {
            setNav('#activityTemplate');
        }
    } else {
        setNav('#account');
    }
    showLoading.value = false;
}).catch((err: Error) => {
    error.value = err.message;
    showLoading.value = false;
})
</script>