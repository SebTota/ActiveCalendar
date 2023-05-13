import type {IToken} from "@/interfaces/token";
import type { IUser } from "@/interfaces/user";
import { backendRouteBase } from "@/settings";
import axios from "axios";
import type {IMsg} from "@/interfaces/msg";

const client = axios.create({ baseURL: backendRouteBase });

function authHeaders(token: string) {
    return {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    };
}


export const api = {
    async googleAuthCallback(state: string) {
        return client.get<IToken>(`${backendRouteBase}/api/v1/google/callback?state=${state}`);
    },

    async googleCalendarAuthCallback(token: string, state: string, code: string) {
        const pack: any = authHeaders(token);
        pack['params'] = {
            state: state,
            code: code
        };
        return client.get<IMsg>(`${backendRouteBase}/api/v1/google/calendar/callback`, pack);
    },

    async stravaAuthCallback(token: string, code: string) {
      return client.get<IMsg>(`${backendRouteBase}/api/v1/strava/callback?code=${code}`, authHeaders(token));
    },

    async getMe(token: string) {
        return client.get<IUser>(`${backendRouteBase}/api/v1/users/me`, authHeaders(token));
    },
    
}