DROP TABLE IF EXISTS solved_puzzles;
DROP TABLE IF EXISTS activation;
DROP TABLE IF EXISTS comm_status;

CREATE TABLE solved_puzzles (
    puzzle_id INTEGER NOT NULL,
    solved BIT NOT NULL DEFAULT 0
);

CREATE TABLE activation (
    activation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comm_status (
    phone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    comm_id  VARCHAR(32),
    solved BIT NOT NULL DEFAULT 0
);
