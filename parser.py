import ply.yacc as yacc
from tok import TokenKind

tokens = [kind.name for kind in TokenKind if kind not in (TokenKind.EOF, TokenKind.ERROR)]

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

def p_programa(p):
    "programa : instrucciones"
    p[0] = f"<html>\n<head><title>Smart Home</title></head>\n<body>\n{p[1]}\n</body>\n</html>"

def p_instrucciones(p):
    """instrucciones : instruccion
                     | instrucciones instruccion"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + "\n" + p[2]

def p_instruccion(p):
    """instruccion : asignacion
                   | bloque_when"""
    p[0] = p[1]

def p_asignacion(p):
    "asignacion : ACTUATOR ATTRIBUTE ASSIGN valor"
    # Acciones semánticas directas: generamos el HTML en lugar de un AST
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
    
    html = f'  <div style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul>\n'
    html += f'      <li>{atributo} = {valor}</li>\n'
    html += f'    </ul>\n'
    html += f'  </div>'
    
    p[0] = html

def p_valor(p):
    """valor : NUMBER
             | TEMP
             | PERCENT
             | LUX
             | TIME_DURATION
             | HORA
             | FECHA
             | STRING
             | EMAIL
             | TRUE
             | FALSE
             | ON
             | OFF
             | COLOR
             | MODO"""
    p[0] = p[1]

def p_bloque_when(p):
    "bloque_when : WHEN condicion DO instrucciones END"
    # El bloque WHEN agrupa la condición y las acciones anidadas
    html = f'<div class="when-block" style="margin-bottom: 20px; padding: 10px; border-left: 4px solid blue;">\n'
    html += f'  <h3 style="color: blue;">WHEN (Evento)</h3>\n'
    html += f'  {p[2]}\n'
    html += f'  <h3 style="color: blue;">DO (Acciones)</h3>\n'
    html += f'  <div style="margin-left: 20px;">\n{p[4]}\n  </div>\n'
    html += f'</div>'
    p[0] = html

def p_condicion(p):
    """condicion : SENSOR operador_comp valor"""
    sensor = p[1]
    operador = p[2]
    valor = p[3]
    
    # <div> verde para sensores como dice el documento
    html = f'  <div style="border: 1px solid green; padding: 20px; margin-bottom: 10px;">\n'
    html += f'    <h2>{sensor}</h2>\n'
    html += f'    <p>Condición: {operador} {valor}</p>\n'
    html += f'  </div>'
    p[0] = html

def p_condicion_actuador(p):
    """condicion : ACTUATOR ATTRIBUTE operador_comp valor"""
    actuador = p[1]
    atributo = p[2]
    operador = p[3]
    valor = p[4]
    
    html = f'  <div style="border: 1px solid green; padding: 20px; margin-bottom: 10px;">\n'
    html += f'    <h2>{actuador}{atributo}</h2>\n'
    html += f'    <p>Condición: {operador} {valor}</p>\n'
    html += f'  </div>'
    p[0] = html

def p_condicion_logica(p):
    """condicion : condicion AND condicion
                 | condicion OR condicion"""
    html = p[1]
    html += f'  <div style="text-align: center; font-weight: bold; margin: 10px;">{p[2]}</div>\n'
    html += p[3]
    p[0] = html

def p_condicion_bool(p):
    """condicion : TRUE
                 | FALSE"""
    p[0] = f'<p>Condición: {p[1]}</p>'

def p_operador_comp(p):
    """operador_comp : EQUAL
                     | NEGATE
                     | GREATER
                     | LESSER
                     | GREAT_EQUAL
                     | LESS_EQUAL"""
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (línea {p.lineno}, columna {p.lexpos})")
    else:
        print("Error de sintaxis: Fin de archivo inesperado")

parser = yacc.yacc()
