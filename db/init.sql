-- Script para executar APÓS criar o banco petshop manualmente
-- Tabela de pets
CREATE TABLE pets (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL CHECK (especie IN ('Cachorro','Gato','Outro')),
    tutor TEXT NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabela de serviços
CREATE TABLE servicos (
    id SERIAL PRIMARY KEY,
    pet_id INT NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    data TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Dados de exemplo
INSERT INTO pets (nome, especie, tutor) VALUES 
('Rex', 'Cachorro', 'João Silva'),
('Mimi', 'Gato', 'Maria Santos'),
('Bob', 'Cachorro', 'Pedro Costa');

INSERT INTO servicos (pet_id, descricao) VALUES 
(1, 'Banho e tosa'),
(1, 'Vacinação antirrábica'),
(2, 'Consulta veterinária'),
(3, 'Banho');