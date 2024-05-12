DROP TABLE IF EXISTS solved_puzzles;

CREATE TABLE solved_puzzles (
    puzzle_id INTEGER NOT NULL,
    solved BIT NOT NULL DEFAULT 0
);