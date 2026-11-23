# Controle de Logística Portuária

**Disciplina:** Teoria das Estruturas de Dados
**Tema sorteado:** Tema 4 – Controle de Logística Portuária
**Aluno:** Arthur Felipe Dos Santos – 251-001225

Sistema de linha de comando (CLI) em Python que usa as quatro estruturas da disciplina (**Lista, Fila, Pilha e Árvore**) para gerenciar as operações de um porto. Os dados são salvos em um arquivo texto (`dados_sistema.txt`).

---

## Estruturas de dados e seus papéis

| Estrutura | Entidade no sistema | Implementação | Regra de acesso |
|-----------|--------------------|---------------|-----------------|
| **Lista** | Frota de veículos e transportadoras credenciadas | `list` | Acesso por índice |
| **Fila** | Caminhões no pátio aguardando liberação para embarque | `queue.Queue` | FIFO: entra no fim, sai do início |
| **Pilha** | Empilhamento físico de contêineres | `queue.LifoQueue` | LIFO: entra e sai pelo topo |
| **Árvore** | Rotas marítimas, portos intermediários e destinos finais | Dicionários aninhados (`dict`) | Navegação e inserção hierárquica |

### Campos de cada registro

- **Lista (Frota):** Placa, Transportadora, Tipo de veículo
- **Fila (Pátio):** Placa, Motorista, Carga
- **Pilha (Contêineres):** Código, Conteúdo, Peso (t)
- **Árvore (Rotas):** caminho hierárquico, por exemplo `Santos>Rotterdam>Hamburgo`

---

## Requisitos

- Python **3.10 ou superior** (o código usa `match/case`)
- Nenhuma biblioteca externa

## Como executar

```bash
python main.py
```

O sistema começa vazio. Para recuperar dados salvos antes, use a opção **6 – Carregar**.

---

## Menu principal

```
1-Frota (Lista)
2-Patio (Fila)
3-Conteineres (Pilha)
4-Rotas (Arvore)
5-Salvar
6-Carregar
0-Sair
```

### 1 – Frota (Lista)
| Opção | Ação |
|-------|------|
| 1 | Inserir veículo no fim da lista |
| 2 | Listar todos os veículos com seus índices |
| 3 | Atualizar o veículo de um índice |
| 4 | Remover o veículo de um índice |

### 2 – Pátio (Fila)
| Opção | Ação |
|-------|------|
| 1 | Chegada: o caminhão entra no **fim** da fila |
| 2 | Listar do primeiro ao último |
| 3 | Atualizar o primeiro da fila |
| 4 | Liberar: remove o caminhão do **início** da fila |

### 3 – Contêineres (Pilha)
| Opção | Ação |
|-------|------|
| 1 | Empilhar contêiner no **topo** |
| 2 | Listar do topo até a base |
| 3 | Atualizar o contêiner do topo |
| 4 | Desempilhar: remove o contêiner do **topo** |

### 4 – Rotas (Árvore)
| Opção | Ação |
|-------|------|
| 1 | Inserir rota (cria os níveis que faltam) |
| 2 | Mostrar a árvore com indentação |
| 3 | Renomear um nó (porto) |
| 4 | Remover um nó e toda a sua sub-rota |

Os caminhos são escritos com `>` separando os níveis:

```
Santos>Rotterdam>Hamburgo
```

Exemplo de exibição:

```
- Santos
  - Rotterdam
    - Hamburgo
  - Lisboa
```

---

## Persistência (`dados_sistema.txt`)

- **5 – Salvar:** grava o estado atual da memória no arquivo e sobrescreve o conteúdo anterior.
- **6 – Carregar:** limpa as estruturas em memória e as reconstrói a partir do arquivo.

Cada linha começa com o identificador da estrutura, seguido dos atributos separados por pipe (`|`). Não são usados banco de dados, JSON, CSV nem `pickle`.

Exemplo:

```
LISTA|ABC1D23|TransPorto Ltda|Carreta
LISTA|XYZ9K88|Maritima SA|Bitrem
FILA|ABC1D23|Joao Pereira|Soja
FILA|XYZ9K88|Ana Costa|Minerio
PILHA|CONT-001|Eletronicos|12
PILHA|CONT-002|Maquinario|25
ARVORE|Santos|Rotterdam|Hamburgo
ARVORE|Santos|Lisboa
```

Como cada estrutura é salva:
- **Fila:** do primeiro ao último, para manter a ordem de chegada.
- **Pilha:** da base ao topo, para que o último contêiner do arquivo volte ao topo ao carregar.
- **Árvore:** uma linha por caminho completo, da raiz até cada folha.

### Validações
- Os campos não podem ficar vazios nem conter `|` ou `>`, pois são os delimitadores do arquivo e dos caminhos da árvore.
- Ao carregar, linhas mal formatadas (campos vazios ou quantidade de campos errada) são ignoradas.

---

## Organização do código (`main.py`)

Todo o código está em um único arquivo e dividido em funções:

| Seção | Funções |
|-------|---------|
| Utilitários de entrada | `ler`, `ler_registro`, `ler_indice`, `exibir` |
| Lista | `lista_menu` |
| Fila | `fila_menu` |
| Pilha | `pilha_menu` |
| Árvore | `inserir_caminho`, `mostrar`, `caminhos`, `ler_caminho`, `buscar_pai`, `arvore_menu` |
| Persistência | `salvar`, `carregar` |
| Menu principal | `main` |