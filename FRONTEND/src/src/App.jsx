import TrainMap from "./components/TrainMap";
import ScheduleUpload from "./components/ScheduleUpload";
import PriorityForm from "./components/PriorityForm";
import Recommendations from "./components/Recommendations";

export default function App() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-center">
        🚆 Railway AI Optimization Dashboard
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ScheduleUpload />
        <PriorityForm />
      </div>
      <Recommendations />
      <TrainMap />
    </div>
  );
}
