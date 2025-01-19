# Sistema de Gestão de Oficina Automotiva

Este projeto é uma aplicação web desenvolvida com o framework Flask. A aplicação tem como objetivo gerenciar clientes de uma oficina automotiva, permitindo funcionalidades como cadastro, edição, exclusão e consulta de clientes, além de um sistema de login para administradores.

## Funcionalidades

- **Login de Administrador:** Apenas administradores (donos da oficina) podem acessar as funcionalidades de gerenciamento.
- **Cadastro de Clientes:** Permite cadastrar informações como nome, contato, veículo, data de entrada e saída, e valor do orçamento.
- **Edição de Clientes:** O administrador pode atualizar as informações de clientes já cadastrados.
- **Exclusão de Clientes:** O administrador pode excluir registros de clientes do banco de dados.
- **Visualização de Clientes:** Permite consultar clientes cadastrados e exibir todos os clientes ou um cliente específico.
- **Cadastro e Edição de Funcionários:** O administrador pode cadastrar e editar informações de funcionários, como nome, cargo e dados de contato.
- **Geração de Relatórios:** O administrador pode gerar relatórios de clientes cadastrados e serviços prestados.

## Tecnologias Utilizadas

- **Flask:** Framework web utilizado para a construção da aplicação.
- **MySQL:** Sistema de gerenciamento de banco de dados utilizado para armazenar as informações dos clientes e funcionários.
- **HTML / Jinja2:** Para renderizar as páginas da aplicação web.
- **CSS:** Para o estilo visual da aplicação.

## Estrutura do Projeto

A aplicação possui as seguintes funcionalidades principais:

1. **Login de Administrador:**
   - Rota: `/`
   - Verifica o login e senha do administrador, autenticando o acesso ao sistema.

2. **Cadastro de Clientes:**
   - Rota: `/cadastro`
   - Permite o cadastro de novos clientes no banco de dados.
   - O formulário coleta informações como nome, contato, veículo, data de entrada, data de saída e valor do orçamento.

3. **Edição de Clientes:**
   - Rota: `/editar/<int:id>`
   - Permite editar os dados de um cliente já cadastrado.

4. **Exclusão de Clientes:**
   - Rota: `/excluir_cliente/<int:id>`
   - Permite excluir um cliente do banco de dados, após confirmação do administrador.

5. **Consulta de Clientes:**
   - Rota: `/clientes`
   - Permite visualizar todos os clientes cadastrados ou buscar um cliente específico pelo nome.

6. **Cadastro de Funcionários:**
   - Rota: `/cadastro_funcionario`
   - Permite cadastrar novos funcionários, com informações como nome, cargo e dados de contato.

7. **Edição de Funcionários:**
   - Rota: `/editar_funcionario/<int:id>`
   - Permite editar as informações de um funcionário já cadastrado.

8. **Relatórios:**
   - Rota: `/relatorios`
   - Permite gerar relatórios sobre os clientes cadastrados e os serviços prestados, com a possibilidade de exportar os dados em formato PDF ou CSV.


