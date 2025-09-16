import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useState, useEffect } from "react";
import { getPredictions } from "../api";
import L from "leaflet";

const trainIcon = new L.Icon({
  iconUrl: "https://cdn-icons-png.flaticon.com/512/747/747310.png",
  iconSize: [30, 30],
});

export default function TrainMap() {
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const data = await getPredictions();
      setPredictions(data);
    }
    fetchData();
    const interval = setInterval(fetchData, 5000); // refresh every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-[500px] w-full rounded-lg shadow-md border">
      <MapContainer
        center={[20.5937, 78.9629]} // center on India
        zoom={5}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap"
        />
        {predictions.map((p, idx) => (
          <Marker
            key={idx}
            position={[p.lat || 20, p.lon || 78]} // fallback India
            icon={trainIcon}
          >
            <Popup>
              🚆 Train {p.train_number} <br />
              Station: {p.station_code || "On route"} <br />
              Predicted Delay: {p.predicted_delay_minutes.toFixed(1)} mins
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
