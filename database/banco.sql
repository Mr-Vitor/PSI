CREATE DATABASE IF NOT EXISTS prova;
USE prova;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
    matricula INT NOT NULL,
    email VARCHAR(200) NOT NULL,
    senha VARCHAR(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS exercicios (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome_exercicio VARCHAR(80) NOT NULL,
    descricao VARCHAR(200),
    exe_usuario_id INT NOT NULL,
    FOREIGN KEY (exe_usuario_id) REFERENCES usuarios(matricula)
    ON DELETE CASCADE
    ON UPDATE CASCADE 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;