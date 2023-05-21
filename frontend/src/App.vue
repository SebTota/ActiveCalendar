<template>
    <router-view :key="$route.path">
        <Header/>
    </router-view>
    <div class="remaining_height">
        <RouterView/>
    </div>
</template>

<script setup lang="ts">
import {RouterView} from 'vue-router'
import Header from './components/Header.vue'
</script>

<style scoped>
    .remaining_height {
        height: Calc(100% - 64px - 2px);
    }
</style>
