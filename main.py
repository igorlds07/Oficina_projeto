import os

from flask import Flask, render_template, request, redirect, url_for, flash

from datetime import datetime

from BD import conexao_bd

# Nome da aplicação
app = Flask(__name__)
app.secret_key = os.urandom(24)


# fazer uma função de login e senha para adms do programa(dono da oficina)
@app.route('/', methods=['GET', 'POST'])
def login_user():
    """ Função que verifica as credenciais de login do administrador.
    Esta função autentica o usuário verificando as informações no banco de dados.
    Caso o login e senha estejam corretos, o usuário será redirecionado para a página principal."""

    error = None
    mensagem = None

    # Condição para ver se o usuário tem acesso ao app
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        conexao_bd()

        conexao = conexao_bd()
        cursor = conexao.cursor()

        # Executa o comando SQL para buscar os parâmetros indicados no login e senha
        cursor.execute('SELECT senha from administradores WHERE login = %s', (login,))

        usuario = cursor.fetchone()
        cursor.close()
        conexao.close()

        if usuario is None:
            error = 'Administrador não cadastrado!'  # Se não encontrado e emetido esta mensagem
        else:
            senha_bd = usuario[0]  # Verificação de senha
            if senha != senha_bd:
                error = 'Senha incorreta!'  # Se incorreta emeti está mensagem

        if error:
            return render_template('login.html', error=error, mensagem=mensagem)  # Passando a mensagem de erro para
            # o template

        mensagem = 'Acesso liberado'

        if mensagem:

            return redirect(url_for('index'))

    return render_template('login.html', mensagem=mensagem)


# Rota para exibir o formulário de cadastro
@app.route('/cadastro')
def index():
    """ Função que renderiza a página de cadastro de clientes.
    Exibe um formulário onde o usuário pode preencher as informações de um novo cliente."""

    return render_template('index.html')


# Rota para cadastrar um novo cliente
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    """ Função que cadastra um novo cliente no banco de dados.
    Recebe os dados preenchidos pelo usuário, insere-os na tabela 'clientes' e exibe uma mensagem de sucesso."""
    if request.method == 'POST':
        nome = request.form['nome']
        contato = request.form['contato']
        veiculo = request.form['veiculo']
        data_entrada = request.form['data_entrada']
        data_saida = request.form['data_saida']
        valor_orcamento1 = request.form['valor_orcamento']
        valor_orcamento = float(valor_orcamento1)

        # CREAT
        conexao = conexao_bd()
        cursor = conexao.cursor()
        comando = (f'INSERT INTO clientes (nome, contato, veiculo, data_entrada, data_saida, valor_orcamento) '
                   f'VALUES (%s, %s, %s, %s, %s, %s);')
        cursor.execute(comando, (nome, contato, veiculo, data_entrada, data_saida, valor_orcamento))
        conexao.commit()

        cursor.close()
        conexao.close()

        message = 'Cadastrado com sucesso!'
        sucess_mesagge = 'Cadastrado com sucesso'
        print(sucess_mesagge)

        # Ao clicar o botão cadastrar e emetido a mensagem de 'sucesso' e  retorna a  página de cadastro
        return render_template('index.html', message=message)

    return render_template('index.html')  # Ao finalizar o processo retorna a página de cadastro novamente


