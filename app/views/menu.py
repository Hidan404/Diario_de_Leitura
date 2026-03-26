from app.controllers.leitura_controllers import LeituraController
from app.models.readings import ReadingType, ReadingStatus
from datetime import datetime

controller = LeituraController()


# ========================
# UTILITÁRIOS
# ========================

def input_lista(msg):
    valor = input(msg)
    return [v.strip() for v in valor.split(",")] if valor else []


def input_opcional_int(msg):
    valor = input(msg)
    return int(valor) if valor else None


def input_data(msg):
    valor = input(msg)
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%Y-%m-%d")
    except:
        print("Formato inválido! Use YYYY-MM-DD")
        return None


def escolher_enum(enum_class, msg):
    print(f"\n{msg}")
    for item in enum_class:
        print(f"- {item.name}")

    valor = input("Escolha: ").upper()

    try:
        return enum_class[valor]
    except:
        print("Valor inválido!")
        return None


# ========================
# AÇÕES
# ========================

def adicionar():
    print("\n=== ADICIONAR LEITURA ===")

    title = input("Título: ")
    authors = input_lista("Autores (separados por vírgula): ")

    type_ = escolher_enum(ReadingType, "Tipo")
    status = escolher_enum(ReadingStatus, "Status")

    rating = input_opcional_int("Nota (opcional): ")
    current_page = input_opcional_int("Página atual: ")
    total_pages = input_opcional_int("Total de páginas: ")
    published_date = input_data("Data (YYYY-MM-DD): ")
    notes = input("Notas: ") or None
    description = input("Descrição: ") or None
    cover = input("Capa (URL ou caminho): ") or None
    genres = input_lista("Gêneros: ")

    if not type_ or not status:
        print("Erro: tipo ou status inválido")
        return

    controller.adicionar_leitura(
        title,
        authors,
        type_,
        status,
        rating,
        current_page,
        total_pages,
        published_date,
        notes,
        description,
        cover,
        genres,
    )

    print("\n✅ Leitura adicionada com sucesso!")


# ------------------------

def listar():
    print("\n=== LISTA DE LEITURAS ===")

    leituras = controller.listar_leitura()

    if not leituras:
        print("Nenhuma leitura encontrada.")
        return

    for l in leituras:
        print(f"\nID: {l.id}")
        print(f"Título: {l.title}")
        print(f"Autores: {', '.join(l.authors)}")
        print(f"Tipo: {l.type.value}")
        print(f"Status: {l.status.value}")
        print(f"Rating: {l.rating if l.rating is not None else 'N/A'}")
        print(f"Página atual: {l.current_page if l.current_page is not None else 'N/A'}")
        print(f"Total de páginas: {l.total_pages if l.total_pages is not None else 'N/A'}")
        print(f"Data de publicação: {l.published_date.strftime('%Y-%m-%d') if l.published_date else 'N/A'}")
        print(f"Notas: {l.notes if l.notes else 'N/A'}")
        print(f"Descrição: {l.description if l.description else 'N/A'}")
        print(f"Capa: {l.cover_image_path if l.cover_image_path else 'N/A'}")
        print(f"Gêneros: {', '.join(l.genres) if l.genres else 'N/A'}")


# ------------------------

def atualizar():
    print("\n=== ATUALIZAR LEITURA ===")

    try:
        id_ = int(input("ID da leitura: "))
    except:
        print("ID inválido!")
        return

    title = input("Novo título: ")
    authors = input_lista("Autores: ")

    type_ = escolher_enum(ReadingType, "Tipo")
    status = escolher_enum(ReadingStatus, "Status")

    rating = input_opcional_int("Nota: ")
    current_page = input_opcional_int("Página atual: ")
    total_pages = input_opcional_int("Total de páginas: ")
    published_date = input_data("Data (YYYY-MM-DD): ")
    notes = input("Notas: ") or None
    description = input("Descrição: ") or None
    cover = input("Capa: ") or None
    genres = input_lista("Gêneros: ")

    controller.atualizar_leitura(
        id_,
        title,
        authors,
        type_,
        status,
        rating,
        current_page,
        total_pages,
        published_date,
        notes,
        description,
        cover,
        genres,
    )

    print("\n✏️ Leitura atualizada!")


# ------------------------

def deletar():
    print("\n=== DELETAR LEITURA ===")

    try:
        id_ = int(input("ID: "))
    except:
        print("ID inválido!")
        return

    controller.excluir_leitura(id_)
    print("🗑️ Leitura removida!")


# ========================
# MENU PRINCIPAL
# ========================

def menu():
    while True:
        print("\n======= MENU =======")
        print("1 - Adicionar leitura")
        print("2 - Listar leituras")
        print("3 - Atualizar leitura")
        print("4 - Deletar leitura")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            atualizar()
        elif opcao == "4":
            deletar()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


# ========================
# ENTRYPOINT
# ========================

if __name__ == "__main__":
    menu()