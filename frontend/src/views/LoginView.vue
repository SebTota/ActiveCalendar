<template>
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
            <img className="mx-auto h-50 w-auto" src="../assets/ActiveRunWideLogo.png" alt="Active" />
            <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-300">Sign in or create
                your
                account.</h2>
            <p className="text-center text-l font-bold leading-9 tracking-tight text-gray-300">Sign in with your Google
                account below.</p>
        </div>
    </div>

    <div className="text-center">
        <template v-if="showLoading">
            <div class="flex justify-center items-center">
                <div class="flex items-center justify-center">
                    <div
                        class="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-tr from-white to-gray-600 animate-spin">
                        <div class="h-9 w-9 rounded-full bg-gray-700"></div>
                    </div>
                </div>
            </div>
            <h2 className="text-center text-l font-bold leading-9 tracking-tight text-gray-300">Signing In...</h2>
        </template>
        <template v-else>
            <a :href="googleAuthPath">
                <img src="../assets/google_sign_in.png" className="inline" />
            </a>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { googleAuthPath, googleAuthCallback } from '../settings';

let showLoading: any = ref(true);

const params: string = window.location.href.split(window.location.pathname)[1];
if (params.includes("code=")) {
    // window.location.href = `${googleAuthCallback}${params}`
} else {
    showLoading = false;
}

</script>