# Rota para editar os clientes já cadastrados no BANCO DE DADOS
@app.route('/editar', methods=['GET', 'POST'])
def editar_cliente():
    """  Função para editar as informações de um cliente já cadastrado.
    Recebe o nome do cliente, busca os dados no banco de dados e permite ao administrador atualizar as informações."""

    cliente = None
    error = []
    conexao = conexao_bd()  # Chama a função para obter a conexão  com o Banco de dados

    # condição para atualizar o cliente
    if request.method == 'POST':
        cliente = request.form['cliente']
        nome = request.form['nome']
        contato = request.form['contato']
        veiculo = request.form['veiculo']
        data_entrada = request.form['data_entrada']
        data_saida = request.form['data_saida']
        valor_orcamentos = request.form['valor_orcamento']
        valor_orcamento = float(valor_orcamentos)

        # Condição para verificar se houve conexão com o banco de dados
        if conexao is None:
            return render_template('editar.html', error=['Erro na conexão com o banco de dados.'])

        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM clientes WHERE nome = %s", (cliente,))

        cliente_existente = cursor.fetchone()
        print(cliente_existente)
        # UPDATE
        if cliente_existente:

            # Comando em SQL para atualizar o cliente escolhido
            cursor.execute("""UPDATE clientes SET nome = %s, contato = %s, veiculo = %s, data_entrada = %s,
                          data_saida = %s, valor_orcamento = %s WHERE nome = %s""",
                           (nome, contato, veiculo, data_entrada, data_saida, valor_orcamento, cliente))
            conexao.commit()

            cursor.close()
            conexao.close()  # Fecha a conexão com o  banco de dados

            flash('Cliente atualizado com sucesso!', 'success')  # Mensagem de sucesso com flash
            return redirect(url_for('editar_cliente'))  # Redireciona para o formulário de edição novamente

        else:
            cursor.close()  # Fechar o cursor se o cliente não for encontrado

            conexao.close()  # Fechar a conexão

            flash('Cliente não encontrado!', 'error')  # Mensagem de erro com flash

            return redirect(url_for('editar_cliente'))  # Redi

    return render_template('editar.html', cliente=None)  # Retorna a página e edição de clientes


# Rota para excluir clientes no banco de dados
@app.route('/excluir_cliente', methods=['GET', 'POST'])
def excluir_cliente():
    """  Função para excluir um cliente do banco de dados.
    O cliente é excluído após uma confirmação do administrador."""

    conexao = conexao_bd()
    cliente = None

    # Condição para verificar se existe o cliente específicado no banco de dados
    if request.method == 'POST':
        nome_cliente = request.form['nome']
        print(f"Nome do cliente enviado: {nome_cliente}")
        print(f"Dados do formulário: {request.form}")

        # Se o cliente for encontrado executa a exclusão
        if nome_cliente:
            cursor = conexao.cursor()

            # DELETE
            cursor.execute('SELECT * FROM clientes WHERE nome = %s;', (nome_cliente,))
            cliente = cursor.fetchone()
            print(cliente)

            # Condição para verificar se o usuário deseja confirmar o delete
            if cliente:
                if request.form.get('confirmar') == 'sim':
                    print('botão pressionado')

                    cursor = conexao.cursor()
                    # Comando em SQL para deletar o cliente
                    comando = f'DELETE FROM clientes WHERE nome = "{nome_cliente}"'
                    cursor.execute(comando)
                    print(f'excluindo cliente {nome_cliente}')

                    conexao.commit()
                    print(f'cliente excluido com  successo')
                    flash(f'Cliente {nome_cliente} excluído com sucesso!', 'success')
                    return render_template('excluir_cliente.html', cliente=None)  # Redireciona após exclusão

            else:
                flash('Cliente não encontrado!', 'error')

        else:
            flash('Por favor, informe o nome do cliente.', 'warning')  # Senão for passado
            # o nome para busca retorna esta mensagem

            return redirect(url_for('excluir_cliente'))

    return render_template('excluir_cliente.html', cliente=cliente)  # Após o procedimento retorna a
    # página excluir_cliente


# Rota para mostrar todos os clientes e algum cliente específico
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    """Função para buscar clientes no banco de dados.
    Permite buscar por nome ou exibir todos os clientes cadastrados."""

    conexao = conexao_bd()  # Conexão com o banco de dados
    cursor = conexao.cursor()

    cliente_cadastrado = []

    if request.method == 'POST':

        nome = request.form['nome']
        if nome:

            # READ
            # Comando em SQL para buscar o cliente específicado
            comando = 'SELECT  * FROM clientes WHERE nome = %s;'
            cursor.execute(comando, (nome,))

            cliente_cadastrado = cursor.fetchall()
            print(cliente_cadastrado)

        # Condição para verificar se o cliente foi encontrado
        if not cliente_cadastrado:
            cliente_cadastrado = ['Cliente não encontrado']

    # Condição para vereificar se o usuário deseja ver todos os clientes
    if request.method == 'GET' and 'ver_todos' in request.args:

        # Comando em SQL para buscar todos os clientes
        comando = 'SELECT * FROM clientes;'
        cursor.execute(comando)

        cliente_cadastrado = cursor.fetchall()
    cursor.close()
    conexao.close()  # A conexão com o banco de dados é finalizada

    # Após todas as buscas retorna a página clientes.html
    return render_template('clientes.html', clientes=cliente_cadastrado)


