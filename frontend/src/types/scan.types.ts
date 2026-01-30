export type RiskLevel = "Low" | "Medium" | "High";

export interface PlatformResult {
  platform: string;
  exists: boolean;
  status: "confirmed" | "not_found" | "blocked" | "error";
  url?: string | null;
  evidence_count: number;
  risk_score?: number;
  risk_level?: RiskLevel;   // 🔥 FIXED
  reverse_osint_flags?: any[];
}

export interface ScanResponse {
  scan_id: number;
  username: string;
  platforms: PlatformResult[];
}
