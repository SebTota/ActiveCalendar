import { defineStore } from 'pinia'
import type { IToken } from '@/interfaces/token';
import type { IUser } from '@/interfaces/user';
import { api } from '@/api/api';
import {getLocalToken, isLoggedIn, removeLocalToken, saveLocalToken} from '@/utils/token';
import router from '@/router';
import {loginPath, settingsPath} from "@/settings";

export interface MainState {
    token: IToken | null;
    isLoggedIn: boolean;
    user: IUser | null;
}

export const useMainStore = defineStore('mainState', {
    state: (): MainState => {
        return {
            token: getLocalToken(),
            isLoggedIn: isLoggedIn(),
            user: null
        }
    },

    actions: {
        async authenticateUserWithGoogle(state: string) {
            try {
                const response = await api.googleAuthCallback(state);
                const token: IToken = response.data;
                if (token) {
                    saveLocalToken(token);
                    this.token = token;
                    this.isLoggedIn = true;
                    this.redirectToHomePage(false);
                } else {
                    this.logout();
                    this.redirectToLogin();
                }
            } catch (error) {
                console.error("Failed to authenticate user with Google.", error);
                this.logout();
                throw new Error("Failed to authenticate user with Google.");
            }

        },
        logout() {
            this.removeLogin();
        },
        removeLogin() {
            this.token = null;
            this.user = null;
            this.isLoggedIn = false;
            removeLocalToken();
        },
        redirectToSettings() {
            if (router.currentRoute.value.path !== settingsPath) {
                console.debug("Redirecting to settings page...");
                router.push({path: settingsPath});
            }
        },
        redirectToLogin() {
            if (router.currentRoute.value.path !== loginPath) {
                console.debug("Redirecting to login page...");
                router.push({path: loginPath});
            }
        },
        redirectToHomePage(forceRefresh: boolean = true) {
            if (forceRefresh || router.currentRoute.value.path !== '/') {
                console.debug("Redirecting to home page...");
                router.push({path: '/'}).then(() => {
                    if (forceRefresh) {
                        router.go(0);
                    }
                })
            }
        }
    }
})
