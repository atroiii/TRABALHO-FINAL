# Controle de Logística Portuária
 
**Disciplina:** Teoria das Estruturas de Dados
**Tema sorteado:** Tema 4 – Controle de Logística Portuária
**Aluno:** Arthur Felipe Dos Santos – 251-001225
 
Sistema de linha de comando (CLI) em Python que usa as quatro estruturas da disciplina (**Lista, Fila, Pilha e Árvore**) para gerenciar as operações de um porto. Os dados são salvos em um arquivo texto (`dados_sistema.txt`).
 
---
 
## Requisitos
 
- Python **3.10 ou superior** (o código usa `match/case` e a sintaxe de tipos `int | None`)
- Nenhuma biblioteca externa: apenas módulos da biblioteca padrão (`os`, `queue`, `collections.abc`)
Para conferir a versão instalada:
 
```bash
python --version
```
 
## Como executar
 
1. Clone o repositório e entre na pasta do projeto:
```bash
git clone <link-do-repositorio>
cd <nome-da-pasta>
```
 
2. Execute o sistema:
   | Sistema operacional | Comando |
   |---------------------|---------|
   | Windows | `python main.py` (ou `py main.py`) |
   | Linux / macOS | `python3 main.py` |
3. Navegue pelos menus digitando o número da opção e pressionando **Enter**.
4. Para encerrar, use a opção **0 – Sair** (ou `Ctrl+C`).
> O sistema começa vazio. Para recuperar dados salvos em uma execução anterior, use a opção **6 – Carregar**. O arquivo `dados_sistema.txt` é criado na pasta em que o comando foi executado, na primeira vez que a opção **5 – Salvar** é usada.
 
---
 
## Estruturas de dados e seus papéis
 
| Estrutura | Entidade no sistema | Implementação | Regra de acesso |
|-----------|--------------------|---------------|-----------------|
| **Lista** | Frota de veículos e transportadoras credenciadas | `list` | Acesso direto por índice |
| **Fila** | Caminhões no pátio aguardando liberação para embarque | `queue.Queue` | FIFO: entra no fim, sai do início |
| **Pilha** | Empilhamento físico de contêineres | `queue.LifoQueue` | LIFO: entra e sai pelo topo |
| **Árvore** | Rotas marítimas, portos intermediários e destinos finais | Dicionários aninhados (`dict`) | Navegação e inserção hierárquica |
 
---
 
## Justificativa técnica das estruturas
 
Cada estrutura foi escolhida porque sua **regra de acesso** reproduz a regra de funcionamento do problema real no porto. Assim, a própria estrutura impede operações que não fariam sentido na prática.
 
### Lista: Frota de veículos
 
**Problema:** a frota é um cadastro de veículos e transportadoras credenciadas. Ela não tem ordem de atendimento: o operador precisa consultar, corrigir ou descredenciar **qualquer** veículo, em **qualquer** posição.
 
**Por que Lista:** a Lista é a única das quatro estruturas que permite acesso direto a qualquer elemento pelo índice. Com isso, as operações de atualizar (`frota[i] = ...`) e remover (`frota.pop(i)`) são feitas sobre o veículo escolhido, sem precisar retirar os outros. A leitura por índice é O(1).
 
**Por que não as outras:** Fila e Pilha só dão acesso às pontas. Para corrigir um veículo no meio do cadastro, seria preciso remover todos os que estão antes dele. A Árvore representa hierarquia, e o cadastro da frota é uma coleção sem relação de pai e filho.
 
**Implementação:** `list` nativa do Python. O índice é validado com `isdigit()` para recusar valores negativos, já que em Python `frota[-1]` é aceito e acessaria o último elemento sem erro.
 
### Fila: Pátio de caminhões
 
**Problema:** os caminhões chegam ao pátio e aguardam liberação para embarque. Por justiça operacional, **quem chegou primeiro deve ser liberado primeiro**.
 
**Por que Fila:** essa é exatamente a regra **FIFO** (*First In, First Out*). Na Fila, a entrada acontece só pelo fim (`put`) e a saída só pelo início (`get`). A estrutura garante a ordem de chegada e impede que um caminhão seja liberado fora de ordem.
 
