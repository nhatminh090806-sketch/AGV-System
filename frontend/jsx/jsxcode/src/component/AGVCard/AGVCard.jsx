import "./Card.css";
function AGVCard({ agv, clickCard, isSelected }) {
  return (
    <div
      className={`agv-card ${isSelected ? "active" : ""}`}
      onClick={clickCard}
    >
      <span>{agv.name}</span>
      <span>{agv.status}</span>

      <progress value={agv.battery} max="100" />
      <span>{agv.battery}%</span>
    </div>
  );
}

export default AGVCard;
