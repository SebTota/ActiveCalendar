import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import SettingsView from '../views/SettingsView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView
        },
        {
            path: '/settings',
            name: 'settings',
            component: SettingsView
        },
        {
            path: '/strava/callback',
            name: 'strava-callback',
            component: () => import('../views/callbackHandlers/StravaAuthCallbackHandlerView.vue')
        },
        {
            path: '/google/calendar/callback',
            name: 'google-calendar-callback',
            component: () => import('../views/callbackHandlers/GoogleCalendarAuthCallbackHandlerView.vue')
        },
        {
            path: '/about',
            name: 'about',
            component: () => import('../views/AboutView.vue')
        },
    ]
})

export default router
