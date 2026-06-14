from lex import Lexer
from parser import parser

codigo = """
WHEN sensor_luz < 250lux DO  
  foco_entrada.estado = ON  
  foco_entrada.brillo = 80%  
END
"""

print(f"Probando código:\n>>> {codigo}\n")

mi_lexer = Lexer(codigo)

# Le pasamos nuestro lexer personalizado a PLY
resultado = parser.parse(lexer=mi_lexer)

print("Resultado del Parser (HTML Generado):")
print(resultado)
