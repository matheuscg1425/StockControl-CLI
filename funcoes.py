"""
Módulo com as funções de manipulação de dados do sistema de controle
de estoque. Cada função tem uma responsabilidade única, o que facilita
a leitura, manutenção e reaproveitamento do código.
"""

import json
import os

ARQUIVO_DADOS = "dados.json"


def carregar_dados():
    """Carrega os produtos salvos no arquivo JSON.

    Se o arquivo não existir ou estiver corrompido, retorna uma lista
    vazia em vez de travar o programa.
    """
    if not os.path.exists(ARQUIVO_DADOS):
        return []

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if not conteudo:
                return []
            return json.loads(conteudo)
    except (json.JSONDecodeError, OSError) as erro:
        print(f"Aviso: não foi possível ler o arquivo de dados ({erro}).")
        print("Iniciando com uma lista de produtos vazia.")
        return []


def salvar_dados(produtos):
    """Salva a lista de produtos no arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
        return True
    except OSError as erro:
        print(f"Erro ao salvar os dados: {erro}")
        return False


def gerar_novo_id(produtos):
    """Gera um novo ID sequencial baseado no maior ID já cadastrado."""
    if not produtos:
        return 1
    return max(produto["id"] for produto in produtos) + 1


def ler_texto_nao_vazio(mensagem):
    """Solicita um texto ao usuário e garante que não fique em branco."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Este campo não pode ficar em branco. Tente novamente.")


def ler_numero_inteiro(mensagem):
    """Solicita um número inteiro não negativo, repetindo em caso de erro."""
    while True:
        valor = input(mensagem).strip()
        try:
            numero = int(valor)
            if numero < 0:
                print("Informe um número inteiro igual ou maior que zero.")
                continue
            return numero
        except ValueError:
            print("Valor inválido. Digite um número inteiro, ex: 10")


def ler_numero_decimal(mensagem):
    """Solicita um número decimal não negativo (usado para preços)."""
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            numero = float(valor)
            if numero < 0:
                print("O valor não pode ser negativo.")
                continue
            return round(numero, 2)
        except ValueError:
            print("Valor inválido. Digite um número, ex: 19.90")


def buscar_por_id(produtos, id_produto):
    """Retorna o produto correspondente ao ID informado, ou None."""
    for produto in produtos:
        if produto["id"] == id_produto:
            return produto
    return None


def cadastrar_produto(produtos):
    """Cadastra um novo produto e o adiciona à lista de produtos."""
    print("\n--- Cadastro de novo produto ---")
    nome = ler_texto_nao_vazio("Nome do produto: ")
    categoria = ler_texto_nao_vazio("Categoria: ")
    quantidade = ler_numero_inteiro("Quantidade em estoque: ")
    preco = ler_numero_decimal("Preço unitário (R$): ")
    estoque_minimo = ler_numero_inteiro("Estoque mínimo desejado: ")

    novo_produto = {
        "id": gerar_novo_id(produtos),
        "nome": nome,
        "categoria": categoria,
        "quantidade": quantidade,
        "preco": preco,
        "estoque_minimo": estoque_minimo,
    }

    produtos.append(novo_produto)
    print(f"Produto '{nome}' cadastrado com sucesso! (ID {novo_produto['id']})")


def listar_produtos(produtos):
    """Exibe todos os produtos cadastrados em formato de tabela."""
    print("\n--- Lista de produtos ---")
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return

    cabecalho = f"{'ID':<4}{'Nome':<20}{'Categoria':<15}{'Qtd':<6}{'Preço':<10}{'Status':<14}"
    print(cabecalho)
    print("-" * len(cabecalho))

    for produto in produtos:
        estoque_baixo = produto["quantidade"] <= produto["estoque_minimo"]
        status = "ESTOQUE BAIXO" if estoque_baixo else "OK"
        nome_exibido = produto["nome"][:18]
        categoria_exibida = produto["categoria"][:13]
        linha = (
            f"{produto['id']:<4}"
            f"{nome_exibido:<20}"
            f"{categoria_exibida:<15}"
            f"{produto['quantidade']:<6}"
            f"R${produto['preco']:<8.2f}"
            f"{status:<14}"
        )
        print(linha)


def exibir_produto(produto):
    """Exibe os detalhes de um único produto."""
    print(f"ID: {produto['id']}")
    print(f"Nome: {produto['nome']}")
    print(f"Categoria: {produto['categoria']}")
    print(f"Quantidade: {produto['quantidade']}")
    print(f"Preço unitário: R${produto['preco']:.2f}")
    print(f"Estoque mínimo: {produto['estoque_minimo']}")


def buscar_produto(produtos):
    """Busca produtos pelo nome (busca parcial, sem diferenciar caixa)."""
    print("\n--- Buscar produto ---")
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return

    termo = ler_texto_nao_vazio("Digite o nome (ou parte dele) para buscar: ")
    encontrados = [p for p in produtos if termo.lower() in p["nome"].lower()]

    if not encontrados:
        print("Nenhum produto encontrado com esse nome.")
        return

    print(f"\n{len(encontrados)} produto(s) encontrado(s):\n")
    for produto in encontrados:
        exibir_produto(produto)
        print("-" * 30)


def editar_produto(produtos):
    """Edita os dados de um produto existente, identificado pelo ID."""
    print("\n--- Editar produto ---")
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return

    id_produto = ler_numero_inteiro("Digite o ID do produto que deseja editar: ")
    produto = buscar_por_id(produtos, id_produto)

    if not produto:
        print("Produto não encontrado.")
        return

    print("Produto atual:")
    exibir_produto(produto)
    print("\nDigite os novos dados (deixe em branco para manter o valor atual).\n")

    novo_nome = input(f"Novo nome [{produto['nome']}]: ").strip()
    if novo_nome:
        produto["nome"] = novo_nome

    nova_categoria = input(f"Nova categoria [{produto['categoria']}]: ").strip()
    if nova_categoria:
        produto["categoria"] = nova_categoria

    nova_quantidade = input(f"Nova quantidade [{produto['quantidade']}]: ").strip()
    if nova_quantidade:
        if nova_quantidade.isdigit():
            produto["quantidade"] = int(nova_quantidade)
        else:
            print("Quantidade inválida, valor mantido.")

    novo_preco = input(f"Novo preço [{produto['preco']:.2f}]: ").strip().replace(",", ".")
    if novo_preco:
        try:
            produto["preco"] = round(float(novo_preco), 2)
        except ValueError:
            print("Preço inválido, valor mantido.")

    novo_minimo = input(f"Novo estoque mínimo [{produto['estoque_minimo']}]: ").strip()
    if novo_minimo:
        if novo_minimo.isdigit():
            produto["estoque_minimo"] = int(novo_minimo)
        else:
            print("Valor inválido, estoque mínimo mantido.")

    print("Produto atualizado com sucesso!")


def excluir_produto(produtos):
    """Remove um produto da lista, após confirmação do usuário."""
    print("\n--- Excluir produto ---")
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return

    id_produto = ler_numero_inteiro("Digite o ID do produto que deseja excluir: ")
    produto = buscar_por_id(produtos, id_produto)

    if not produto:
        print("Produto não encontrado.")
        return

    exibir_produto(produto)
    confirmacao = input("Tem certeza que deseja excluir este produto? (s/n): ").strip().lower()

    if confirmacao == "s":
        produtos.remove(produto)
        print("Produto excluído com sucesso!")
    else:
        print("Operação cancelada.")
