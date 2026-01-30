import { useState } from "react";
import { runScan, fetchTimeline } from "../api/scan.api";
import type { ScanResponse, PlatformResult } from "../types/scan.types";
import type { TimelineEvent } from "../types/timeline";

import RiskRing from "../components/charts/RiskRing";
import ReverseAlerts from "../components/alerts/ReverseAlerts";
import Timeline from "../components/timeline/Timeline";

export default function Dashboard() {
  const [username, setUsername] = useState("");
  const [scan, setScan] = useState<ScanResponse | null>(null);
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleScan() {
    if (!username.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await runScan(username.trim());
      setScan(data);

      // 🔹 REAL timeline fetch
      try {
        const events = await fetchTimeline(data.scan_id);
        setTimelineEvents(events);
      } catch {
        setTimelineEvents([]);
      }
    } catch {
      setError("Scan failed. Check backend logs.");
      setTimelineEvents([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-slate-900 to-black text-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6">OSINT Dashboard</h1>

      {/* Scan input */}
      <div className="flex gap-3 mb-6">
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter username"
          className="px-4 py-2 rounded bg-gray-800 border border-gray-700 w-64"
        />
        <button
          onClick={handleScan}
          disabled={loading}
          className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Scanning..." : "Scan"}
        </button>
      </div>

      {error && (
        <div className="mb-4 text-red-400 font-medium">
          {error}
        </div>
      )}

      {/* Scan meta */}
      {scan && (
        <div className="mb-6 text-sm text-gray-400">
          Scan #{scan.scan_id} — Username: {scan.username}
        </div>
      )}

      {/* Platform results */}
      <div className="space-y-4">
        {scan?.platforms.map((p: PlatformResult) => (
          <div
            key={p.platform}
            className="border border-gray-700 rounded-lg p-4 flex justify-between items-center"
          >
            <div>
              <div className="font-semibold text-lg capitalize">
                {p.platform}
              </div>

              <div>
                Exists:{" "}
                <span className={p.exists ? "text-green-400" : "text-gray-400"}>
                  {p.exists ? "Yes" : "No"}
                </span>
              </div>

              <div>Evidence: {p.evidence_count}</div>

              {p.risk_level && (
                <div className="mt-1 text-sm">
                  Risk Level:{" "}
                  <span
                    className={
                      p.risk_level === "High"
                        ? "text-red-400"
                        : p.risk_level === "Medium"
                        ? "text-orange-400"
                        : "text-green-400"
                    }
                  >
                    {p.risk_level}
                  </span>
                </div>
              )}
            </div>

            {typeof p.risk_score === "number" && (
              <RiskRing
                score={p.risk_score}
                level={p.risk_level}
              />
            )}
          </div>
        ))}
      </div>

      {/* Reverse OSINT alerts */}
      {scan && (
        <ReverseAlerts platforms={scan.platforms} />
      )}

      {/* Timeline (REAL DATA) */}
      <Timeline events={timelineEvents} />
    </div>
  );
}
