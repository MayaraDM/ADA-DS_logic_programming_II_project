# Projeto Módulo II - Sistema de Cadastro de Produtos

# Import e funções para lidar com arquivo:
import json

ARQUIVO_CADASTRO = "cadastro_produtos.json"

def consultar_cadastro() -> list:
    '''Lê o arquivo json onde estão salvos os produtos do cadastro. Retorna uma lista de produtos'''
    try:
        with open(ARQUIVO_CADASTRO, "r") as arquivo:
            cadastro = [produto for produto in json.loads(arquivo.read())['Produtos']]
    # Caso o arquivo não exista
    except FileNotFoundError:
        cadastro = []
    # Caso o arquivo esteja vazio
    except json.decoder.JSONDecodeError:
        cadastro = []
    return cadastro

def atualizar_arquivo_cadastro(nova_lista: list):
    '''Atualiza arquivo json de acordo com a estrutura certa usando os valores
    da lista atualizada recebida como parâmetro.'''
    # Sobrescreve o arquivo json com a nova lista.
    with open(ARQUIVO_CADASTRO, 'w') as arquivo:
        arquivo.write(json.dumps({"Produtos": nova_lista}))
    print("Arquivo atualizado.")
    return


# Levantamento de erros:
def erro_numero(numero):
    if numero < 0:
        raise Exception('O número não pode ser negativo.')
    else:
        return numero

def erro_string(string):
    if len(string) == 0:
        raise Exception('O campo não pode ficar vazio.')
    else:
        return string

# Validação de inputs:
def validar_numero(campo, valor):
    try:
        valor = int(erro_numero(valor))
        return valor
    except ValueError:
        print(f'O {campo} precisa ser um número inteiro.')
    except Exception:
        print(f'O {campo} precisa ser um número inteiro não negativo.')

def validar_string(campo, valor):
    try:
        valor = erro_string(valor)
    except Exception:
        print(f'{campo} não pode ficar vazio.')

# Funções para cadastro e validação dos inputs:
def especificacoes():
    especificacoes = {}
    caracteristica = input('Insira o título da característica ou deixe em branco para encerrar: ').capitalize()
    while caracteristica != '':
        while True:
            valor = validar_string(caracteristica, input(f'Insira a descrição referente a {caracteristica}: '))
            if valor != None:
                break
        especificacoes[caracteristica] = valor
        caracteristica = input('Insira o título da característica ou deixe em branco para encerrar: ').capitalize()
    return especificacoes

def inserir_infos(lista_chaves:list) -> dict: 
    lista_valores = []
    cadastro = consultar_cadastro()
    for chave in lista_chaves:
        if chave == 'ID':
            if cadastro == []:
                valor = 1
            else:
                valor = cadastro[-1]['ID'] + 1
        elif chave == 'Nome':
            while True:
                valor = validar_string(chave, input(f'Informe {chave} do produto: '))
                if valor != None:
                    break
        elif chave == 'Especificações':
            print(f'Informe {chave} do produto: ')
            valor = especificacoes()
        elif chave == 'Estoque':
            while True:
                valor = validar_numero(chave, input(f'Informe {(chave).lower()} do produto: '))
                if valor != None:
                    break
        else:
            valor = input(f'Informe {(chave).lower()} do produto: ')
        lista_valores.append(valor)
        return lista_valores
    
def cadastrar_produto(lista_chaves, lista_valores) -> dict:
    '''Monta um dicionário com os valores inseridos pelo usuário e salva no arquivo do cadastro.
    Retorna o dicionário estruturado'''
    
    produto = {chave:valor for chave, valor in zip(lista_chaves, lista_valores)}

    cadastro = consultar_cadastro()
    # Adiciona o produto à lista de produtos
    cadastro.append(produto)
    # Sobrescreve o arquivo json com a nova lista.
    with open(ARQUIVO_CADASTRO, 'w') as arquivo:
        arquivo.write(json.dumps({"Produtos": cadastro}))

    return produto


#Funções de consulta:
def consultar_produto(produto_id: int) -> dict:
    '''Busca a ID informada pelo usuário entre os registros no arquivo de cadastro. Retorna o dicionário do produto. '''
    cadastro = consultar_cadastro()

    filtro = filter(lambda produto: int(produto['ID']) == produto_id, cadastro)
    produto = list(filtro)
    if produto == []:
        print('Produto não encontrado.') # Assim o return da função já é None (não precisa return None)
    else:
        return produto[0]

def consultar_produto_nome(nome: str) -> dict:
    '''Busca o nome informado pelo usuário entre os registros no arquivo de cadastro. Retorna o dicionário do produto. '''
    cadastro = consultar_cadastro()
    filtro = filter(lambda produto: produto['Nome'].lower() == nome.lower(), cadastro)
    produto = list(filtro)
    if produto == []:
        print('Produto não encontrado.')
    else:
        return produto[0]

