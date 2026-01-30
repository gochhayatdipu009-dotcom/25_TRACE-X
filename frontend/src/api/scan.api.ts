import axios from "axios";
import type { ScanResponse } from "../types/scan.types";
import type { TimelineEvent } from "../types/timeline";

const API_BASE = "http://127.0.0.1:8000/api";

// ---------- Scan ----------
export async function runScan(username: string): Promise<ScanResponse> {
  const res = await axios.post(`${API_BASE}/scan`, { username });
  return res.data;
}

// ---------- Timeline ----------
export async function fetchTimeline(
  scanId: number
): Promise<TimelineEvent[]> {
  const res = await axios.get(
    `${API_BASE}/scan/${scanId}/timeline`
  );
  return res.data;
}
