
# Sistema de Gestão de Oficina Automotiva

Este é um sistema web desenvolvido com o framework Flask, projetado para automatizar o gerenciamento de uma oficina automotiva. A aplicação permite o controle de clientes, funcionários, caixa diário, comissões, cálculos de orçamentos e muito mais.

## Funcionalidades

### 1. **Gestão de Clientes**
- **Cadastro de Clientes:** Cadastro de informações dos clientes, como nome, veículo, dados de contato e detalhes do orçamento.
- **Edição de Clientes:** Atualização das informações dos clientes cadastrados.
- **Exclusão de Clientes:** Exclui um cliente da base de dados.
- **Consulta de Clientes:** Permite visualizar todos os clientes ou realizar buscas específicas.

### 2. **Gestão de Funcionários**
- **Cadastro de Funcionários:** Cadastro e edição de informações de funcionários, como nome, cargo e dados de contato.
- **Edição de Funcionários:** Atualização dos dados dos funcionários cadastrados.
- **Exclusão de Funcionários:** Exclui o funcionário escolhido pelo administrador.

### 3. **Comissões**
- **Cálculo de Comissão:** Calcula as comissões devidas aos funcionários com base no número de peças feitas ou serviços prestados.
- **Relatório de Comissões:** Geração de relatórios detalhados sobre as comissões de cada funcionário. O relatório inclui informações como o valor total de comissão de cada funcionário, data e serviços associados, facilitando o acompanhamento e pagamento das comissões devidas.

### 4. **Caixa Diário**
- **Controle do Caixa Diário:** Registra entradas e saídas de dinheiro ao longo do dia, permitindo um controle financeiro completo do movimento diário da oficina.

### 5. **Despesas**
- **Controle de Despesas:** Registra as despesas da oficina, como compras de peças, pagamentos de salários e outros custos operacionais, permitindo que o administrador monitore os gastos e mantenha o controle financeiro.

### 6. **Cálculo de Orçamentos**
- **Cálculo de Orçamento:** O sistema calcula automaticamente o valor final do orçamento para o cliente, levando em consideração os custos de peças, serviços prestados e despesas adicionais. O valor total pode incluir uma margem de lucro definida pelo administrador.

### 7. **Geração de Relatórios**
- **Relatórios de Clientes:** Geração de relatórios sobre os clientes cadastrados e serviços prestados.
- **Relatórios de Despesas:** Geração de relatórios detalhados sobre as despesas da oficina, facilitando o acompanhamento dos custos.
- **Relatórios de Comissões:** Geração de relatórios sobre as comissões de funcionários, incluindo o valor total de comissão de cada funcionário, por serviço ou venda realizada.
- **Relatórios de Orçamentos:** Geração de relatórios sobre os orçamentos realizados, incluindo o cálculo do valor final.
- **Exportação de Relatórios para Excel:** Possibilidade de exportar dados de clientes, serviços, orçamentos, comissões e despesas para arquivos Excel, tornando mais fácil o gerenciamento e análise de dados.

### 8. **Relatórios Personalizados**
- **Exportação de Relatórios em Formatos Diversos:** Além de Excel, a aplicação permite exportar relatórios em formato PDF e CSV.

## Tecnologias Utilizadas

- **Flask:** Framework para desenvolvimento web.
- **MySQL:** Banco de dados para armazenamento das informações.
- **Pandas:** Biblioteca para geração de relatórios e exportação para Excel.
- **HTML / CSS:** Desenvolvimento do front-end da aplicação.

## Como Rodar o Projeto

1. **Clonar o Repositório:**
   ```bash
   git clone <URL_do_repositório>
   cd <nome_da_pasta>
   ```

2. **Instalar Dependências:**
   Crie um ambiente virtual e instale as dependências necessárias:
   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows: venv\Scriptsctivate
   pip install -r requirements.txt
   ```

3. **Configurar Banco de Dados:**
   Garanta que o MySQL esteja rodando e configure a conexão no arquivo `config.py`.

4. **Rodar o Servidor:**
   ```bash
   flask run
   ```

A aplicação estará disponível em [http://localhost:5000](http://localhost:5000).

