export interface IUser {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
    status: string;
    is_superuser: boolean;
    hasStravaAuth: boolean;
    hasGoogleCalendarAuth: boolean;
}