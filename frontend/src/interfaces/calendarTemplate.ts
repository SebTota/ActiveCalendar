import type {CalendarTemplateStatus} from "@/enums/CalendarTemplateStatus";
import type {CalendarTemplateType} from "@/enums/CalendarTemplateType";

export interface ICalendarTemplate {
    id: string,
    status: CalendarTemplateStatus,
    type: CalendarTemplateType,
    title_template: string,
    body_template: string
}