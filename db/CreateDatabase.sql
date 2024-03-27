CREATE TABLE Enquetes (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    descricao TEXT
) DEFAULT CHARSET=utf8;

CREATE TABLE Opcoes (
    id INTEGER PRIMARY KEY,
    enquete_id INTEGER,
    descricao TEXT NOT NULL,
    votos INTEGER DEFAULT 0,
    FOREIGN KEY(enquete_id) REFERENCES Enquetes(id)
) DEFAULT CHARSET=utf8;

INSERT INTO Enquetes (titulo, descricao) VALUES ('Enquete 1', 'Descrição da Enquete 1');
INSERT INTO Opcoes (enquete_id, descricao) VALUES (1, 'Opção 1 da Enquete 1');
INSERT INTO Opcoes (enquete_id, descricao) VALUES (1, 'Opção 2 da Enquete 1');
