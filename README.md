# 📦 StockControl CLI — Sistema de Controle de Estoque

Sistema de linha de comando (CLI) desenvolvido em **Python puro**, sem
dependências externas, para gerenciar o estoque de produtos de um pequeno
comércio: cadastro, listagem, busca, edição e exclusão de itens, com
persistência dos dados em arquivo JSON.

## 💡 Problema que o projeto resolve

Pequenos comerciantes e microempreendedores frequentemente controlam seu
estoque em cadernos ou planilhas soltas, o que dificulta saber rapidamente
**o que precisa ser reposto** e **qual o valor total em estoque**. O
StockControl centraliza essas informações em um único lugar, de forma
simples, e já avisa automaticamente quando um produto está com o estoque
baixo (quantidade igual ou menor que o mínimo definido).

## ⚙️ Funcionalidades

- ✅ Cadastro de produtos (nome, categoria, quantidade, preço, estoque mínimo)
- ✅ Listagem de todos os produtos em formato de tabela
- ✅ Indicação automática de "ESTOQUE BAIXO" quando a quantidade atinge o mínimo
- ✅ Busca de produtos por nome (busca parcial, sem diferenciar maiúsculas/minúsculas)
- ✅ Edição de qualquer campo de um produto já cadastrado
- ✅ Exclusão de produtos, com confirmação antes de remover
- ✅ Validação de todos os dados digitados (textos vazios, números inválidos, valores negativos)
- ✅ Tratamento de erros de leitura/escrita de arquivo
- ✅ Salvamento automático em `dados.json` após cada alteração
- ✅ Carregamento automático dos dados ao iniciar o programa

## 🗂️ Estrutura do projeto

```
stock-control-cli/
├── main.py          # Ponto de entrada: menu e fluxo principal do programa
├── funcoes.py        # Regras de negócio, validações e manipulação de dados
├── dados.json         # Arquivo onde os produtos são salvos (gerado/atualizado automaticamente)
├── README.md          # Documentação do projeto
└── .gitignore         # Arquivos/pastas ignorados pelo Git
```

### Como cada arquivo funciona

- **`main.py`**: contém apenas o laço principal do programa. Exibe o menu,
  lê a opção escolhida pelo usuário e chama a função correspondente do
  `funcoes.py`. Não possui nenhuma regra de negócio — só orquestra o fluxo.
- **`funcoes.py`**: concentra toda a lógica do sistema: leitura e escrita do
  JSON, validação de entradas do usuário (textos, números inteiros e
  decimais) e as operações de CRUD (cadastrar, listar, buscar, editar,
  excluir).
- **`dados.json`**: arquivo de persistência. Cada produto é salvo como um
  objeto com `id`, `nome`, `categoria`, `quantidade`, `preco` e
  `estoque_minimo`. É lido automaticamente ao iniciar o programa e
  sobrescrito a cada alteração.

## ▶️ Como executar

Requisitos: **Python 3.8 ou superior** (nenhuma biblioteca externa é necessária).

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/stock-control-cli.git
cd stock-control-cli

# Execute o programa
python main.py
```

Ao iniciar, o programa carrega os produtos existentes em `dados.json` e
exibe o menu principal:

```
===== StockControl - Sistema de Controle de Estoque =====
1. Cadastrar produto
2. Listar produtos
3. Buscar produto
4. Editar produto
5. Excluir produto
6. Salvar e sair
===========================================================
```

