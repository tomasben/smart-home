import sys
import os
import msvcrt

from lex import Lexer


def limpiar_pantalla():
    os.system("cls")


def mostrar_banner():
    print("\033[96m" + "=" * 60)
    print("        SMART HOME - Analizador Léxico")
    print("=" * 60 + "\033[0m")
    print()


def mostrar_menu():
    mostrar_banner()
    print("  \033[93m[1]\033[0m  Escribir código en consola")
    print("  \033[93m[2]\033[0m  Cargar archivo .smart")
    print("  \033[93m[0]\033[0m  Salir")
    print()


def mostrar_resultados(lexer, tokens):
    print()
    print("\033[96m" + "-" * 60)
    print("  Resultados del Análisis Léxico")
    print("-" * 60 + "\033[0m")

    if lexer.errors:
        print("\n\033[91mErrores encontrados:\033[0m")
        for err in lexer.errors:
            print(f"  {err}\n")
    else:
        print("\n\033[92mAnálisis léxico exitoso. Sin errores.\033[0m")

    print()
    for tok in tokens:
        print(tok)


def analizar(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    mostrar_resultados(lexer, tokens)


def editor_consola():
    print("\033[96m" + "-" * 60)
    print("  Editor de código Smart Home")
    print("-" * 60 + "\033[0m")
    print()
    print("  \033[90mEscribí tu código libremente.\033[0m")
    print("  \033[90mPresioná \033[93mCtrl+Enter\033[90m para enviar y analizar.\033[0m")
    print("  \033[90mPresioná \033[93mEsc\033[90m para volver al menú.\033[0m")
    print()

    lineas = [""]
    linea_actual = 0
    col = 0

    num = " 1"
    sys.stdout.write(f"\033[92m{num} │\033[0m ")
    sys.stdout.flush()

    while True:
        ch = msvcrt.getwch()

        if ch == "\x1b":
            print()
            return None

        if ch == "\n":
            source = "\n".join(lineas)
            print()
            return source

        if ch == "\r":
            print()
            linea_actual += 1
            lineas.append("")
            col = 0
            num = str(linea_actual + 1).rjust(2)
            sys.stdout.write(f"\033[92m{num} │\033[0m ")
            sys.stdout.flush()
            continue

        if ch == "\t":
            lineas[linea_actual] += "    "
            col += 4
            sys.stdout.write("    ")
            sys.stdout.flush()
            continue

        if ch == "\x08":
            if col > 0:
                lineas[linea_actual] = lineas[linea_actual][:-1]
                col -= 1
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue

        if ch == "\x00" or ch == "\xe0":
            msvcrt.getwch()
            continue

        if ord(ch) < 32:
            continue

        lineas[linea_actual] += ch
        col += 1
        sys.stdout.write(ch)
        sys.stdout.flush()


def cargar_archivo():
    print("\033[96m" + "-" * 60)
    print("  Cargar archivo .smart")
    print("-" * 60 + "\033[0m")
    print()

    ruta = input("  \033[93mRuta del archivo:\033[0m ").strip()

    if not ruta:
        print("\n\033[91m  No se ingresó ninguna ruta.\033[0m")
        return None

    if ruta.startswith('"') and ruta.endswith('"'):
        ruta = ruta[1:-1]

    if not ruta.lower().endswith(".smart"):
        print(f"\n\033[91m  Error: el archivo debe tener extensión .smart\033[0m")
        return None

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"\n\033[91m  Error: archivo '{ruta}' no encontrado.\033[0m")
        return None
    except PermissionError:
        print(f"\n\033[91m  Error: sin permisos para leer '{ruta}'.\033[0m")
        return None


def pausar():
    print("\n\033[90m  Presioná cualquier tecla para volver al menú...\033[0m")
    msvcrt.getwch()


def main():
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
        if not file_name.lower().endswith(".smart"):
            print(
                f"\033[91mError:\033[0m el archivo '{file_name}' no tiene extensión .smart"
            )
            sys.exit(1)
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                source = f.read()
        except FileNotFoundError:
            print(f"\033[91mError:\033[0m archivo '{file_name}' no encontrado")
            sys.exit(1)
        analizar(source)
        return

    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input("  \033[93mElegí una opción:\033[0m ").strip()

        if opcion == "1":
            limpiar_pantalla()
            source = editor_consola()
            if source is not None and source.strip():
                analizar(source)
                pausar()
            elif source is not None:
                print("\n\033[91m  No se ingresó código.\033[0m")
                pausar()

        elif opcion == "2":
            limpiar_pantalla()
            source = cargar_archivo()
            if source is not None:
                analizar(source)
                pausar()
            else:
                pausar()

        elif opcion == "0":
            limpiar_pantalla()
            print("\033[96m  ¡Hasta luego!\033[0m\n")
            break

        else:
            print("\n\033[91m  Opción no válida.\033[0m")
            pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[91m  Ejecución interrumpida.\033[0m")
        sys.exit(130)
