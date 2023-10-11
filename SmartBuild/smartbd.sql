-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 22/09/2023 às 07:07
-- Versão do servidor: 10.4.28-MariaDB
-- Versão do PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `smartbd`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `cadastro`
--

CREATE TABLE `cadastro` (
  `id_smart` int(11) NOT NULL,
  `nome_smart` varchar(45) NOT NULL,
  `senha_smart` varchar(45) NOT NULL,
  `email_smart` varchar(45) NOT NULL,
  `username_smart` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='cadastro banco';

--
-- Despejando dados para a tabela `cadastro`
--

INSERT INTO `cadastro` (`id_smart`, `nome_smart`, `senha_smart`, `email_smart`, `username_smart`) VALUES
(27, 'Victor Henrique Amorim Correia', '!008976Vvt', 'victorhuski@gmail.com', 'oAmorim'),
(28, 'Eduardo de Caprio', '12345!Vv', 'Edudocaprio@hotmail.com', 'Edu');

-- --------------------------------------------------------

--
-- Estrutura para tabela `objetos`
--

CREATE TABLE `objetos` (
  `id_ob` int(11) NOT NULL,
  `tipo_ob` varchar(10) NOT NULL,
  `padx_ob` float NOT NULL,
  `pady_ob` float NOT NULL,
  `altura_ob` float NOT NULL,
  `largura_ob` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `objetos`
--

INSERT INTO `objetos` (`id_ob`, `tipo_ob`, `padx_ob`, `pady_ob`, `altura_ob`, `largura_ob`) VALUES
(3, 'Quadrado', 640, 337.5, 21, 13),
(4, 'Quadrado', 640, 337.5, 0, 0),
(5, 'Quadrado', 640, 337.5, 200, 200),
(6, 'Quadrado', 640, 337.5, 200, 200),
(7, 'Quadrado', 640, 337.5, 200, 200),
(8, 'Quadrado', 640, 337.5, 200, 200),
(9, 'Quadrado', 640, 337.5, 200, 200),
(10, 'Quadrado', 640, 337.5, 200, 200),
(11, 'Quadrado', 640, 337.5, 200, 200),
(12, 'Quadrado', 640, 337.5, 200, 200),
(13, 'Quadrado', 640, 337.5, 299, 299),
(14, 'Quadrado', 640, 337.5, 200, 200),
(15, 'Quadrado', 640, 337.5, 200, 200),
(16, 'Quadrado', 640, 337.5, 200, 200),
(17, 'Triangulo', 640, 337.5, 200, 200),
(18, 'Triangulo', 640, 337.5, 200, 200);

-- --------------------------------------------------------

--
-- Estrutura para tabela `projeto`
--

CREATE TABLE `projeto` (
  `id_projeto` int(11) NOT NULL,
  `nome_projeto` varchar(45) NOT NULL,
  `canva_altu` float NOT NULL,
  `canva_larg` float NOT NULL,
  `user_projeto` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `cadastro`
--
ALTER TABLE `cadastro`
  ADD PRIMARY KEY (`id_smart`);

--
-- Índices de tabela `objetos`
--
ALTER TABLE `objetos`
  ADD PRIMARY KEY (`id_ob`);

--
-- Índices de tabela `projeto`
--
ALTER TABLE `projeto`
  ADD PRIMARY KEY (`id_projeto`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `cadastro`
--
ALTER TABLE `cadastro`
  MODIFY `id_smart` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de tabela `objetos`
--
ALTER TABLE `objetos`
  MODIFY `id_ob` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de tabela `projeto`
--
ALTER TABLE `projeto`
  MODIFY `id_projeto` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
