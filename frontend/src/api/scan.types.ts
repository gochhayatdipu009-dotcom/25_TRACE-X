export interface ReverseOsintFlag {
  signal: string;
  explanation: string;
  confidence: number;
}

export interface PlatformResult {
  platform: string;
  exists: boolean;
  evidence_count: number;
  risk_score?: number | null;
  risk_level?: "Low" | "Medium" | "High" | "unknown";
  reverse_osint_flags?: ReverseOsintFlag[];
}

export interface ScanResponse {
  scan_id: number;
  username: string;
  platforms: PlatformResult[];
}
