import type {IToken} from "@/interfaces/token";

const LOCAL_STORAGE_NAME_AUTH_TOKEN: string = 'ActiveRunAuthToken';

export const getLocalToken = (): IToken | null => {
    const serializedToken: string | null = localStorage.getItem(LOCAL_STORAGE_NAME_AUTH_TOKEN);
    if (serializedToken) {
        const t: IToken = JSON.parse(serializedToken) as IToken;
        t.access_token_expires = new Date(t.access_token_expires);
        return t;
    }
    return null;
}

export const saveLocalToken = (token: IToken) => {
    localStorage.setItem(LOCAL_STORAGE_NAME_AUTH_TOKEN, JSON.stringify(token));
}

export const removeLocalToken = () => {
    localStorage.removeItem(LOCAL_STORAGE_NAME_AUTH_TOKEN);
}