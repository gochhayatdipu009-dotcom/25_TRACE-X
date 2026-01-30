export interface PlatformResult {
  platform: "github" | "instagram";
  exists: boolean;
  status: "confirmed" | "not_found" | "blocked" | "error";
  url?: string | null;
  evidence_count: number;
  risk_score?: number;
  risk_level?: "Low" | "Medium" | "High";
  reverse_osint_flags?: any[];
}

export interface ScanResponse {
  scan_id: number;
  username: string;
  platforms: PlatformResult[];
}
