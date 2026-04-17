const DIFFICULTY_LEVELS = [
  { value: "easy", label: "Easy", depth: 2, description: "Beginner level" },
  { value: "medium", label: "Medium", depth: 3, description: "Intermediate level" },
  { value: "hard", label: "Hard", depth: 4, description: "Advanced level" },
  { value: "expert", label: "Expert", depth: 6, description: "Master level" },
];

export default function DifficultySelector({ value, onChange, disabled = false }) {
  return (
    <div className="difficulty-selector">
      <label>Difficulty:</label>
      <div className="difficulty-options">
        {DIFFICULTY_LEVELS.map((level) => (
          <button
            key={level.value}
            className={`difficulty-btn ${value === level.value ? "active" : ""}`}
            onClick={() => onChange(level.value)}
            disabled={disabled}
            title={level.description}
          >
            {level.label}
          </button>
        ))}
      </div>
    </div>
  );
}