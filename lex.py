import ply.lex as lex

# Definimos los tokens como strings (en lugar de Enum)
tokens = [
    'WHEN', 'EVERY', 'IF', 'THEN', 'ELSE', 'DO', 'END',
    'AND', 'OR', 'NOT',
    'TRUE', 'FALSE', 'ON', 'OFF',
    'MODO', 'COLOR',
    
    'ACT_FOCO', 'ACT_AIRE', 'ACT_PERSIANA', 'ACT_CERRADURA', 'ACT_RELOJ', 'ACT_ALTAVOZ', 'ACT_ALARMA',
    
    'SENS_TEMP', 'SENS_HUMEDAD', 'SENS_LUZ', 'SENS_MOVIMIENTO', 'SENS_HUMO',
    
    'ATTR_ESTADO', 'ATTR_BRILLO', 'ATTR_COLOR', 'ATTR_MODO', 'ATTR_TEMP_OBJ', 'ATTR_TEMP_ACT', 
    'ATTR_POSICION', 'ATTR_HORA', 'ATTR_FECHA', 'ATTR_VOLUMEN', 'ATTR_MUTE', 'ATTR_MENSAJE', 
    'ATTR_EMAIL_NOTIF', 'ATTR_ACTIVADA',
    
    'NUMBER', 'TEMP', 'PERCENT', 'LUX', 'TIME_DURATION', 'HORA', 'FECHA', 'STRING', 'EMAIL',
    
    'EQUAL', 'NEGATE', 'GREATER', 'LESSER', 'GREAT_EQUAL', 'LESS_EQUAL', 'ASSIGN',
    
    'LPAREN', 'RPAREN'
]

PALABRAS_RESERVADAS = {
    "when": "WHEN",
    "every": "EVERY",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "do": "DO",
    "end": "END",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "true": "TRUE",
    "false": "FALSE",
    "on": "ON",
    "off": "OFF",
}

PREFIJOS_SENSOR = {
    "sensor_temp": "SENS_TEMP",
    "sensor_luz": "SENS_LUZ",
    "sensor_movimiento": "SENS_MOVIMIENTO",
    "sensor_humo": "SENS_HUMO",
    "sensor_humedad": "SENS_HUMEDAD",
}

PREFIJOS_ACTUADOR = {
    "foco_": "ACT_FOCO",
    "aire_": "ACT_AIRE",
    "persiana_": "ACT_PERSIANA",
    "cerradura_": "ACT_CERRADURA",
    "reloj_": "ACT_RELOJ",
    "altavoz_": "ACT_ALTAVOZ",
    "alarma_": "ACT_ALARMA",
}

ATRIBUTOS_VALIDOS = {
    ".estado": "ATTR_ESTADO",
    ".brillo": "ATTR_BRILLO",
    ".color": "ATTR_COLOR",
    ".modo": "ATTR_MODO",
    ".temp_obj": "ATTR_TEMP_OBJ",
    ".temp_act": "ATTR_TEMP_ACT",
    ".posicion": "ATTR_POSICION",
    ".hora": "ATTR_HORA",
    ".fecha": "ATTR_FECHA",
    ".volumen": "ATTR_VOLUMEN",
    ".mute": "ATTR_MUTE",
    ".mensaje": "ATTR_MENSAJE",
    ".email_notif": "ATTR_EMAIL_NOTIF",
    ".activada": "ATTR_ACTIVADA",
}

# Expresiones regulares simples
t_EQUAL = r'=='
t_NEGATE = r'!='
t_GREAT_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_GREATER = r'>'
t_LESSER = r'<'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Ignorar espacios y tabulaciones
t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMENTARIO(t):
    r'//.*'
    pass

def t_EMAIL(t):
    r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]+'
    parts = t.value.split('@')
    if len(parts) == 2:
        user, domain = parts
        if '.' in domain:
            ext = domain.rsplit('.', 1)[-1]
            if 2 <= len(ext) <= 4 and ext.isalpha():
                t.type = 'EMAIL'
                return t
    
    t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Email inválido '{t.value}'")
    pass

def t_FECHA(t):
    r'\d{2}/\d{2}/\d{4}|\d+/\d+/\d+'
    parts = t.value.split('/')
    if len(parts) == 3 and len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 4:
        dia, mes, anio = map(int, parts)
        if 1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= anio <= 2099:
            t.type = 'FECHA'
            return t
    t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Fecha inválida '{t.value}'")
    pass

