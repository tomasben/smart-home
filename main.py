import sys

from lex import Lexer


def main():
    if len(sys.argv) < 2:
        print("\033[91mError:\033[0m debes indicar un archivo .smart")
        print("Uso: python lexer.py <archivo.smart>")
        sys.exit(1)

    file_name = sys.argv[1]

    if not file_name.endswith(".smart"):
        print(
            f"\033[91mError:\033[0m el archivo '{file_name}' no tiene extensión .smart"
        )
        sys.exit(1)

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: archivo '{file_name}' no encontrado")
        sys.exit(1)

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    if lexer.errors:
        print("\n\033[91mErrores encontrados:\033[0m")
        for err in lexer.errors:
            print(f"  {err}\n")
    else:
        print("\n\033[92mAnálisis léxico exitoso.\033[0m")

    for tok in tokens:
        print(tok)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por teclado")

        sys.exit(130)