# A função pedida era pra listar só o ID e nome do produto, por isso tirei o que tinha a mais, pra simplificar.
def listar_produtos():
    cadastro = consultar_cadastro()
    print('Produtos cadastrados: ')
    for produto in cadastro:
        print(f'ID: {produto["ID"]} | Nome: {produto["Nome"]}', end=' | ')


# Funções de alteração do cadastro:
def menu_atualizar_cadastro(menu:str):
    if menu == '1':
        chave = 'Nome'
        while True:
            valor = validar_string(chave, input(f'Informe o novo {chave}: '))
            if valor != None:
                break
        return chave, valor
    elif menu == '2':
        chave = 'Especificações'
        valor = especificacoes()
        return chave, valor

    elif menu == '3':
        chave = 'Estoque'
        while True:
            valor = validar_numero(chave, input(f'Informe o novo {chave}: '))
            if valor != None:
                break
        return chave, valor

    elif menu == '4':
        chave = 'Descrição'
        while True:
            valor = validar_string(chave, input(f'Informe o novo {chave}: '))
            if valor != None:
                break
        return chave, valor
    else:
        print('Opção inválida, por favor, digite um número de acordo com o menu: ')
    
def atualizar_cadastro_produto(produto_id:int, lista_chaves):
    ''' Altera o valor de um dos campos do produto a ser informado. '''
    produto = consultar_produto(produto_id)
    if produto:
        menu = input('Qual campo deseja atualizar?\n1 - Nome\n2 - Especificações\n3 - Estoque\n4 - Descrição\n')  
        chave, valor = menu_atualizar_cadastro(menu)
        produto[chave] = valor
        
        cadastro = consultar_cadastro()
        for indice, valor in enumerate(cadastro): 
            if valor['ID'] == produto_id:
                cadastro[indice] = produto 
                print('Cadastro atualizado')
        return cadastro 
    else:
        print('Produto não encontrado.')


def excluir_produto(produto_id: int):
    '''Exclui o produto e todos os seus atributos da lista de produtos cadastrados. '''
    lista_produtos = consultar_cadastro()
    produto = consultar_produto(produto_id)

    if produto:
        print(f"{produto['ID']}: {produto['Nome']} | Qtde: {produto['Estoque']} | {produto['Descrição']}")
        excluir = input('Você tem certeza que deseja excluir este cadastro (S/N)?').upper()
        if excluir == 'S':
            for indice, valor in enumerate(lista_produtos):
                if valor == produto:
                    lista_produtos.pop(indice)
                    print('Cadastro excluído')
            return lista_produtos
        else:
            print("Ação cancelada.")
    else:
        print('Produto não encontrado no cadastro.')


# Executável num loop while:
print('Bem vindo ao sistema de cadastro de produtos.\n\n')
print('Informe qual opção deseja executar:\n')

while True:
    opcao = input('1 - Cadastrar produto\n2 - Consultar produto\n3 - Listar produtos cadastrados\n4 - Atualizar cadastro\n5 - Excluir cadastro\n6 - Sair\n')
    
    if opcao == '1':
        lista_chaves = ['ID', 'Nome', 'Especificações', 'Estoque', 'Descrição']
        lista_valores = inserir_infos(lista_chaves)
        cadastrar_produto(lista_chaves, lista_valores)
        print(f"Produto {nome} inserido com sucesso.")

    elif opcao == '2':
        opcao_busca = input('Você deseja consultar o produto por:\n1 - ID\n2 - Nome\nOpção: ').lower()
        
        if opcao_busca == '1' or opcao_busca == 'id':
            while True:
                valor = validar_numero('ID', input('Informe o ID do produto: '))
                if valor != None:
                    break
            produto = consultar_produto(produto_id)
            if produto:
                print(produto)
            else:
                print("Produto não encontrado.")
        
        elif opcao_busca == '2' or opcao_busca == 'nome':
                nome = input('Informe o nome do produto: ')
                print(consultar_produto_nome(nome))
        else:
            print('Opção inválida.')

    elif opcao == '3':
        listar_produtos()

    elif opcao == '4':
        while True:
                produto_id = validar_numero('ID', input('Informe o ID do produto: '))
                if produto_id != None:
                    break
        lista_atualizada = atualizar_cadastro_produto(produto_id)
        print(lista_atualizada)
        atualizar_arquivo_cadastro(lista_atualizada)


    elif opcao == '5':
        while True:
                produto_id = validar_numero('ID', input('Informe o ID do produto: '))
                if produto_id != None:
                    break
        lista_atualizada = excluir_produto(produto_id)
        if lista_atualizada or lista_atualizada == []:
            atualizar_arquivo_cadastro(lista_atualizada)

    elif opcao == '6':
        break

    else:
        print('Opção inválida, por favor, digite um número de acordo com o menu: ')
