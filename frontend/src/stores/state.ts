import {defineStore} from 'pinia'
import type {IToken} from '@/interfaces/token';
import type {IUser} from '@/interfaces/user';
import {api} from '@/api/api';
import {getLocalToken, isLoggedIn, removeLocalToken, saveLocalToken} from '@/utils/token';
import router from '@/router';
import {loginPath, settingsPath} from "@/settings";
import type {IMsg} from "@/interfaces/msg";
import type {CalendarTemplateType} from "@/enums/CalendarTemplateType";
import type {ICalendarTemplate} from "@/interfaces/calendarTemplate";

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
                token.access_token_expires = new Date(token.access_token_expires);
                if (token) {
                    saveLocalToken(token);
                    this.token = token;
                    this.isLoggedIn = true;
                    this.redirectToSettings();
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
        async authenticateUserWithGoogleCalendar(state: string, code: string) {
            if (!this.isLoggedIn || !this.hasValidAccessToken()) {
                console.debug("User tried to retrieve user info but is not logged in or access token is expired.");
                this.logout();
                this.redirectToLogin();
                return;
            }

            try {
                const response = await api.googleCalendarAuthCallback(this.token!.access_token, state, code);
                const data: IMsg = response.data;
                if (data && data.msg === "Authenticated") {
                    this.redirectToSettings();
                } else {
                    throw new Error("Failed to authenticate user with Google Calendar.");
                }
            } catch (error) {
                console.error("Failed to authenticate user with Google Calendar.", error);
                this.logout();
                throw new Error("Failed to authenticate user with Google Calendar.");
            }
        },
        async authenticateUserWithStrava(code: string) {
            if (!this.isLoggedIn || !this.hasValidAccessToken()) {
                console.debug("User tried to retrieve user info but is not logged in or access token is expired.");
                this.logout();
                this.redirectToLogin();
                return;
            }

            const response = await api.stravaAuthCallback(this.token!.access_token, code);
            const data: IMsg = response.data;
            if (data && data.msg === "Authenticated") {
                this.redirectToSettings();
            } else {
                throw new Error("Failed to authenticate user with Strava.");
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
                    console.debug("Failed to retrieve user info. Signing user out.");
                    this.logout();
                    this.redirectToLogin();
                }
            } catch (error) {
                console.error("Failed to retrieve user info.", error);
                throw new Error("Failed to retrieve user info.");
            }
        },
        async getCalendarTemplate(calendarTemplateType: CalendarTemplateType) {
            if (!this.isLoggedIn || !this.hasValidAccessToken()) {
                console.debug("User tried to retrieve user info but is not logged in or access token is expired.");
                this.logout();
                this.redirectToLogin();
                return;
            }

            try {
                const response = await api.getCalendarTemplate(this.token!.access_token, calendarTemplateType);
                const calendarTemplate: ICalendarTemplate = response.data;
                if (calendarTemplate) {
                    return calendarTemplate;
                } else {
                    console.debug("Failed to retrieve calendar template. Signing user out.");
                    this.logout();
                    this.redirectToLogin();
                }
            } catch (error: any) {
                console.error("Failed to retrieve calendar template.", error);
                throw new Error("Failed to retrieve calendar template.");
            }
        },
        async updateCalendarTemplate(id: string, template: ICalendarTemplate) {
            if (!this.isLoggedIn || !this.hasValidAccessToken()) {
                console.debug("User tried to retrieve user info but is not logged in or access token is expired.");
                this.logout();
                this.redirectToLogin();
                return;
            }

            try {
                const response = await api.updateCalendarTemplate(this.token!.access_token, id, template);
                const calendarTemplate: ICalendarTemplate = response.data;
                if (calendarTemplate) {
                    return calendarTemplate;
                } else {
                    console.debug("Failed to update calendar template. Signing user out.");
                    this.logout();
                    this.redirectToLogin();
                }
            } catch (error: any) {
                console.error("Failed to update calendar template.", error);
                throw new Error(error.response.data.detail);
            }
        },
        hasValidAccessToken() {
            return this.token && this.token.access_token_expires.getTime() > new Date().getTime();
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
