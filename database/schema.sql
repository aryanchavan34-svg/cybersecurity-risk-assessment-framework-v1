CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    owner TEXT NOT NULL,
    description TEXT,
    confidentiality INTEGER NOT NULL CHECK(confidentiality BETWEEN 1 AND 5),
    integrity INTEGER NOT NULL CHECK(integrity BETWEEN 1 AND 5),
    availability INTEGER NOT NULL CHECK(availability BETWEEN 1 AND 5),
    criticality_score REAL NOT NULL,
    criticality TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
