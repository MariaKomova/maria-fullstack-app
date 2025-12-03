CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);
INSERT INTO items (name, description) VALUES
('Монитор', 'Компьютерный монитор Dell'),
('Клавиатура', 'Механическая клавиатура Logitech');

