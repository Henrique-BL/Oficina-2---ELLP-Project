
# Projeto de Cadastro e Geração de Certificados de Alunos Voluntários

Este projeto tem como objetivo gerenciar o cadastro de alunos voluntários e permitir a geração de certificados para atividades realizadas no projeto de extensão da ELLP da UTFPR. 

## Repositório de Requisitos Funcionais e Scripts de Teste

Os requisitos funcionais e suas respectivas descrições e os roteiros automatizados de teste podem ser encontrados [aqui](https://docs.google.com/document/d/1iE47Ov9iKo7-fqfxT6soyRNzELpT3FdiURancwWl-MQ/edit?usp=sharing).

## Protótipos Front-end
[Figma](https://www.figma.com/design/es0iuy9vC95dO182IFBzVY/projeto-ellp?node-id=0-1&t=B4fgZEXiUSjEUgWz-1).

## Arquitetura do Sistema

A arquitetura deste projeto é baseada em uma abordagem de três camadas principais: **Frontend**, **Backend** e **Banco de Dados**. Abaixo, detalhamos cada um dos componentes e suas tecnologias.
### Backend
![image](https://github.com/user-attachments/assets/2f444b13-af2f-442e-9fe5-d8ad9d860f42)
### Frontend
![image](https://www.plantuml.com/plantuml/png/ZPIn3jCm48PtFyKfIs6es1bGgnPOG4WTodoohyLgScVP3WE8Xq4CdHXvWhmOvw18QPgKPZn__v-x-orlKiQOswOsPWLxEddsx0G40bh9125wjZvW3Lfz5uKpiJDwUC4pGJLKuCM1qEQN5NmteDyATj84OU9R3mGCjRVONRjVqfDsu60RWhaJ9w0Ko7Q_JzvAAaqadp8rE15NEtIOSXHm14UfMyxTp-WbLKlWgmzozbpmhMjqRAsXarWzCluiyPA-IBY3tbFiP-gf7SNijLzqvVS_ZBdPXW9A4rkFZHPwnTkK5JQtXdD8DJKJs7_w24Ul6VxBgCzXx3G-7rAQTL6f8Yp0-9NEPHTJcmBqsWFLPTm_9HxEaK0Is75cq3iQZHJMwpSFqe7Nq2QSWClfJFZvTARGSZe3QHuqg0xBSQWUosRzDpJ_x_rvg_cndjSlJ_oyYLccr6F-Oga-URPHk3ZC8oeUNITLH697KGNGj0wvks8oPgF5yYpz1G00)

### 1. Frontend
- **Tecnologia**: React
- **Principais Funcionalidades**:
  - Cadastro de alunos e consulta de informações.
  - Solicitação e visualização de certificados.
  - Autenticação e navegação entre as diferentes seções do sistema.

### 2. Backend
- **Tecnologia**: FastAPI
- **Principais Funcionalidades**:
  - Endpoints de CRUD para gerenciar o cadastro e as informações dos alunos.
  - Registro e controle de atividades voluntárias.
  - Geração de certificados em PDF com dados do aluno e atividades realizadas.
  - Implementação de autenticação e autorização para controlar o acesso às funcionalidades.

### 3. Banco de Dados
- **Tecnologia**: PostgreSQL com SQLAlchemy
- **Estrutura de Dados**:
  - Tabelas para armazenamento de informações dos alunos, atividades e registros de certificados.
  - Chaves e relacionamentos definidos para vincular atividades aos respectivos alunos.

### Fluxo de Comunicação

1. O **frontend** faz solicitações HTTP ao **backend** através de chamadas para a API REST fornecida pelo FastAPI.
2. O **backend** processa essas solicitações, realizando as operações necessárias no **banco de dados** PostgreSQL via SQLAlchemy.
3. Quando um certificado é solicitado, o backend gera o PDF e armazena as informações no banco de dados, retornando o arquivo gerado ou um link para visualização.

### Gerenciamento de Certificados em PDF

- **Geração**: A geração dos certificados é realizada no backend, utilizando uma biblioteca para criação do PDF.
- **Conteúdo do Certificado**: Cada certificado inclui dados como nome do aluno, atividades realizadas, data e assinatura digital do projeto.

## Resumo das Tecnologias Utilizadas

| Área                | Tecnologia           | Finalidade                                   |
|---------------------|----------------------|----------------------------------------------|
| **Frontend**        | React                | Interface do usuário e navegação             |
| **Backend**         | FastAPI              | API REST para cadastro e geração de certificados |
| **Banco de Dados**  | PostgreSQL, SQLAlchemy | Persistência de dados e manipulação com ORM |
| **Migrations**  | Alembic | Controle de mudanças (migrations) no banco de dados  |
| **Container**  | Docker | Definição de containers, ambientes e imagens utilizadas no projeto  |
| **Geração de PDF**  | ReportLab ou WeasyPrint | Criação de certificados PDF                 |
| **Testes**          | Pytest      | Automação de testes para assegurar qualidade |

## Instalação e Execução

### Pré-requisitos
- Node.js e npm para rodar o frontend em React.
- Python e pip para o backend com FastAPI.
- PostgreSQL para o banco de dados.

### Instruções de Execução
1. Clone este repositório.
2. Instale as dependências necessárias para o frontend e backend.
3. Configure o banco de dados PostgreSQL e as variáveis de ambiente.
4. Inicie o backend e o frontend e acesse o sistema pelo navegador.

