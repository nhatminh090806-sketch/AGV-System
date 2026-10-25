import "./UnitDetail.css";

function UnitDetail({ agv }) {
  if (!agv) {
    return (
      <div className="unit-detail">
        <div className="section-title">UNIT DETAIL</div>
        <p className="empty-text">Chọn một AGV để xem chi tiết</p>
      </div>
    );
  }

  return (
    <div className="unit-detail">
      {/* Tiêu đề */}
      <div className="section-title">UNIT DETAIL</div>

      {/* Tên xe và Trạng thái */}
      <div className="unit-header">
        <h3>{agv.name}</h3>
        <span className="status-badge">{agv.status}</span>
      </div>

      {/* Thông số Telemetry */}
      <div className="telemetry-section">
        <div className="telemetry-title">TELEMETRY</div>

        <div className="telemetry-grid">
          <div className="telemetry-item">
            <span className="label">BATTERY</span>
            <span className="value text-cyan">{agv.battery}%</span>
          </div>
          <div className="telemetry-item">
            <span className="label">SPEED</span>
            <span className="value">{agv.speed} M/S</span>
          </div>
          <div className="telemetry-item">
            <span className="label">PAYLOAD</span>
            <span className="value">{agv.payload} KG</span>
          </div>
          <div className="telemetry-item">
            <span className="label">TRIPS</span>
            <span className="value">{agv.trips}</span>
          </div>
        </div>

        {/* Thanh ngang */}
        <div className="telemetry-bar"></div>
      </div>
    </div>
  );
}

export default UnitDetail;
