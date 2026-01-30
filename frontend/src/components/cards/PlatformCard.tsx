import type { PlatformResult } from "../../api/scan.types";

interface Props {
  result: PlatformResult;
}

export default function PlatformCard({ result }: Props) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold capitalize">
          {result.platform}
        </h3>
        <span
          className={`text-sm px-2 py-1 rounded ${
            result.risk_level === "High"
              ? "bg-red-500"
              : result.risk_level === "Medium"
              ? "bg-yellow-500"
              : "bg-green-500"
          }`}
        >
          {result.risk_level}
        </span>
      </div>

      <div className="mt-4 space-y-1 text-sm text-slate-300">
        <div>Exists: {result.exists ? "Yes" : "No"}</div>
        <div>Risk Score: {result.risk_score}</div>
        <div>Evidence: {result.evidence_count}</div>
      </div>
    </div>
  );
}
