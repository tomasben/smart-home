from tok import (
    ATRIBUTOS_VALIDOS,
    PALABRAS_RESERVADAS,
    PREFIJOS_ACTUADOR,
    PREFIJOS_SENSOR,
    Token,
    TokenKind,
)

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.row = 1
        self.col = 1
        self.tokens = []
        self.errors = []

    def add_error(self, msg, row=None, col=None):
        r = row if row is not None else self.row
        c = col if col is not None else self.col
        lines = self.source.split("\n")
        line_idx = r - 1
        if 0 <= line_idx < len(lines):
            line_text = lines[line_idx]
            margen_izq = 30
            margen_der = 10
            inicio = max(0, c - 1 - margen_izq)
            fin = min(len(line_text), c - 1 + margen_der + 1)
            fragmento = line_text[inicio:fin]
            prefijo = "..." if inicio > 0 else ""
            sufijo = "..." if fin < len(line_text) else ""
            pos_flecha = (c - 1) - inicio + len(prefijo)
            err_msg = f"\033[91mError Léxico\033[0m en línea {r}, col {c}: {msg}\n"
            err_msg += f"  {prefijo}{fragmento}{sufijo}\n"
            err_msg += "  " + " " * pos_flecha + "\033[91m^\033[0m"
            self.errors.append(err_msg)
        else:
            self.errors.append(f"\033[91mError Léxico:\033[0m {msg}")

    def peek(self, offset=0):
        p = self.pos + offset
        if p < len(self.source):
            return self.source[p]
        return ""

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.row += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def tokenize(self):
        while self.pos < len(self.source):
            ch = self.peek()

            if ch in " \t\r\n":
                self.advance()
                continue

            if ch in "=!<>()":
                self.consumir_operador()
                continue

            if ch == "/" and self.peek(1) == "/":
                self.consumir_comentario()
                continue

            if self.consumir_email():
                continue

            if self.consumir_hora():
                continue

            if self.consumir_fecha():
                continue

            if ch.isdigit():
                self.consumir_numero()
                continue

            if ch == '"':
                self.consumir_string()
                continue

            if ch.isalpha() or ch == "_":
                self.consumir_identificador()
                continue

            if ch == ".":
                self.consumir_atributo()
                continue

            self.add_error(f"Carácter no reconocido: '{ch}'")
            self.advance()

        self.tokens.append(Token(TokenKind.EOF, "", self.row, self.col))
        return self.tokens

    def consumir_email(self):
        temp_pos = self.pos
        while temp_pos < len(self.source) and (
            self.source[temp_pos].isalnum() or self.source[temp_pos] in "_.+-@"
        ):
            temp_pos += 1

        candidato = self.source[self.pos : temp_pos]

        if candidato.count("@") == 1:
            usuario, resto = candidato.split("@")
            if usuario and "." in resto:
                dominio, extension = resto.rsplit(".", 1)

                caracteres_validos = set("_.+-")
                usuario_valido = all(
                    c.isalnum() or c in caracteres_validos for c in usuario
                )
                dominio_valido = all(
                    c.isalnum() or c in caracteres_validos for c in dominio
                )
                extension_valida = extension.isalpha() and 2 <= len(extension) <= 4

                if usuario_valido and dominio_valido and extension_valida and dominio:
                    start_row, start_col = self.row, self.col
                    lexema = ""
                    while self.pos < temp_pos:
                        lexema += self.advance()
                    self.tokens.append(
                        Token(TokenKind.EMAIL, lexema, start_row, start_col)
                    )
                    return True
        return False

    def consumir_fecha(self):
        if self.pos + 9 >= len(self.source):
            return False

        d1 = self.source[self.pos]
        d2 = self.source[self.pos + 1]
        sep1 = self.source[self.pos + 2]
        m1 = self.source[self.pos + 3]
        m2 = self.source[self.pos + 4]
        sep2 = self.source[self.pos + 5]
        a1 = self.source[self.pos + 6]
        a2 = self.source[self.pos + 7]
        a3 = self.source[self.pos + 8]
        a4 = self.source[self.pos + 9]

        if not (
            d1.isdigit()
            and d2.isdigit()
            and sep1 == "/"
            and m1.isdigit()
            and m2.isdigit()
            and sep2 == "/"
            and a1.isdigit()
            and a2.isdigit()
            and a3.isdigit()
            and a4.isdigit()
        ):
            return False

        dia = int(d1 + d2)
        mes = int(m1 + m2)
        anio = int(a1 + a2 + a3 + a4)

        if not (1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= anio <= 2099):
            self.add_error(
                f"Fecha fuera de rango: '{d1}{d2}/{m1}{m2}/{a1}{a2}{a3}{a4}'"
            )
            for _ in range(10):
                self.advance()
            return True

        start_row, start_col = self.row, self.col
        lexema = ""

        for _ in range(10):
            lexema += self.advance()

        self.tokens.append(Token(TokenKind.FECHA, lexema, start_row, start_col))
        return True

    def consumir_hora(self):
        start_pos = self.pos
        start_row = self.row
        start_col = self.col
        num1 = ""
        num2 = ""


        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            num1 += self.source[self.pos]
            self.pos += 1
            self.col += 1


        if len(num1) != 2:
            self.pos = start_pos
            self.row = start_row
            self.col = start_col
            return False

        if self.pos >= len(self.source) or self.source[self.pos] != ":":
            self.pos = start_pos
            self.row = start_row
            self.col = start_col
            return False
        self.pos += 1
        self.col += 1


        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            num2 += self.source[self.pos]
            self.pos += 1
            self.col += 1

        if len(num2) != 2:
            self.pos = start_pos
            self.row = start_row
            self.col = start_col
            return False

        if not (0 <= int(num1) <= 23 and 0 <= int(num2) <= 59):
            self.add_error(f"Hora inválida: '{num1}:{num2}'", start_row, start_col)
            return True

        lexema = f"{num1}:{num2}"
        self.tokens.append(Token(TokenKind.HORA, lexema, start_row, start_col))
        return True

    def consumir_numero(self):
        start_row = self.row
        start_col = self.col
        lexema = ""

        while self.pos < len(self.source) and self.peek().isdigit():
            lexema += self.advance()

        if self.peek() == "." and self.peek(1).isdigit():
            lexema += self.advance()
            while self.pos < len(self.source) and self.peek().isdigit():
                lexema += self.advance()

        sig = self.peek()

        if sig == "%":
            lexema += self.advance()
            self.tokens.append(Token(TokenKind.PERCENT, lexema, start_row, start_col))

        elif sig == "°":
            lexema += self.advance()
            if self.peek().upper() == "C":
                lexema += self.advance()
                self.tokens.append(Token(TokenKind.TEMP, lexema, start_row, start_col))
            else:
                self.add_error(f"Unidad de temperatura incompleta: '{lexema}'")

        elif sig.lower() in ("l", "s", "m", "h"):
            if sig.lower() == "l" and self.source[self.pos : self.pos + 3].lower() == "lux":
                lexema += self.advance()
                lexema += self.advance()
                lexema += self.advance()
                self.tokens.append(Token(TokenKind.LUX, lexema, start_row, start_col))
            elif sig.lower() in ("s", "m", "h"):
                lexema += self.advance()
                self.tokens.append(
                    Token(TokenKind.TIME_DURATION, lexema, start_row, start_col)
                )
            else:
                self.tokens.append(
                    Token(TokenKind.NUMBER, lexema, start_row, start_col)
                )

        else:
            self.tokens.append(Token(TokenKind.NUMBER, lexema, start_row, start_col))

    def consumir_comentario(self):
        self.advance()
        self.advance()
        while self.pos < len(self.source) and self.peek() != "\n":
            self.advance()

    def consumir_identificador(self):
        start_row = self.row
        start_col = self.col
        lexema = ""

        while self.pos < len(self.source) and (
            self.peek().isalnum() or self.peek() == "_"
        ):
            lexema += self.advance()

        lexema_lower = lexema.lower()

        if lexema_lower in PALABRAS_RESERVADAS:
            self.tokens.append(
                Token(PALABRAS_RESERVADAS[lexema_lower], lexema, start_row, start_col)
            )
            return

        if lexema_lower in ("blanco", "rojo", "azul"):
            self.tokens.append(Token(TokenKind.COLOR, lexema, start_row, start_col))
            return

        if lexema_lower in ("frio", "calor", "vent"):
            self.tokens.append(Token(TokenKind.MODO, lexema, start_row, start_col))
            return

        for prefijo in PREFIJOS_SENSOR:
            if lexema_lower == prefijo or lexema_lower.startswith(prefijo + "_"):
                self.tokens.append(
                    Token(TokenKind.SENSOR, lexema, start_row, start_col)
                )
                return

        for prefijo in PREFIJOS_ACTUADOR:
            if lexema_lower.startswith(prefijo):
                self.tokens.append(
                    Token(TokenKind.ACTUATOR, lexema, start_row, start_col)
                )
                return

        self.add_error(f"Identificador no reconocido: '{lexema}'", start_row, start_col)

    def consumir_atributo(self):
        start_row = self.row
        start_col = self.col

        self.advance()

        nombre = ""
        while self.pos < len(self.source) and (
            self.peek().isalnum() or self.peek() == "_"
        ):
            nombre += self.advance()

        if not nombre:
            self.add_error(
                "Se esperaba un nombre de atributo después del '.'",
                start_row,
                start_col,
            )
            return

        if f".{nombre.lower()}" not in ATRIBUTOS_VALIDOS:
            self.add_error(f"Atributo desconocido: '.{nombre}'", start_row, start_col)
            return

        self.tokens.append(
            Token(TokenKind.ATTRIBUTE, "." + nombre, start_row, start_col)
        )

    def consumir_string(self):
        start_row = self.row
        start_col = self.col

        self.advance()
        contenido = ""

        while self.pos < len(self.source) and self.peek() != '"':
            if self.peek() == "\n":
                self.add_error(
                    "Cadena sin cerrar antes del fin de línea", start_row, start_col
                )
                return
            contenido += self.advance()

        if self.pos >= len(self.source):
            self.add_error("Cadena sin cerrar (EOF)")
            return

        self.advance()

        self.tokens.append(
            Token(TokenKind.STRING, '"' + contenido + '"', start_row, start_col)
        )

    def consumir_operador(self):
        start_row = self.row
        start_col = self.col
        ch = self.peek()
        sig = self.peek(1)

        if ch == "=" and sig == "=":
            self.advance()
            self.advance()
            self.tokens.append(Token(TokenKind.EQUAL, "==", start_row, start_col))
            return

        if ch == "!" and sig == "=":
            self.advance()
            self.advance()
            self.tokens.append(Token(TokenKind.NEGATE, "!=", start_row, start_col))
            return

        if ch == ">" and sig == "=":
            self.advance()
            self.advance()
            self.tokens.append(Token(TokenKind.GREAT_EQUAL, ">=", start_row, start_col))
            return

        if ch == "<" and sig == "=":
            self.advance()
            self.advance()
            self.tokens.append(Token(TokenKind.LESS_EQUAL, "<=", start_row, start_col))
            return

        if ch == "=":
            self.advance()
            self.tokens.append(Token(TokenKind.ASSIGN, "=", start_row, start_col))
            return

        if ch == ">":
            self.advance()
            self.tokens.append(Token(TokenKind.GREATER, ">", start_row, start_col))
            return

        if ch == "<":
            self.advance()
            self.tokens.append(Token(TokenKind.LESSER, "<", start_row, start_col))
            return

        if ch == "(":
            self.advance()
            self.tokens.append(Token(TokenKind.LPAREN, "(", start_row, start_col))
            return

        if ch == ")":
            self.advance()
            self.tokens.append(Token(TokenKind.RPAREN, ")", start_row, start_col))
            return

        if ch == "!":
            self.add_error("Operador inválido: '!' (¿quisiste decir '!='?)")
            self.advance()
            return

        self.add_error(f"Operador no reconocido: '{ch}'")
        self.advance()
