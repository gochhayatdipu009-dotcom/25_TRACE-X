export type Severity = "low" | "medium" | "high";

export interface ReverseOSINTFlag {
  type: string;
  description: string;
  severity: Severity;
  detected_at?: string;
}
export interface TimelineEvent {
  event_type: "new" | "removed" | "changed";
  platform_exposure_id: number;
  previous_value: string | null;
  current_value: string | null;
  detected_at: string;
}


