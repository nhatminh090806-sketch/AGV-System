import "./App.css";
import Header from "./component/Header/Header";
import ControlPanel from "./component/ControlPanel/ControlPanel";
import Map from "./component/Map/Map";
import AGVCard from "./component/AGVCard/AGVCard";
import UnitDetail from "./component/unitdetail/UnitDetail";
import { useEffect, useState } from "react";

function App() {
  // Lưu danh sách AGV và vị trí từ backend
  const [agvs, setAgvs] = useState([]);
  const [locations, setLocations] = useState([]);
  // Lưu ID của xe đang được chọn
  const [detailAGVId, setDetailAGVId] = useState(null);
  //gọi API django
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/agv/")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Không lấy được danh sách AGV");
        }
        return res.json();
      })
      .then((data) => {
        setAgvs(data);
      })
      .catch((err) => console.error("Lỗi lấy AGV:", err));

    fetch("http://127.0.0.1:8000/api/location/")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Không lấy được danh sách điểm");
        }
        return res.json();
      })
      .then((data) => {
        setLocations(data);
      })
      .catch((err) => console.error("Lỗi lấy Location:", err));
  }, []);

  return (
    <div className="dashboard-layout">
      <div className="layout-left">
        <Header />
        <ControlPanel agvs={agvs} locations={locations} />
      </div>

      <div className="layout-center">
        <div className="map-area">
          <Map />
        </div>
        {/* Hiển thị danh sách AGV */}

        <div className="cards-area">
          {agvs.map((agv) => (
            <AGVCard
              key={agv.id}
              agv={agv}
              isSelected={agv.id === detailAGVId}
              clickCard={() => setDetailAGVId(agv.id)}
            />
          ))}
        </div>
      </div>

      <div className="layout-right">
        <UnitDetail agv={agvs.find((item) => item.id === detailAGVId)} />
        {/*props tên agv gán detail id cho unitdetail */}
      </div>
    </div>
  );
}

export default App;
