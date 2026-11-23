# Tema 4: Controle de Logistica Portuaria
# Aluno: Arthur Felipe Dos Santos - 251-001225
import os
from collections.abc import Iterator
from queue import Queue, LifoQueue

# Tipos usados no programa
Registro = list[str]
Arvore = dict[str, "Arvore"]
Caminho = tuple[str, ...]

ARQUIVO: str = "dados_sistema.txt"

frota: list[Registro] = []
fila: Queue[Registro] = Queue()
pilha: LifoQueue[Registro] = LifoQueue()
arvore: Arvore = {}


CAMPOS: dict[str, list[str]] = {
    "LISTA": ["Placa", "Transportadora", "Tipo de veiculo"],
    "FILA": ["Placa", "Motorista", "Carga"],
    "PILHA": ["Codigo", "Conteudo", "Peso (t)"],
}


def ler(msg: str) -> str:
    while True:
        txt = input(msg).strip()
        if txt and "|" not in txt and ">" not in txt:
            return txt
        print("Valor invalido (vazio ou com | ou >).")


def ler_registro(tipo: str) -> Registro:
    return [ler(c + ": ") for c in CAMPOS[tipo]]


def exibir(registro: Registro) -> str:
    return " | ".join(registro)


def ler_indice(lista: list[Registro]) -> int | None:
    txt = input("Indice: ").strip()
    if txt.isdigit() and int(txt) < len(lista):
        return int(txt)
    print("Indice invalido.")
    return None


# ---------- LISTA (frota) ----------
def lista_menu() -> None:
    print("1-Inserir")
    print("2-Listar")
    print("3-Atualizar")
    print("4-Remover")
    op = input("-> ").strip()

    match op:
        case "1":
            frota.append(ler_registro("LISTA"))

        case "2":
            if not frota:
                print("Frota vazia.")
            for pos, v in enumerate(frota):
                print(pos, "-", exibir(v))

        case "3" | "4":
            i = ler_indice(frota)
            if i is None:
                return
            match op:
                case "3":
                    frota[i] = ler_registro("LISTA")
                case "4":
                    print("Removido:", exibir(frota.pop(i)))

        case _:
            print("Opcao invalida.")


def fila_menu() -> None:
    print("1-Chegada")
    print("2-Listar")
    print("3-Atualizar primeiro")
    print("4-Liberar")
    op = input("-> ").strip()

    match op:
        case "1":
            fila.put(ler_registro("FILA"))  # entra no fim

        case "2" | "3" | "4" if fila.empty():
            print("Patio vazio.")

        case "2":
            for c in fila.queue:  # apenas leitura, do primeiro ao ultimo
                print(exibir(c))

        case "3":
            fila.queue[0] = ler_registro("FILA")  # primeiro da fila

        case "4":
            print("Liberado:", exibir(fila.get()))  # sai do inicio

        case _:
            print("Opcao invalida.")


def pilha_menu() -> None:
    print("1-Empilhar")
    print("2-Listar")
    print("3-Atualizar topo")
    print("4-Desempilhar")
    op = input("-> ").strip()

    match op:
        case "1":
            pilha.put(ler_registro("PILHA"))  # entra no topo

        case "2" | "3" | "4" if pilha.empty():
            print("Nenhum conteiner empilhado.")

        case "2":
            for c in reversed(pilha.queue):  # apenas leitura, do topo a base
                print(exibir(c))

        case "3":
            pilha.queue[-1] = ler_registro("PILHA")  # topo = ultimo da lista interna

        case "4":
            print("Desempilhado:", exibir(pilha.get()))  # sai do topo

        case _:
            print("Opcao invalida.")


def inserir_caminho(caminho: list[str]) -> None:
    no: Arvore = arvore
    for nome in caminho:          # desce criando os niveis que faltam
        no = no.setdefault(nome, {})


def mostrar(no: Arvore, nivel: int = 0) -> None:
    for nome, filhos in no.items():
        print("  " * nivel + "- " + nome)
        mostrar(filhos, nivel + 1)


def caminhos(no: Arvore, prefixo: Caminho = ()) -> Iterator[Caminho]:
    for nome, filhos in no.items():
        if filhos:
            yield from caminhos(filhos, prefixo + (nome,))
        else:
            yield prefixo + (nome,)


def ler_caminho() -> list[str] | None:
    partes = [p.strip() for p in input("Caminho (ex: Santos>Rotterdam>Hamburgo): ").split(">")]
    if all(partes) and not any("|" in p for p in partes):
        return partes
    print("Caminho invalido.")
    return None


def buscar_pai(caminho: list[str]) -> Arvore | None:
    pai: Arvore = arvore
    for nome in caminho[:-1]:
        proximo = pai.get(nome)
        if proximo is None:
            return None
        pai = proximo
    return pai


def arvore_menu() -> None:
    print("1-Inserir")
    print("2-Mostrar")
    print("3-Renomear")
    print("4-Remover")
    op = input("-> ").strip()

    match op:
        case "2":
            if arvore:
                mostrar(arvore)
            else:
                print("Nenhuma rota.")

        case "1" | "3" | "4":
            caminho = ler_caminho()
            if caminho is None:
                return

            if op == "1":
                inserir_caminho(caminho)
                return

            pai = buscar_pai(caminho)
            if pai is None or caminho[-1] not in pai:
                print("Rota nao encontrada.")
                return

            match op:
                case "3":
                    novo = ler("Novo nome: ")
                    if novo in pai:
                        print("Ja existe um no com esse nome.")
                    else:
                        pai[novo] = pai.pop(caminho[-1])
                case "4":
                    del pai[caminho[-1]]

        case _:
            print("Opcao invalida.")


def salvar() -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        for v in frota:
            f.write("LISTA|" + "|".join(v) + "\n")
        for c in fila.queue:
            f.write("FILA|" + "|".join(c) + "\n")
        for c in pilha.queue:
            f.write("PILHA|" + "|".join(c) + "\n")
        for c in caminhos(arvore):
            f.write("ARVORE|" + "|".join(c) + "\n")
    print("Dados salvos.")


def carregar() -> None:
    if not os.path.exists(ARQUIVO):
        print("Arquivo nao encontrado.")
        return
    frota.clear()
    fila.queue.clear()
    pilha.queue.clear()
    arvore.clear()
    with open(ARQUIVO, encoding="utf-8") as f:
        for linha in f:
            tipo, *dados = linha.strip().split("|")
            dados = [d.strip() for d in dados]
            if not all(dados):
                continue
            if tipo in CAMPOS and len(dados) != len(CAMPOS[tipo]):
                continue

            match tipo:
                case "LISTA":
                    frota.append(dados)
                case "FILA":
                    fila.put(dados)
                case "PILHA":
                    pilha.put(dados)
                case "ARVORE" if dados:
                    inserir_caminho(dados)
    print("Dados carregados.")


def main() -> None:
    while True:
        print()
        print("1-Frota (Lista)")
        print("2-Patio (Fila)")
        print("3-Conteineres (Pilha)")
        print("4-Rotas (Arvore)")
        print("5-Salvar")
        print("6-Carregar")
        print("0-Sair")
        op = input("-> ").strip()

        match op:
            case "1":
                lista_menu()
            case "2":
                fila_menu()
            case "3":
                pilha_menu()
            case "4":
                arvore_menu()
            case "5":
                salvar()
            case "6":
                carregar()
            case "0":
                break
            case _:
                print("Opcao invalida.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrado.")