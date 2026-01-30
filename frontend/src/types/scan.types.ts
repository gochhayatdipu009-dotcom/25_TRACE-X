// ---------- Platform-level result ----------
export interface PlatformResult {
  platform: string;
  exists: boolean;
  evidence_count: number;

  // optional intelligence
  risk_score?: number;
  risk_level?: "Low" | "Medium" | "High";

  reverse_osint_flags?: {
    signal: string;
    explanation: string;
    confidence: number;
  }[];
}

// ---------- Scan response ----------
export interface ScanResponse {
  scan_id: number;
  username: string;
  scanned_at?: string;

  platforms: PlatformResult[];
}
