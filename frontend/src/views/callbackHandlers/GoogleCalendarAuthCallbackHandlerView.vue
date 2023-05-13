<template>
    <LoadingSpinner v-if="showLoading" />
</template>

<script setup lang="ts">

import LoadingSpinner from "@/components/LoadingSpinner.vue";
import {Ref, ref} from "vue";
import {useMainStore} from "@/stores/state";

const mainStore = useMainStore();
const showLoading: Ref<boolean> = ref(true);

async function handleAuthCheck() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('code') && urlParams.has('state')) {
        try {
            await mainStore.authenticateUserWithGoogleCalendar(urlParams.get('state'), urlParams.get('code'));
        } catch (error) {
            await mainStore.redirectToSettings();
        }
    } else {
        await mainStore.redirectToSettings();
    }
}
handleAuthCheck();

</script>