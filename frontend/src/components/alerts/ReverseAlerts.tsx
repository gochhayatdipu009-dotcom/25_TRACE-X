import type { PlatformResult } from "../../types/scan.types";
import { severityColor } from "../../utils/severityColor";

interface Props {
  platforms: PlatformResult[];
}

function confidenceToSeverity(confidence: number): "low" | "medium" | "high" {
  if (confidence >= 0.75) return "high";
  if (confidence >= 0.4) return "medium";
  return "low";
}

export default function ReverseAlerts({ platforms }: Props) {
  const alerts = platforms.flatMap((p) =>
    (p.reverse_osint_flags ?? []).map((flag) => {
      const severity = confidenceToSeverity(flag.confidence);

      return {
        platform: p.platform,
        signal: flag.signal,
        explanation: flag.explanation,
        confidence: flag.confidence,
        severity,
      };
    })
  );

  if (alerts.length === 0) {
    return (
      <div className="mt-6 p-4 rounded-lg border border-gray-700 text-gray-400">
        No reverse OSINT signals detected.
      </div>
    );
  }

  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-3 text-red-400">
        Reverse OSINT Alerts
      </h2>

      <div className="space-y-3">
        {alerts.map((a, i) => (
          <div
            key={i}
            className={`p-4 rounded-lg border ${severityColor(a.severity)}`}
          >
            <div className="flex justify-between items-center">
              <span className="font-semibold capitalize">
                {a.platform}
              </span>
              <span className="uppercase text-xs font-mono">
                {a.severity}
              </span>
            </div>

            <div className="text-sm mt-2 text-gray-300">
              {a.explanation}
            </div>

            <div className="text-xs mt-1 text-gray-500">
              Confidence: {(a.confidence * 100).toFixed(0)}%
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
