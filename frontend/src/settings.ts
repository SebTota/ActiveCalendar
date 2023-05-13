// UI Paths
export const homePath: string = "/";
export const loginPath: string = "/login";
export const settingsPath: string = "/settings";
export const aboutPath: string = "/about";


function getBackendRoute(): string {
    const dev: boolean = true;

    if (dev) {
        return `http://localhost`;
    } else {
        return `https://${window.location.hostname}`;
    }
    
}

export const backendRouteBase: string = getBackendRoute();
export const stravaAuthPath: string = `${backendRouteBase}/api/v1/strava/auth`;
export const googleAuthPath: string = `${backendRouteBase}/api/v1/google/auth`;
export const googleCalendarAuthPath: string = `${backendRouteBase}/api/v1/google/calendar/auth`;

