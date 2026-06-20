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

    SENSOR = auto()
    ACTUATOR = auto()
    ATTRIBUTE = auto()

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

PREFIJOS_SENSOR = (
    "sensor_temp",
    "sensor_luz",
    "sensor_movimiento",
    "sensor_humo",
    "sensor_humedad",
)

PREFIJOS_ACTUADOR = (
    "foco_",
    "aire_",
    "persiana_",
    "cerradura_",
    "reloj_",
    "altavoz_",
    "alarma_",
)

ATRIBUTOS_VALIDOS = {
    ".estado",
    ".brillo",
    ".color",
    ".modo",
    ".temp_obj",
    ".temp_act",
    ".posicion",
    ".hora",
    ".fecha",
    ".volumen",
    ".mute",
    ".mensaje",
    ".email_notif",
    ".activada",
}
