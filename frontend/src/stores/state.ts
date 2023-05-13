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
        async getMe() {
            if (!this.isLoggedIn || !this.hasValidAccessToken()) {
                console.debug("User tried to retrieve user info but is not logged in or access token is expired.");
                this.logout();
                this.redirectToLogin();
                return;
            }

            try {
                const response = await api.getMe(this.token!.access_token);
                const user: IUser = response.data;
                if (user) {
                    this.user = user;
                    return this.user;
                } else {
                    this.logout();
                    this.redirectToLogin();
                }
            } catch (error) {
                console.error("Failed to retrieve user info.", error);
                throw new Error("Failed to retrieve user info.");
            }
        },
        hasValidAccessToken() {
            return this.token && this.token.access_token_expires > new Date();
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
