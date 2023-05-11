import type {IToken} from "@/interfaces/token";
import type { IUser } from "@/interfaces/user";
import { backendRouteBase } from "@/settings";
import axios from "axios";

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

    async getMe(token: string) {
        return client.get<IUser>(`${backendRouteBase}/api/v1/users/me`, authHeaders(token));
    },
    
}