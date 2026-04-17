export default function RoomPage({ roomId }) {
  return (
    <div className="room-page">
      <h1>Private Room</h1>
      <p>Room ID: {roomId}</p>
      <p>Waiting for opponent...</p>
    </div>
  );
}