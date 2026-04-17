export class GameReplay {
  constructor(moves = []) {
    this.moves = moves;
    this.currentIndex = -1;
  }

  next() {
    if (this.currentIndex < this.moves.length - 1) {
      this.currentIndex++;
      return this.moves[this.currentIndex];
    }
    return null;
  }

  prev() {
    if (this.currentIndex >= 0) {
      return this.moves[this.currentIndex--];
    }
    return null;
  }

  goTo(index) {
    if (index >= 0 && index < this.moves.length) {
      this.currentIndex = index;
      return this.moves[this.currentIndex];
    }
    return null;
  }

  getCurrentMove() {
    return this.moves[this.currentIndex] || null;
  }

  getPosition() {
    return this.currentIndex + 1;
  }

  isAtEnd() {
    return this.currentIndex >= this.moves.length - 1;
  }

  isAtStart() {
    return this.currentIndex <= 0;
  }

  reset() {
    this.currentIndex = -1;
  }
}