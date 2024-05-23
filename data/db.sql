CREATE TABLE Course (
    id INT PRIMARY KEY,
    block VARCHAR(255),
    name VARCHAR(255),
    desc TEXT,
    credits VARCHAR(5),
    requisites TEXT,
    repeatable INT,
    lastTaught TEXT,
    level INT,
    breadth TEXT,
    grad INT,
    lns INT,
    ethnic INT,
    honors INT,
    genEd INT,
    workplace INT,
    foreignLang INT
);

CREATE INDEX idx_block ON Course (block);