**Por que não as outras:** uma Lista permitiria remover qualquer posição e quebraria a ordem de atendimento. Uma Pilha liberaria primeiro o **último** caminhão a chegar, o oposto do desejado. A Árvore não representa uma sequência de espera.
 
**Implementação:** `queue.Queue`. Internamente ela usa um `collections.deque`, que insere no fim e remove do início em tempo O(1). Já uma `list` comum com `pop(0)` custaria O(n), porque desloca todos os elementos restantes a cada remoção.
 
### Pilha: Contêineres empilhados
 
**Problema:** contêineres são empilhados fisicamente uns sobre os outros. O guindaste só alcança o contêiner **de cima**: para chegar a um contêiner de baixo, todos os que estão acima precisam ser retirados antes.
 
**Por que Pilha:** essa é a regra **LIFO** (*Last In, First Out*). Na Pilha, inserção e remoção acontecem só pelo topo, e o último contêiner empilhado é o primeiro a sair. A estrutura reproduz a limitação física do empilhamento.
 
**Por que não as outras:** uma Lista permitiria "tirar" um contêiner do meio da pilha, o que é fisicamente impossível. Uma Fila retiraria primeiro o contêiner da base. A Árvore não representa uma sequência linear.
 
**Implementação:** `queue.LifoQueue`. Internamente ela usa uma `list`, em que o topo é o último elemento: `append` e `pop` no final são O(1).
 
### Árvore: Rotas marítimas
 
**Problema:** uma rota parte de um porto de origem e pode se ramificar em vários portos intermediários, e cada um deles pode levar a vários destinos finais. Por exemplo, Santos → Rotterdam → Hamburgo e Santos → Lisboa. Os dados têm relação de **pai e filho**.
 
**Por que Árvore:** a Árvore é a estrutura que representa hierarquias. Cada nó (porto) pode ter vários filhos (próximos portos), e as **folhas** são os destinos finais. Remover um porto intermediário remove automaticamente toda a sua sub-rota, porque ela depende dele.
 
**Por que não as outras:** Lista, Fila e Pilha são estruturas **lineares**: cada elemento tem no máximo um sucessor. Elas não conseguem representar um porto que se divide em vários caminhos sem repetir dados ou perder a relação entre os portos.
 
**Implementação:** dicionários aninhados, em que cada nó é um `dict` cujas chaves são os nomes dos portos filhos e cujos valores são os nós desses filhos. Uma folha é um dicionário vazio (`{}`). Essa escolha permite:
- buscar um filho pelo nome em tempo O(1) em média, sem percorrer uma lista de filhos;
- impedir nomes de porto repetidos no mesmo nível, já que as chaves de um dicionário são únicas;
- inserir um caminho inteiro criando só os níveis que faltam (`setdefault`);
- percorrer a árvore de forma recursiva para exibi-la com indentação e para salvá-la.
---
 
## Campos de cada registro
 
- **Lista (Frota):** Placa, Transportadora, Tipo de veículo
- **Fila (Pátio):** Placa, Motorista, Carga
- **Pilha (Contêineres):** Código, Conteúdo, Peso (t)
- **Árvore (Rotas):** caminho hierárquico, por exemplo `Santos>Rotterdam>Hamburgo`
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
 
> Nas opções de listar e atualizar da Fila e da Pilha, o acesso aos elementos é feito pelo atributo interno `.queue` (somente leitura na listagem e alteração apenas do elemento da ponta). A inserção e a remoção sempre usam `put` e `get`, respeitando a regra FIFO/LIFO.
 
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
- **Fila:** do primeiro ao último, para manter a ordem de chegada ao carregar.
- **Pilha:** da base ao topo, para que o último contêiner do arquivo volte a ser o topo ao carregar.
- **Árvore:** uma linha por caminho completo, da raiz até cada folha. Ao carregar, os caminhos que compartilham o mesmo início (como `Santos`) voltam a se juntar no mesmo nó.
### Validações
- Os campos não podem ficar vazios nem conter `|` ou `>`, pois são os delimitadores do arquivo e dos caminhos da árvore.
- Índices da Lista precisam ser números inteiros não negativos e menores que o tamanho da frota.
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