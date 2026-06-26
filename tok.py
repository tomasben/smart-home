from dataclasses import dataclass
from enum import Enum, auto

RESET = "\033[0m"
DIM = "\033[2m"
BLUE = "\033[94m"


class TokenKind(Enum):
    WHEN = auto()
    EVERY = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    DO = auto()
    END = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    TRUE = auto()
    FALSE = auto()
    ON = auto()
    OFF = auto()

    MODO = auto()
    COLOR = auto()

    # === ACTUADORES ESPECÍFICOS ===
    ACT_FOCO = auto()
    ACT_AIRE = auto()
    ACT_PERSIANA = auto()
    ACT_CERRADURA = auto()
    ACT_RELOJ = auto()
    ACT_ALTAVOZ = auto()
    ACT_ALARMA = auto()

    # === SENSORES ESPECÍFICOS ===
    SENS_TEMP = auto()
    SENS_HUMEDAD = auto()
    SENS_LUZ = auto()
    SENS_MOVIMIENTO = auto()
    SENS_HUMO = auto()

    # === ATRIBUTOS ESPECÍFICOS ===
    ATTR_ESTADO = auto()
    ATTR_BRILLO = auto()
    ATTR_COLOR = auto()
    ATTR_MODO = auto()
    ATTR_TEMP_OBJ = auto()
    ATTR_TEMP_ACT = auto()
    ATTR_POSICION = auto()
    ATTR_HORA = auto()
    ATTR_FECHA = auto()
    ATTR_VOLUMEN = auto()
    ATTR_MUTE = auto()
    ATTR_MENSAJE = auto()
    ATTR_EMAIL_NOTIF = auto()
    ATTR_ACTIVADA = auto()


    NUMBER = auto()
    TEMP = auto()
    PERCENT = auto()
    LUX = auto()
    TIME_DURATION = auto()
    HORA = auto()
    FECHA = auto()
    STRING = auto()
    EMAIL = auto()

    EQUAL = auto()
    NEGATE = auto()
    GREATER = auto()
    LESSER = auto()
    GREAT_EQUAL = auto()
    LESS_EQUAL = auto()
    ASSIGN = auto()

    LPAREN = auto()
    RPAREN = auto()

    EOF = auto()
    ERROR = auto()


@dataclass
class Token:
    kind: TokenKind
    src: str
    row: int
    col: int

    @property
    def type(self):
        return self.kind.name

    @property
    def value(self):
        return self.src

    @property
    def lineno(self):
        return self.row

    @property
    def lexpos(self):
        return self.col

    def __str__(self):
        return f"{BLUE}{self.kind.name}{RESET}"

    def __repr__(self):
        return f"\033[92mToken\033[0m(\033[93m{self.kind.name}\033[0m, \033[96m'{self.src}'\033[0m, línea={self.row}, col={self.col})"


PALABRAS_RESERVADAS = {
    "when": TokenKind.WHEN,
    "every": TokenKind.EVERY,
    "if": TokenKind.IF,
    "then": TokenKind.THEN,
    "else": TokenKind.ELSE,
    "do": TokenKind.DO,
    "end": TokenKind.END,
    "and": TokenKind.AND,
    "or": TokenKind.OR,
    "not": TokenKind.NOT,
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
    "on": TokenKind.ON,
    "off": TokenKind.OFF,
}

PREFIJOS_SENSOR = {
    "sensor_temp": TokenKind.SENS_TEMP,
    "sensor_luz": TokenKind.SENS_LUZ,
    "sensor_movimiento": TokenKind.SENS_MOVIMIENTO,
    "sensor_humo": TokenKind.SENS_HUMO,
    "sensor_humedad": TokenKind.SENS_HUMEDAD,
}

PREFIJOS_ACTUADOR = {
    "foco_": TokenKind.ACT_FOCO,
    "aire_": TokenKind.ACT_AIRE,
    "persiana_": TokenKind.ACT_PERSIANA,
    "cerradura_": TokenKind.ACT_CERRADURA,
    "reloj_": TokenKind.ACT_RELOJ,
    "altavoz_": TokenKind.ACT_ALTAVOZ,
    "alarma_": TokenKind.ACT_ALARMA,
}

ATRIBUTOS_VALIDOS = {
    ".estado": TokenKind.ATTR_ESTADO,
    ".brillo": TokenKind.ATTR_BRILLO,
    ".color": TokenKind.ATTR_COLOR,
    ".modo": TokenKind.ATTR_MODO,
    ".temp_obj": TokenKind.ATTR_TEMP_OBJ,
    ".temp_act": TokenKind.ATTR_TEMP_ACT,
    ".posicion": TokenKind.ATTR_POSICION,
    ".hora": TokenKind.ATTR_HORA,
    ".fecha": TokenKind.ATTR_FECHA,
    ".volumen": TokenKind.ATTR_VOLUMEN,
    ".mute": TokenKind.ATTR_MUTE,
    ".mensaje": TokenKind.ATTR_MENSAJE,
    ".email_notif": TokenKind.ATTR_EMAIL_NOTIF,
    ".activada": TokenKind.ATTR_ACTIVADA,
}