@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    conexao = conexao_bd()
    cursor = conexao.cursor()

    funcionario = []

    if request.method == 'GET' and 'ver_todos' in request.args:
        comando = 'SELECT * FROM funcionários;'
        cursor.execute(comando,)
        funcionario = cursor.fetchall()
        print(funcionario)

        return render_template('funcionarios.html', funcionarios=funcionario)

    if request.method == 'POST':
        nome = request.form['nome']
        contato = request.form['contato']
        cargo = request.form['cargo']

        # Verifica se já existe um funcionário com esse nome (ou outro identificador)
        comando = "INSERT INTO funcionários (nome, contato, cargo) VALUES (%s, %s, %s);"
        cursor.execute(comando, (nome, contato, cargo))
        conexao.commit()
        flash('Funcionário cadastrado com sucesso !', 'success')
        funcionarios_cadastrados = cursor.fetchall()

        return render_template('funcionarios.html', funcionarios=funcionarios_cadastrados)

    return render_template('funcionarios.html')


@app.route('/funcionarios_atualizar', methods=['GET', 'POST'])
def funcionarios_atualizar():
    conexao = conexao_bd()
    cursor = conexao.cursor()
    funcionario = None

    if request.method == 'POST':

        nome_funcionario = request.form.get('nome')

        cursor.execute('SELECT * FROM funcionários WHERE nome = %s;', (nome_funcionario,))
        funcionario_escolhido = cursor.fetchall()

        if funcionario_escolhido:
            funcionario_escolhido = funcionario_escolhido[0]

            # Obter os valores do formulário
            total_pecas = request.form.get('total_peças', 0)  # Valor padrão de 0 caso não seja enviado
            valor_comissao = request.form.get('valor_comissão', 0)  # Valor padrão de 0 caso não seja enviado

            # Recuperar os valores do banco de dados e substituir None por 0
            total_pecas_db = funcionario_escolhido[0][5] if funcionario_escolhido[0][5] is not None else 0
            valor_comissao_db = funcionario_escolhido[0][6] if funcionario_escolhido[0][6] is not None else 0

            # Somar os valores antigos com os novos
            novo_total_pecas = total_pecas_db + int(total_pecas)  # Soma de total_peças
            novo_valor_comissao = valor_comissao_db + float(valor_comissao)  # Soma de valor_comissão

            # Atualiza o banco de dados com os valores acumulados
            comando = """UPDATE funcionários 
                                               SET total_peças = %s, valor_comissão = %s 
                                               WHERE nome = %s;"""
            cursor.execute(comando, (novo_total_pecas, novo_valor_comissao, funcionario_escolhido[0][0]))
            conexao.commit()
            conexao.close()
            flash('Valores adicionados com sucesso!', 'sucess')

            return render_template('funcionarios_atualizar.html', funcionario=funcionario_escolhido)

        else:
            flash('Funcionário não encontrado!', 'error')

    return render_template('funcionarios_atualizar.html', funcionario=funcionario)


@app.route('/excluir_funcionario', methods=['GET', 'POST'])
def excluir_funcionario():
    conexao = conexao_bd()
    cursor = conexao.cursor()
    funcionario = None
    if request.method == 'POST':
        nome = request.form.get('nome')

        if nome:
            cursor.execute('SELECT * FROM funcionários WHERE nome = %s;', (nome,))
            funcionario = cursor.fetchone()

            if funcionario:
                if request.form.get('confirmar') == 'sim':
                    print('botão pressionado')

                    cursor = conexao.cursor()
                    # Comando em SQL para deletar o cliente
                    cursor.execute(f'DELETE FROM clientes WHERE nome = "{funcionario}";')
                    print(f'excluindo cliente {funcionario}')

                    conexao.commit()
                    print(f'cliente excluido com  successo')
                    flash(f'Funcionário {funcionario[1]} excluído com sucesso!', 'success')
                    return render_template('excluir_funcionario.html', funcionario=None)  # Redireciona após exclusão

            else:
                flash('Funcionário não encontrado!', 'error')

        else:
            flash('Por favor, informe o nome do cliente.', 'warning')  # Senão for passado
            return redirect(url_for('excluir_funcionario'))

    return render_template('excluir_funcionario.html', funcionario=funcionario)