def t_HORA(t):
    r'\d{2}:\d{2}|\d+:\d+'
    parts = t.value.split(':')
    if len(parts) == 2 and len(parts[0]) == 2 and len(parts[1]) == 2:
        hh, mm = map(int, parts)
        if 0 <= hh <= 23 and 0 <= mm <= 59:
            t.type = 'HORA'
            return t
    t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Hora inválida '{t.value}'")
    pass

def t_NUMBER_AND_UNITS(t):
    r'-?\d+(\.\d+)?([a-zA-Z°%]+)?'
    val = t.value
    num_part = ""
    unit_part = ""
    for i, c in enumerate(val):
        if c.isdigit() or c == '.' or (i == 0 and c == '-'):
            num_part += c
        else:
            unit_part = val[i:]
            break
            
    if not unit_part:
        t.type = 'NUMBER'
        return t
        
    unit_upper = unit_part.upper()
    if unit_upper == '%':
        num_val = int(num_part)
        if 0 <= num_val <= 100: 
            t.type = 'PERCENT'
            return t
        else:
            t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Valor de porcentaje fuera de rango (0-100): '{t.value}'")
            pass

    elif unit_upper == '°C':
        t.type = 'TEMP'
        return t
    elif unit_upper == '°':
        t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Unidad de temperatura incompleta '{t.value}'")
        pass
    elif unit_upper == 'LUX':
        num_val = int(num_part)
        if 0 <= num_val <= 1000: 
            t.type = 'LUX'
            return t
        else:
            t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Valor de iluminancia fuera de rango (0-1000): '{t.value}'")
            pass
    elif unit_upper in ['S', 'M', 'H']:
        t.type = 'TIME_DURATION'
        return t
    else:
        t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Unidad inválida '{unit_part}' en valor '{t.value}'")
        pass

def t_ATRIBUTO(t):
    r'\.[a-zA-Z0-9_]+'
    attr_key = t.value.lower()
    if attr_key in ATRIBUTOS_VALIDOS:
        t.type = ATRIBUTOS_VALIDOS[attr_key]
        return t
    t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Atributo desconocido '{t.value}'")
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    lexema_lower = t.value.lower()

    if lexema_lower in PALABRAS_RESERVADAS:
        t.type = PALABRAS_RESERVADAS[lexema_lower]
        return t

    if lexema_lower in ("blanco", "rojo", "azul"):
        t.type = 'COLOR'
        return t

    if lexema_lower in ("frio", "calor", "vent"):
        t.type = 'MODO'
        return t

    for prefijo, token_kind in PREFIJOS_SENSOR.items():
        if lexema_lower == prefijo or lexema_lower.startswith(prefijo + "_"):
            t.type = token_kind
            return t

    for prefijo, token_kind in PREFIJOS_ACTUADOR.items():
        if lexema_lower.startswith(prefijo):
            t.type = token_kind
            return t

    t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Identificador no reconocido '{t.value}'")
    pass

def t_STRING(t):
    r'["“][^"”\n]*["”]'
    return t

def t_UNCLOSED_STRING(t):
    r'["“][^"”\n]*\n'
    t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Cadena sin cerrar antes del fin de línea")
    t.lexer.lineno += 1
    pass

def t_error(t):
    t.lexer.errors.append(f"\033[91mError Léxico\033[0m en línea {t.lexer.lineno}: Carácter no reconocido '{t.value[0]}'")
    t.lexer.skip(1)

# Parcheamos el repr de LexToken para que se imprima lindo en consola
from ply.lex import LexToken
def token_repr(self):
    return f"\033[92mToken\033[0m(\033[93m{self.type}\033[0m, \033[96m'{self.value}'\033[0m, línea={self.lineno}, col={getattr(self, 'col', self.lexpos)})"

LexToken.__repr__ = token_repr
LexToken.__str__ = token_repr

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.lexer = lex.lex()
        self.lexer.errors = []
        self.errors = self.lexer.errors
        self._tokens_list = []
        self._token_index = 0

    def input(self, data):
        self._token_index = 0

    def tokenize(self):
        self.lexer.input(self.source)
        self.lexer.lineno = 1
        self._tokens_list = []
        
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            
            last_cr = self.source.rfind('\n', 0, tok.lexpos)
            if last_cr < 0:
                last_cr = -1
            tok.col = (tok.lexpos - last_cr)
            
            self._tokens_list.append(tok)
            
        return self._tokens_list

    def token(self):
        if not self._tokens_list and not self.errors:
            self.tokenize()
            
        if self._token_index < len(self._tokens_list):
            tok = self._tokens_list[self._token_index]
            self._token_index += 1
            return tok
        return None
