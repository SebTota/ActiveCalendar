// UI Paths
export const homePath: string = "/";
export const loginPath: string = "/login";
export const settingsPath: string = "/settings";
export const aboutPath: string = "/about";


function getBackendRoute(): string {
    const env = import.meta.env.VITE_APP_ENV;
    console.log(`VUE_APP_ENV: ${env}`);

    if (env === "production") {
        return `https://active.sebtota.com`;
    } else {
        return `http://localhost`;
    }
}

export const backendRouteBase: string = getBackendRoute();
export const stravaAuthPath: string = `${backendRouteBase}/api/v1/strava/auth`;
export const googleAuthPath: string = `${backendRouteBase}/api/v1/google/auth`;
export const googleCalendarAuthPath: string = `${backendRouteBase}/api/v1/google/calendar/auth`;

