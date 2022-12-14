# Projeto Módulo II - Sistema de Cadastro de Produtos

# Import e função para lidar com arquivo:
import json

ARQUIVO_ESTOQUE = "itens_estoque.json"

def consultar_estoque() -> list:
    '''Lê o arquivo json onde estão salvos os produtos do estoque. Retorna uma lista de produtos'''
    try:
        with open(ARQUIVO_ESTOQUE, "r") as arquivo:
            estoque = [produto for produto in json.loads(arquivo.read())['Produtos']]
    # Caso o arquivo não exista
    except FileNotFoundError:
        estoque = []
    # Caso o arquivo esteja vazio
    except json.decoder.JSONDecodeError:
        estoque = []
    return estoque


# Funções para cadastro e validação dos inputs:
def especificacoes():
    especificacoes = {}
    caracteristica = input('Insira o título da característica ou deixe em branco para encerrar: ').capitalize()
    while caracteristica != '':
        valor = input(f'Insira a descrição referente a {caracteristica}: ')
        especificacoes[caracteristica] = valor
        caracteristica = input('Insira o título da característica ou deixe em branco para encerrar: ').capitalize()
    return especificacoes

def cadastrar_produto(nome:str, quantidade: int, descricao:str) -> dict:
    '''Monta um dicionário com os valores inseridos pelo usuário e salva no arquivo do estoque.
    Retorna o dicionário estruturado'''
    produto = {}
    if len(estoque) == 0:
        produto_id = 1
    else:
        produto_id = produto_id[-1['id']] + 1
    produto['nome'] = nome
    produto['especificações'] = especificacoes()
    produto['quantidade'] = quantidade
    produto['descrição'] = descricao

    estoque = consultar_estoque()
    # Adiciona o produto à lista de produtos
    estoque.append(produto)
    # Sobrescreve o arquivo json com a nova lista.
    with open(ARQUIVO_ESTOQUE, 'w') as arquivo:
        arquivo.write(json.dumps({"Produtos": estoque}))

    return produto

def validar_informacao(campo, valor):
    '''Valida a informação inserida pelo usuário, com condições específicas para cada campo.'''
    pass


#Funções de consulta:
def consultar_produto(produto_id: int) -> dict:
    '''Busca a ID informada pelo usuário entre os registros no arquivo do estoque. Retorna o dicionário do produto. '''
    estoque = consultar_estoque()

    filtro = (produto for produto in estoque if produto['id'] == produto_id)
    produto = list(filtro)
    if produto == []:
        print('Produto não encontrado.') # Assim o return da função já é None (não precisa return None)
    else:
        return produto[0]

def consultar_produto_nome(nome: str) -> dict:
    '''Busca o nome informado pelo usuário entre os registros no arquivo do estoque. Retorna o dicionário do produto. '''
    estoque = consultar_estoque()
    filtro = (produto for produto in estoque if produto['nome'] == nome)
    produto = list(filtro)
    if produto == []:
        print('Produto não encontrado.')
    else:
        return produto[0]

# A função pedida era pra listar só o ID e nome do produto, por isso tirei o que tinha a mais, pra simplificar.
def listar_produtos():
    estoque = consultar_estoque()
    print('Produtos cadastrados: ')
    for produto in estoque:
        print(f'ID: {produto["id"]} | Nome: {produto["nome"]}', end=' | ')


# Funções de alteração do cadastro:
def atualizar_cadastro(produto_id:int):
    ''' Altera o valor de um dos campos do produto a ser informado. '''
    produto = consultar_produto(produto_id) #troquei o for da funçao que estava no collab pela funçao de consultar que já existia
    if produto:
        campo_atualizacao = input('Informe o campo a ser atualizado: ')
        produto[campo_atualizacao] = input(f'Informe o novo {campo_atualizacao}: ')
        estoque = consultar_estoque()
        for indice, valor in enumerate(estoque): #percorrendo o estoque todo para encontrar o id selecionado
            if valor['id'] == produto_id:#quando encontra o id selecionado
                estoque[indice] = produto #atualiza o produto na lista
                print('Cadastro atualizado')
        return estoque #retorna a lista de produtos atualizada
    else:
        print('Produto não encontrado.')


def atualizar_arquivo_estoque(nova_lista: list):
    '''Atualiza arquivo json de acordo com a estrutura certa usando os valores
    da lista atualizada recebida como parâmetro.'''
    # Sobrescreve o arquivo json com a nova lista.
    with open(ARQUIVO_ESTOQUE, 'w') as arquivo:
        arquivo.write(json.dumps({"Produtos": nova_lista}))
    print("Arquivo atualizado.")
    return


def excluir_cadastro(produto_id: int):
    '''Exclui o produto e todos os seus atributos da lista de produtos cadastrados. '''
    lista_produtos = consultar_estoque()
    produto = consultar_produto(produto_id)

    if produto:
        print(f"{produto['id']}: {produto['nome']} | Qtde: {produto['quantidade']} | {produto['descrição']}")
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
        id = input('Digite o numero de identificação do produto:')
        nome = input('Digite o nome do produto:')
        especificacoes = {}
        while True:
            caracteristica = input('Insira o título da característica ou deixe em branco para encerrar: ').capitalize()
            if caracteristica:
                valor = input(f'Insira a descrição referente a {caracteristica}: ')
                especificacoes[caracteristica] = valor
            else:
                break
        try:
            quantidade = int(input('Digite a quantidade de produto em estoque:'))
        except TypeError:
            print('A quantidade deve ser um valor numérico.')
        descritivo = input('Coloque aqui um texto descritivo do produto cadastrado:')
        cadastrar_produto(id, nome, quantidade, descritivo, **especificacoes)
        print(f"Produto {nome} inserido com sucesso.")

    elif opcao == '2':
        # Achei legal criar uma opção aqui dentro pra procurar um id se a pessoa não souber, pelo nome do produto.
        opcao_busca = input('Você deseja consultar o produto por:\n1 - ID\n2 - Nome\nOpção: ').lower()
        if opcao_busca == '1' or opcao_busca == 'id':
            try:
                produto_id = int(input('Informe o ID do produto: '))
                produto = consultar_produto(produto_id)
                if produto:
                    print(produto)
                else:
                    print("Produto não encontrado.")
            except ValueError:
                print("O valor da ID deve ser numérico.")
        elif opcao_busca == '2' or opcao_busca == 'nome':
            try:
                nome = input('Informe o nome do produto: ')
                print(consultar_produto_nome(nome))
            except:
                print('Erro')

    elif opcao == '3':
        listar_produtos()

    elif opcao == '4':
        try:
            produto_id = int(input('Informe o ID do produto: '))
        except ValueError:
            print("O valor da ID deve ser numérico.")
        except:
            print('Erro')
        lista_atualizada = atualizar_cadastro(produto_id)
        print(lista_atualizada)
        atualizar_arquivo_estoque(lista_atualizada)


    elif opcao == '5':
        try:
            produto_id = int(input('Informe o ID do produto: '))
        except ValueError:
            print("O valor da ID deve ser numérico.")
        except:
            print('Erro')
        lista_atualizada = excluir_cadastro(produto_id)
        if lista_atualizada or lista_atualizada == []:
            atualizar_arquivo_estoque(lista_atualizada)

    elif opcao == '6':
        break

    else:
        print('Opção inválida, por favor, digite um número de acordo com o menu: ')
