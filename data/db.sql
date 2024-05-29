-- Create the 'classes' table
CREATE TABLE classes (
    block VARCHAR NOT NULL,
    name VARCHAR,
    description TEXT,
    requisites TEXT,
    repeatable TEXT,
    lastTaught DATE,
    level INTEGER,
    breadth VARCHAR,
    grad INTEGER,
    lns INTEGER,
    ethnic INTEGER,
    honors INTEGER,
    genEd INTEGER,
    workplace INTEGER,
    foreignLang INTEGER,
    min_credits INTEGER,
    max_credits INTEGER,
    PRIMARY KEY (block)
);

-- Create the 'grades' table
CREATE TABLE grades (
    block VARCHAR NOT NULL,
    total INTEGER,
    aCount INTEGER,
    abCount INTEGER,
    bCount INTEGER,
    bcCount INTEGER,
    cCount INTEGER,
    dCount INTEGER,
    fCount INTEGER,
    letter CHAR(2),
    FOREIGN KEY (block) REFERENCES classes (block)
);

-- Create an index on the 'block' column in the 'classes' table
CREATE INDEX block_index ON classes (block);
