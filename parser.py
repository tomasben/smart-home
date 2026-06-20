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
                   | bloque_when
                   | bloque_if"""
    p[0] = p[1]

def p_asignacion(p):
    "asignacion : ACTUATOR ATTRIBUTE ASSIGN valor"
    # Acciones semánticas directas: generamos el HTML en lugar de un AST
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
    
    #SEMANTICA
    if atributo == ".estado" and valor not in ("ON", "OFF"):
        print(f"Error semantico en la linea {p.lineno(1)}: {atributo} solo acepta valores ON u OFF no puede tomar el valor {valor}")
        #acá hay que decidir qué hacer, capaz le preguntamos a vigil si cortamos todo el análisis o seguimos igual pero avisando qué hubo un error, de momento devuelve un error en el html en rojo y sigue todo, así no se rompe y podemos testear
        p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: {atributo} no acepta {valor}</div>"
        return

    elif atributo == ".brillo" and not valor.endswith("%"):
        print(f"Error semantico en la linea {p.lineno(1)}: {atributo} requiere un simbolo porcentaje (%) no puede tomar el valor {valor}")
        p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: {atributo} no acepta {valor}</div>"
        return
    #FIN DE LA SEMANTICA por ahora

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
    
    condicion = p[2]
    instrucciones_do = p[4]

    html = f'<div class="when-block" style="margin-bottom: 20px; padding: 10px; border-left: 4px solid blue;">\n'
    html += f'  <h3 style="color: blue;">WHEN (Evento)</h3>\n'
    html += f'  {condicion}\n'
    html += f'  <h3 style="color: blue;">DO (Acciones)</h3>\n'
    html += f'  <div style="margin-left: 20px;">\n{instrucciones_do}\n  </div>\n'
    html += f'</div>'
    
    p[0] = html


def p_bloque_if(p):
    """bloque_if : IF condicion THEN instrucciones END
                 | IF condicion THEN instrucciones ELSE instrucciones END"""
     
    condicion = p[2]  
    instrucciones_then = p[4] 
    if len(p) == 6:
        html = f'<div class="if-block" style="margin-bottom: 20px; padding: 10px; border-left: 4px solid orange;">\n'
        html += f'  <h3 style="color: orange;">IF (Condición)</h3>\n'
        html += f'  {condicion}\n'
        html += f'  <h3 style="color: orange;">THEN (Hacer esto)</h3>\n'
        html += f'  <div style="margin-left: 20px;">\n{instrucciones_then}\n  </div>\n'
        html += f'</div>'
        p[0] = html

    elif len(p) == 8:
        instrucciones_else = p[6]
        html = f'<div class="if-block" style="margin-bottom: 20px; padding: 10px; border-left: 4px solid orange;">\n'
        html += f'  <h3 style="color: orange;">IF (Condición)</h3>\n'
        html += f'  {condicion}\n'
        html += f'  <h3 style="color: orange;">THEN (Hacer esto)</h3>\n'
        html += f'  <div style="margin-left: 20px;">\n{instrucciones_then}\n  </div>\n'
        html += f'  <h3 style="color: red;">ELSE (Si no se cumple, hacer esto)</h3>\n'
        html += f'  <div style="margin-left: 20px;">\n{instrucciones_else}\n  </div>\n'
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
