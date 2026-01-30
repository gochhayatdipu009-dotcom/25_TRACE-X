import type { Severity } from "../types/timeline";

export function severityColor(severity: Severity) {
  switch (severity) {
    case "high":
      return "border-red-500 bg-red-500/10 text-red-400";
    case "medium":
      return "border-orange-400 bg-orange-400/10 text-orange-300";
    case "low":
      return "border-yellow-400 bg-yellow-400/10 text-yellow-300";
    default:
      return "border-gray-600 bg-gray-800 text-gray-300";
  }
}
