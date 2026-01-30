import type { TimelineEvent } from "../../types/timeline";

interface Props {
  events: TimelineEvent[];
}

export default function Timeline({ events }: Props) {
  if (!events || events.length === 0) {
    return (
      <div className="mt-6 p-4 rounded-lg border border-gray-700 text-gray-400">
        No timeline events yet.
      </div>
    );
  }

  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-3">
        Exposure Timeline
      </h2>

      <div className="space-y-3">
        {events.map((e, i) => {
          const date = e.detected_at
            ? new Date(e.detected_at).toLocaleString()
            : "Unknown time";

          return (
            <div
              key={i}
              className="p-4 rounded-lg border border-gray-700"
            >
              <div className="flex justify-between text-sm text-gray-400">
                <span className="uppercase">{e.event_type}</span>
                <span>{date}</span>
              </div>

              <div className="mt-1 text-sm">
                Platform exposure change detected
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
