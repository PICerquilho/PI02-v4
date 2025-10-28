
---

# Painel de Cadastro e Pesquisa de Alunos

Este é um sistema de gerenciamento escolar desenvolvido com Django, focado em facilitar o cadastro, organização e acesso às informações dos alunos de forma eficiente e segura.

## Dependências
*   Python 3
*   Django
*   Pillow

## Como Instalar
1.  **Instale o Python 3**: Se você ainda não tem o Python instalado, faça o download e a instalação através do site oficial: [python.org](https://www.python.org/).
2.  **Instale o Pip**: O Pip geralmente vem junto com o Python 3. Para verificar, abra seu terminal e digite `pip --version`.
3.  **Clone o Repositório**:
    ```bash
    git clone https://github.com/PICerquilho/PI02-v4.git
    cd PI02-v4
    ```
4.  **Instale o Django**: No terminal (ou no terminal integrado do Visual Studio Code, se estiver usando), navegue até a pasta do projeto clonado e execute o seguinte comando:
    ```bash
    python3 -m pip install Django
    ```
    *Observação: O comando `django-admin` é para criar um novo projeto Django. Para instalar a biblioteca, use `pip install Django` ou `python3 -m pip install Django`.*
5.  **Instale o Pillow**: No mesmo terminal, instale a biblioteca Pillow:
    ```bash
    python3 -m pip install Pillow
    ```
6.  **Configurar Banco de Dados (Migrações)**:
    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```
7.  **Crie um Superusuário (Opcional, mas Recomendado)**: Para acessar a área administrativa:
    ```bash
    python3 manage.py createsuperuser
    ```

## Como Executar
1.  Acesse o diretório do projeto onde o arquivo `manage.py` está localizado.
2.  Execute o comando para iniciar o servidor de desenvolvimento:
    ```bash
    python3 manage.py runserver
    ```
3.  Abra seu navegador e acesse `http://127.0.0.1:8000/`.

## Funcionalidades
*   **📥 Cadastro de alunos** com nome, contato, documento, responsável, endereço, observações, série, turma e período.
*   **🖼️ Upload obrigatório de foto** no cadastro.
*   **✏️ Edição e visualização** de informações com interface clara.
*   **🔍 Busca avançada** com filtros dinâmicos.
*   **🔐 Controle de acesso** por permissões (add, edit, delete).
*   **📂 Organização** por série, turma e período.
*   **🌐 Interface responsiva e moderna**.

---

