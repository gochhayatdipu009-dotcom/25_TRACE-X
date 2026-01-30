interface Props {
  score: number; // 0–100
  level?: "Low" | "Medium" | "High";
  size?: number;
}

export default function RiskRing({
  score,
  level = "Low",
  size = 72,
}: Props) {
  const radius = size / 2 - 6;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.min(Math.max(score, 0), 100);
  const offset = circumference - (progress / 100) * circumference;

  const color =
    level === "High"
      ? "stroke-red-500"
      : level === "Medium"
      ? "stroke-orange-400"
      : "stroke-green-400";

  return (
    <svg width={size} height={size}>
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="transparent"
        strokeWidth="6"
        className="stroke-gray-700"
      />

      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="transparent"
        strokeWidth="6"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        className={`${color} transition-all duration-700`}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />

      <text
        x="50%"
        y="50%"
        dominantBaseline="middle"
        textAnchor="middle"
        className="fill-gray-200 text-sm font-semibold"
      >
        {Math.round(progress)}
      </text>
    </svg>
  );
}