@app.route('/editar_funcionario', methods=['GET', 'POST'])
def editar_funcionario():
    conexao = conexao_bd()
    cursor = conexao.cursor()
    funcionario = None
    error = None

    if request.method == 'POST':
        funcionaro_nome = request.form['nome_funcionario']
        nome = request.form['nome']
        contato = request.form['contato']
        cargo = request.form['cargo']

        cursor.execute('SELECT * FROM funcionários WHERE nome = %s;', (funcionaro_nome,))
        funcionario = cursor.fetchone()
        print(funcionario)

        if funcionario:
            cursor.execute("""UPDATE funcionários SET nome = %s, contato = %s, cargo = %s, WHERE nome = %s""",
                           (nome, contato, cargo, funcionario))
            conexao.commit()

            cursor.close()
            conexao.close()  # Fecha a conexão com o  banco de dados

            flash('Funcionário atualizado com sucesso!', 'success')  # Mensagem de sucesso com flash
            return redirect(url_for('editar_funcionario'))  # Redireciona para o formulário de edição novamente

        else:
            flash('Funcionário não encontrado !', 'error')
            conexao.close()
            cursor.close()
            return redirect(url_for('editar_funcionario'))

    return render_template('editar_funcionario.html', funcionario=None)


@app.route('/relatorio_orcamentos', methods=['GET', 'POST'])
def relatorio_orcamentos():
    conexao = conexao_bd()
    cursor = conexao.cursor()
    resultados = None

    if request.method == 'POST':
        data_inicio = request.form['data_entrada']
        data_fim = request.form['data_saida']

        if data_inicio and data_fim:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

            if data_inicio > data_fim:
                flash('A data de inicío não pode ser maior que a data de fim!', 'error')
                return render_template(
                    'relatorio_orcamentos.html',)

        # Consulta SQL para buscar orçamentos no período
        query = """
            SELECT idclientes, nome, contato, veiculo, data_entrada, data_saida, valor_orcamento
            FROM clientes
            WHERE data_entrada BETWEEN %s AND %s
        """
        cursor.execute(query, (data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')))
        resultados = cursor.fetchall()
        total = 0
        for cliente in resultados:
            total += 1
        message = f'Foram realizados {total} orçamentos !'

        conexao.close()
        cursor.close()

        return render_template('relatorio_orcamentos.html', resultados=resultados, message=message)

    return render_template('relatorio_orcamentos.html', resultados=resultados)


@app.route('/relatorio_despesas', methods=['GET', 'POST'])
def relatorio_despesas():
    conexao = conexao_bd()
    cursor = conexao.cursor()

    despesas = None

    if request.method == 'POST':
        data_inicio = request.form['data']
        data_fim = request.form['data']

        if data_fim < data_inicio:
            flash('A data do fim não pode ser menor que a data de inicío!', 'error')
            return render_template('relattorio_depsesas')



@app.route('/despesas', methods=['GET', 'POST'])
def despesas():
    conexao = conexao_bd()
    cursor = conexao.cursor()

    despesa = None

    if request.method == 'POST':
        descricao = request.form['descrição']
        data = request.form['data']
        valor = request.form['valor']

        cursor.execute('INSERT INTO despesas(descrição, data, valor)'
                       'VALUES(%s, %s,%s);', (descricao, data, valor))

        conexao.commit()
        conexao.close()
        cursor.close()
        print(f'Despesas foram inseridas {descricao} , {data}, {valor} ')
        flash('Despesas acrescentadas com sucesso!', 'sucess')

        return render_template('despesas.html')

    return render_template('despesas.html')




# Condição para verificar se o projeto esta sendo executado diretamente
if __name__ == '__main__':
    app.run(debug=True)
