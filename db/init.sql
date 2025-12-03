CREATE TABLE items (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	description TEXT,
    value INTEGER
);
INSERT INTO items (name, description, value) VALUES
('Item A', 'First item in the catalog', 10),
('Item B', 'Second item in the catalog', 20);
