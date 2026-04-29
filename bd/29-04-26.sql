-- =============================================
-- BANCO DE DADOS: Oficina Mecânica com IA
-- Banco: PostgreSQL
-- =============================================

-- CLIENTES
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MECANICOS
CREATE TABLE mecanicos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- VEICULOS
CREATE TABLE veiculos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    placa VARCHAR(10) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    ano INTEGER,
    cor VARCHAR(30),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AGENDAMENTOS
CREATE TABLE agendamentos (
    id SERIAL PRIMARY KEY,
    veiculo_id INTEGER NOT NULL REFERENCES veiculos(id),
    mecanico_id INTEGER REFERENCES mecanicos(id),
    data_agendada TIMESTAMP NOT NULL,
    descricao TEXT,
    status VARCHAR(20) DEFAULT 'aguardando'
        CHECK (status IN ('aguardando', 'em_andamento', 'concluido', 'cancelado')),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIAGNOSTICOS (gerados pela IA)
CREATE TABLE diagnosticos (
    id SERIAL PRIMARY KEY,
    veiculo_id INTEGER NOT NULL REFERENCES veiculos(id),
    mecanico_id INTEGER REFERENCES mecanicos(id),
    sintomas TEXT NOT NULL,
    resultado_ia TEXT,
    urgencia VARCHAR(20)
        CHECK (urgencia IN ('baixa', 'media', 'alta', 'critica')),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PECAS EM ESTOQUE
CREATE TABLE pecas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    quantidade INTEGER DEFAULT 0,
    preco_unitario NUMERIC(10,2),
    estoque_minimo INTEGER DEFAULT 5,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ORDENS DE SERVICO
CREATE TABLE ordens_servico (
    id SERIAL PRIMARY KEY,
    veiculo_id INTEGER NOT NULL REFERENCES veiculos(id),
    mecanico_id INTEGER REFERENCES mecanicos(id),
    diagnostico_id INTEGER REFERENCES diagnosticos(id),
    descricao_servico TEXT,
    status VARCHAR(20) DEFAULT 'aberta'
        CHECK (status IN ('aberta', 'em_andamento', 'concluida', 'cancelada')),
    custo_total NUMERIC(10,2) DEFAULT 0,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    concluido_em TIMESTAMP
);

-- PECAS USADAS POR ORDEM DE SERVICO
CREATE TABLE ordens_pecas (
    id SERIAL PRIMARY KEY,
    ordem_id INTEGER NOT NULL REFERENCES ordens_servico(id),
    peca_id INTEGER NOT NULL REFERENCES pecas(id),
    quantidade INTEGER NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL
);

-- =============================================
-- DADOS DE EXEMPLO
-- =============================================

INSERT INTO clientes (nome, telefone, email) VALUES
    ('João Silva', '(11) 99999-1111', 'joao@email.com'),
    ('Maria Souza', '(11) 99999-2222', 'maria@email.com'),
    ('Carlos Lima', '(11) 99999-3333', 'carlos@email.com');

INSERT INTO mecanicos (nome, especialidade) VALUES
    ('Bruno', 'Motor e Suspensão'),
    ('Pedro', 'Elétrica Automotiva'),
    ('Ana', 'Freios e Transmissão');

INSERT INTO veiculos (cliente_id, placa, marca, modelo, ano, cor) VALUES
    (1, 'ABC1D23', 'Volkswagen', 'Gol', 2015, 'Prata'),
    (2, 'XYZ9H87', 'Honda', 'Civic', 2020, 'Preto'),
    (3, 'DEF4G56', 'Chevrolet', 'Onix', 2018, 'Branco');

INSERT INTO pecas (nome, descricao, quantidade, preco_unitario, estoque_minimo) VALUES
    ('Filtro de óleo', 'Filtro de óleo universal', 15, 25.00, 5),
    ('Pastilha de freio dianteira', 'Par de pastilhas dianteiras', 8, 85.00, 3),
    ('Correia dentada', 'Correia dentada 115 dentes', 4, 120.00, 2),
    ('Vela de ignição', 'Vela NGK comum', 30, 18.00, 10),
    ('Óleo motor 5W30', 'Litro de óleo sintético', 20, 35.00, 8);