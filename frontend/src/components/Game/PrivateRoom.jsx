export default function PrivateRoom({ roomId, onCopyLink, onShare }) {
  const shareUrl = `${window.location.origin}/room/${roomId}`;

  const handleCopy = () => {
    navigator.clipboard.writeText(shareUrl);
    onCopyLink?.();
  };

  return (
    <div className="private-room">
      <h3>Private Room</h3>
      <div className="room-link">
        <input type="text" value={shareUrl} readOnly />
        <button onClick={handleCopy}>Copy</button>
      </div>
      <div className="share-options">
        <button onClick={onShare}>Share</button>
      </div>
    </div>
  );
}