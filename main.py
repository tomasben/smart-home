import os
import sys
import textwrap

from lex import Lexer
from parser import parser

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
UI_LENGTH = 40


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_banner():
    title = "Smart-Home | Analizador Léxico"
    lpadding = (UI_LENGTH - len(title)) // 2

    print(f"{DIM}{'─' * UI_LENGTH}")
    print(f"{lpadding * ' '}{BLUE}{BOLD}Smart-Home{RESET} {DIM}| Analizador Léxico")
    print(f"{DIM}{'─' * UI_LENGTH}{RESET}")


def mostrar_menu():
    mostrar_banner()
    print()
    print(f"  {BLUE}[1]{RESET}  Ingreso manual")
    print(f"  {BLUE}[2]{RESET}  Cargar archivo")
    print()
    print(f"  {BLUE}[0]{RESET}  Salir")
    print()


def mostrar_resultados(lexer, tokens, mode: str):
    if mode == "default":
        if lexer.errors:
            print(f"\n  {RED}Errores encontrados:{RESET}")
            for err in lexer.errors:
                print(f"  {err}\n")
        else:
            print("\n  Análisis léxico exitoso.")

        print()
        for tok in tokens:
            print(repr(tok))
    elif mode == "simple":
        print(
            f"<<< {' '.join(str(tok) for tok in tokens)}. {len(lexer.errors)} error(es) encontrados"
        )


def analizar(source, mode: str = "default", route: str = None):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    mostrar_resultados(lexer, tokens, mode)

    if not lexer.errors and mode == "default":
        print(f"\n  {BLUE}Iniciando Análisis Sintáctico...{RESET}")
        html_output = parser.parse(source, lexer=lexer)
        
        if html_output:
            print(f"  {GREEN}Análisis sintáctico exitoso.{RESET}")
            if route:
                html_route = route.rsplit(".", 1)[0] + ".html"
                try:
                    with open(html_route, "w", encoding="utf-8") as f:
                        f.write(html_output)
                    print(f"  {GREEN}[+] Archivo HTML generado en: {BOLD}{html_route}{RESET}")
                except Exception as e:
                    print(f"  {RED}Error al guardar HTML: {e}{RESET}")
        else:
            print(f"  {RED}El análisis sintáctico falló.{RESET}")


def interactivo():
    title = "Modo Interactivo (En Vivo)"
    lpadding = (UI_LENGTH - len(title)) // 2

    print(f"{DIM}{'─' * UI_LENGTH}{RESET}")
    print(f"{lpadding * ' '}{BLUE}{title}{RESET}")
    print(f"{DIM}{'─' * UI_LENGTH}{RESET}")

    for linea in textwrap.wrap(
        "Generación HTML en tiempo real. Abre 'interactivo.html' en tu navegador.", width=UI_LENGTH - 1
    ):
        print(" " + linea)
    for linea in textwrap.wrap(
        "Escribe 'cancelar' para descartar la línea actual, o 'salir' para terminar.", width=UI_LENGTH - 1
    ):
        print(" " + linea)

    print(f"{DIM}{'─' * UI_LENGTH}{RESET}")
    print()

    codigo_acumulado = ""
    buffer_temporal = ""
    prompt = ">>> "

    while True:
        sentence = input(prompt)

        if sentence.strip().lower() == "salir":
            break
        
        if sentence.strip().lower() == "cancelar":
            buffer_temporal = ""
            prompt = ">>> "
            print(f"  {YELLOW}Bloque actual descartado.{RESET}")
            continue

        if sentence.strip() == "" and not buffer_temporal:
            continue

        buffer_temporal += sentence + "\n"
        test_source = codigo_acumulado + "\n" + buffer_temporal

        # Chequeo Léxico
        lexer = Lexer(test_source)
        lexer.tokenize()
        if lexer.errors:
            print(f"  {RED}Error léxico. Escribe 'cancelar' para descartar.{RESET}")
            prompt = "... "
            continue

        # Evitamos que p_error ensucie la consola usando stdout temporal
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = captura = io.StringIO()
        
        try:
            html_output = parser.parse(test_source, lexer=lexer)
        except Exception:
            html_output = None
        finally:
            sys.stdout = old_stdout

        salida_error = captura.getvalue()

        if html_output:
            # Se parseó con éxito (instrucción o bloque completado)
            codigo_acumulado = test_source
            buffer_temporal = ""
            prompt = ">>> "
            
            with open("interactivo.html", "w", encoding="utf-8") as f:
                f.write(html_output)
            print(f"  {GREEN}[+] HTML generado/actualizado en 'interactivo.html'{RESET}")
            
        elif "Fin de archivo inesperado" in salida_error:
            # PLY necesita más líneas (ej: falta el 'end' de un bloque)
            prompt = "... "
        else:
            # Error de sintaxis o semántico real
            print(salida_error, end="")
            prompt = "... "


def cargar_archivo():
    message = "Cargar archivo .smart"
    lpadding = (UI_LENGTH - len(message)) // 2

    print(f"{DIM}{'─' * UI_LENGTH}{RESET}")
    print(f"{lpadding * ' '}{BLUE}Cargar archivo{RESET} {DIM}.smart{RESET}")
    print(f"{DIM}{'─' * UI_LENGTH}{RESET}")

    while True:
        print()
        route = input("  Ruta del archivo: ").strip()

        if route.startswith(('"', "'")) and route.endswith(('"', "'")):
            route = route[1:-1]

        if not route.lower().endswith(".smart"):
            print(
                f"  {RED}Error:{RESET} el archivo debe tener extensión {BOLD}.smart{RESET}"
            )
        else:
            try:
                with open(route, "r", encoding="utf-8") as file:
                    return file.read(), route
            except FileNotFoundError:
                print(f"\n  {RED}Error:{RESET} archivo '{route}' no encontrado.")
                return None
            except PermissionError:
                print(f"\n  {RED}Error:{RESET} sin permisos para leer '{route}'.")
                return None


def pausar():
    try:
        input(f"\n  {DIM}Presioná Enter para volver al menú...{RESET}")
    except (KeyboardInterrupt, EOFError):
        pass


def main():
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
        if not file_name.lower().endswith(".smart"):
            print(
                f"  {RED}Error:{RESET} el archivo debe tener extensión {BOLD}.smart{RESET}"
            )
            sys.exit(1)
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                source = file.read()
        except FileNotFoundError:
            print(f"\n  {RED}Error:{RESET} archivo '{file_name}' no encontrado.")
            sys.exit(1)
        analizar(source, route=file_name)
        return

    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input("  >>> ").strip()

        if opcion == "1":
            limpiar_pantalla()
            interactivo()

        elif opcion == "2":
            limpiar_pantalla()
            result = cargar_archivo()
            if result is not None:
                source, route = result
                analizar(source, route=route)
                pausar()
            else:
                pausar()

        elif opcion == "0":
            limpiar_pantalla()
            sys.exit(0)
            break

        else:
            print("\n  Opción no válida.")
            pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  Ejecución interrumpida por teclado.")
        sys.exit(130)
