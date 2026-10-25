import "./control.css";
import { useState } from "react";

function ControlPanel({ agvs, locations }) {
  // Lưu xe đã chọn
  const [selectedAGV, setSelectedAGV] = useState("");
  // Lưu điểm bắt đầu đã chọn
  const [startPoint, setStartPoint] = useState("");
  // Lưu điểm kết thúc đã chọn
  const [endPoint, setEndPoint] = useState("");

  //submit
  function handleSubmit() {
    if (!selectedAGV || !startPoint || !endPoint) {
      alert("Hãy chọn xe, điểm bắt đầu và điểm kết thúc!");
      return;
    }

    const missionData = {
      agv: Number(selectedAGV),
      start_point: Number(startPoint),
      end_point: Number(endPoint),
    };

    fetch("http://127.0.0.1:8000/api/mission/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(missionData),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((error) => {
            console.log("Lỗi từ Django:", error);
            throw new Error("Không tạo được nhiệm vụ");
          });
        }
        return res.json();
      })
      .then((data) => {
        console.log("Nhiệm vụ đã tạo:", data);
        alert("Giao nhiệm vụ thành công!");
      })
      .catch((err) => {
        console.error("Lỗi gửi nhiệm vụ:", err);
        alert("Giao nhiệm vụ thất bại! Kiểm tra Console.");
      });
  }

  //hàm clear
  function handleClear() {
    setSelectedAGV("");
    setStartPoint("");
    setEndPoint("");
  }

  // Xử lý khi nhấn STOP
  function handleStop() {
    fetch("http://127.0.0.1:8000/api/agv/stop_all/", {
      method: "POST",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("STOP thất bại");
        }
        return res.json();
      })
      .then((data) => {
        alert(data.message);
      })
      .catch((error) => {
        console.error(error);
        alert("Không gọi được API STOP!");
      });
  }

  return (
    <section className="control-panel">
      <div className="control-buttons">
        <button className="stop-button" onClick={handleStop}>
          STOP
        </button>
      </div>

      <div className="select-box-container">
        <select
          value={startPoint}
          onChange={(e) => setStartPoint(e.target.value)}
        >
          <option value="" disabled>
            Start point
          </option>
          {locations?.map((location) => (
            <option key={location.id} value={location.id}>
              {location.name}
            </option>
          ))}
        </select>

        <select value={endPoint} onChange={(e) => setEndPoint(e.target.value)}>
          <option value="" disabled>
            End point
          </option>
          {locations?.map((location) => (
            <option key={location.id} value={location.id}>
              {location.name}
            </option>
          ))}
        </select>

        {/* Chọn xe */}
        <select
          value={selectedAGV}
          onChange={(e) => setSelectedAGV(e.target.value)}
        >
          <option value="" disabled>
            Select robot
          </option>
          {agvs?.map((agv) => (
            <option key={agv.id} value={agv.id}>
              {agv.name}
            </option>
          ))}
        </select>
      </div>

      {/* Các nút hành động */}
      <div className="action-buttons">
        <button className="submit-button" onClick={handleSubmit}>
          Submit
        </button>
        <button className="clear-button" onClick={handleClear}>
          Clear
        </button>
      </div>
    </section>
  );
}

export default ControlPanel;
