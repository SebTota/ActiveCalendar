<template>
    <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-md">
            <img class="mx-auto h-50 w-auto" src="../assets/ActiveRunWideLogo.png" alt="Active" />
            <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-300">Sign in or create
                your
                account.</h2>
            <p class="text-center text-l font-bold leading-9 tracking-tight text-gray-300">Sign in with your Google
                account below.</p>
        </div>
    </div>

    <div class="text-center">
        <template v-if="showLoading">
            <div class="flex justify-center items-center">
                <div class="flex items-center justify-center">
                    <div
                        class="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-tr from-white to-gray-600 animate-spin">
                        <div class="h-9 w-9 rounded-full bg-gray-700"></div>
                    </div>
                </div>
            </div>
            <h2 class="text-center text-l font-bold leading-9 tracking-tight text-gray-300">Signing In...</h2>
        </template>
        <template v-else>
            <a :href="googleAuthPath">
                <img src="../assets/google_sign_in.png" class="inline" alt="Google Sign In Button" />
            </a>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, type Ref } from "vue";
import { googleAuthPath } from '../settings';
import { useMainStore } from "@/stores/state";

const mainStore = useMainStore();

let showLoading: Ref<boolean> = ref(true);
let loginError: Ref<string> = ref("");

async function handleAuthCheck() {
    const params: string = window.location.href.split(window.location.pathname)[1];
    console.log(params)
    if (params.includes("state=")) {
        try {
            await mainStore.authenticateUserWithGoogle(params);
        } catch (error) {
            loginError.value = "Failed to authenticate with Google.";
        }

    } else {
        showLoading.value = false;
    }
}
handleAuthCheck();

</script>