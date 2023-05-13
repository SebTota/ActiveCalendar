<template>
  <LoadingSpinner />
</template>
<script setup lang="ts">
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import type {Ref} from "vue";
import {ref} from "vue";
import {useMainStore} from "@/stores/state";

const mainStore = useMainStore();
const error: Ref<string> = ref("");


async function handleAuthCheck() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('code')) {
        try {
            await mainStore.authenticateUserWithStrava(urlParams.get('code'));
        } catch (error) {
            await mainStore.redirectToSettings();
        }
    } else {
        await mainStore.redirectToSettings();
    }
}
handleAuthCheck();

</script>