class UserSummaryTemplates {

  // Per Run Template
  perRunSummaryEnabled: boolean;
  perRunSummaryTemplate: string;

  // Daily Template
  dailySummaryEnabled: boolean;
  dailySummaryTemplate: string;

  // Weekly Template
  weeklySummaryEnabled: boolean;
  weeklySummaryTemplate: string;
  weeklySummaryDay: string;  // Day of the week the weekly summary should be present

  constructor(perRunSummaryEnabled: boolean, perRunSummaryTemplate: string, perRunTitleTemplate: string,
              dailySummaryEnabled: boolean, dailySummaryTemplate: string, dailySummaryTitleTemplate: string,
              weeklySummaryEnabled: boolean, weeklySummaryTemplate: string, weeklySummaryTitleTemplate: string,
              weeklySummaryDay: string) {
    this.perRunSummaryEnabled = perRunSummaryEnabled
    this.perRunSummaryTemplate = perRunSummaryTemplate
    this.dailySummaryEnabled = dailySummaryEnabled
    this.dailySummaryTemplate = dailySummaryTemplate
    this.weeklySummaryEnabled = weeklySummaryEnabled
    this.weeklySummaryTemplate = weeklySummaryTemplate
    this.weeklySummaryDay = weeklySummaryDay
  }

}
