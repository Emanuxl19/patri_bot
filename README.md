# PatriBot - Bot de Gestão de Patrimônio para Telegram

Um bot para Telegram, desenvolvido em Python, para gerir e controlar ativos de patrimônio de uma empresa. Permite adicionar, consultar, atualizar, remover e exportar informações sobre equipamentos de forma simples e rápida.

## ✨ Funcionalidades

* **Adicionar Patrimônio (`/add`):** Inicia uma conversa para cadastrar um novo ativo, passo a passo.
* **Consultar Patrimônio (`/search`):** Busca por um ativo específico usando o número de patrimônio ou lista todos os ativos de um determinado usuário.
* **Atualizar Patrimônio (`/update`):** Permite alterar informações de um ativo já cadastrado.
* **Remover Patrimônio (`/remove`):** Apaga um ativo do banco de dados de forma permanente.
* **Desvincular Usuário (`/unlink_user`):** Remove a associação de um usuário a um ativo, sem apagar o ativo.
* **Exportar para Excel (`/export`):** Gera e envia uma planilha `.xlsx` com todos os ativos cadastrados.
* **Cancelar Operação (`/cancel`):** Interrompe qualquer operação em andamento (como um cadastro).
* **Ajuda (`/ajuda`):** Exibe uma lista com todos os comandos disponíveis.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **python-telegram-bot:** Framework para a criação do bot.
* **Microsoft Azure SQL Database:** Banco de dados relacional na nuvem para persistência dos dados.
* **pyodbc:** Driver de conexão para o banco de dados SQL Server.
* **pandas & openpyxl:** Bibliotecas para a geração de relatórios em Excel.

## 🚀 Configuração do Ambiente

Siga os passos abaixo para executar o projeto localmente.

**Pré-requisitos:**
* Python 3.8 ou superior
* Uma conta no Microsoft Azure
* Um token de bot do Telegram (obtido com o @BotFather)

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Emanuxl19/patri_bot.git](https://github.com/Emanuxl19/patri_bot.git)
    cd patri_bot
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements
    ```

4.  **Configure o Banco de Dados:**
    * Crie um recurso "SQL Database" no portal do Microsoft Azure.
    * Certifique-se de configurar as regras de firewall para permitir o acesso do seu IP.

5.  **Configure as Variáveis de Ambiente:**
    * Crie uma cópia do ficheiro `config.py.example` e renomeie-a para `config.py`.
    * Abra o `config.py` e preencha com as suas credenciais:
        * `TELEGRAM_TOKEN`: O token do seu bot do Telegram.
        * `SQL_SERVER_CONNECTION`: A string de conexão do seu banco de dados Azure.

6.  **Execute o bot:**
    ```bash
    python -m bot.main
    ```

## 💬 Como Usar

Após executar o bot, abra o seu cliente Telegram, encontre o seu bot e utilize os comandos listados na secção de funcionalidades. Comece com `/ajuda` para ver todas as opções.
