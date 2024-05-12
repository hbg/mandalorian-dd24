DROP TABLE IF EXISTS solved_puzzles;
DROP TABLE IF EXISTS activation;

CREATE TABLE solved_puzzles (
    puzzle_id INTEGER NOT NULL,
    solved BIT NOT NULL DEFAULT 0
);

CREATE TABLE activation (
    activation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);