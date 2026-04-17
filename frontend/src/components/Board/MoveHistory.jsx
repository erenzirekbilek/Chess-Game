export default function MoveHistory({ moves = [] }) {
  const whiteMoves = moves.filter((_, i) => i % 2 === 0);
  const blackMoves = moves.filter((_, i) => i % 2 === 1);

  return (
    <div className="move-history">
      <h3>Move History</h3>
      <div className="moves-container">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>White</th>
              <th>Black</th>
            </tr>
          </thead>
          <tbody>
            {whiteMoves.map((move, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{move.to || move.san || move}</td>
                <td>{blackMoves[index]?.to || blackMoves[index]?.san || blackMoves[index] || ""}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}