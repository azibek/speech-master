import { Radar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
} from "chart.js";

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip);

type Props = { metrics: Record<string, number> };

export default function RadarChart({ metrics }: Props) {
  const labels = Object.keys(metrics);
  const data = {
    labels,
    datasets: [
      {
        label: "Similarity",
        data: Object.values(metrics).map((v) => Math.round(v * 100)),
        fill: true,
      },
    ],
  };
  const options = {
    scales: { r: { suggestedMin: 0, suggestedMax: 100 } },
    plugins: { legend: { display: false } },
  };
  return <Radar data={data} options={options} className="max-w-md" />;
}
