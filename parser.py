import ply.yacc as yacc
from tok import TokenKind
#DICCIONARIO CON TODA LA SEMANTICA
from semantica import REGLAS_ACTUADORES
from semantica import REGLAS_SENSORES

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
                | bloque_if
                | bloque_every"""
    p[0] = p[1]

def p_asignacion(p):
    "asignacion : ACTUATOR ATTRIBUTE ASSIGN valor"
    # Acciones semánticas directas: generamos el HTML en lugar de un AST
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
    
    #SEMANTICA
    prefijo = actuador.split("_")[0] + "_"

    if prefijo in REGLAS_ACTUADORES:
        reglas = REGLAS_ACTUADORES[prefijo]
        
        # 1. Validar que el atributo exista en este actuador
        if atributo not in reglas:
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El {prefijo} no soporta el atributo {atributo}</div>"
            return

        regla_atributo = reglas[atributo]
        
        # 2. Validar que NO sea de solo lectura (Write permissions)
        if regla_atributo["permiso"] == "R":
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El atributo {atributo} de {prefijo} es de SOLO LECTURA y no puede modificarse.</div>"
            return

        # 3. Validar el tipo de dato
        tipo_esperado = regla_atributo["valores"] 

        if isinstance(tipo_esperado, list):
            if valor not in tipo_esperado:
                p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: {atributo} debe ser uno de {tipo_esperado}</div>"
                return

        elif tipo_esperado == "porcentaje": 
            if not str(valor).endswith("%"):
                p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: {atributo} requiere un porcentaje (%)</div>"
                return
            #rangos de valores
            if "rango" in regla_atributo: 
                min_val,max_val = regla_atributo["rango"]
                num=float(str(valor).replace("%",""))
                if not (min_val <= num <= max_val):
                    p[0] = f"<div style='color:red;'>Error Semántico: El valor de {atributo} debe estar entre {min_val}% y {max_val}%</div>"
                    return
                    
        elif tipo_esperado == "temperatura": 
            if not str(valor).endswith("°C"):
                p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: {atributo} requiere una temperatura en grados Celsius (°C)</div>"
                return
            #rangos de valores
            if "rango" in regla_atributo: 
                min_val,max_val = regla_atributo["rango"]
                num = float(str(valor).replace("°C", ""))
                if not (min_val <= num <= max_val):
                    p[0] = f"<div style='color:red;'>Error Semántico: El valor de {atributo} debe estar entre {min_val}°C y {max_val}°C</div>"
                    return
    #fin semantica

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

def p_bloque_every(p):
    """bloque_every : EVERY HORA DO instrucciones END
                    | EVERY TIME_DURATION DO instrucciones END"""
    
    hora = p[2]
    instrucciones_do = p[4]
    
    html = f'<div class="every-block" style="margin-bottom: 20px; padding: 10px; border-left: 4px solid green;">\n'
    html += f'  <h3 style="color: green;">EVERY</h3>\n'
    html += f'  {hora}\n'
    html += f'  <h3 style="color: green;">DO</h3>\n'
    html += f'  <div style="margin-left: 20px;">\n{instrucciones_do}\n  </div>\n'
    html += f'</div>'
    
    p[0] = html

def p_bloque_when(p):
    "bloque_when : WHEN condicion DO instrucciones END"
    
    condicion = p[2]
    instrucciones_do = p[4]

    html = f'<div class="when-block" style="margin-bottom: 20px; padding: 10px; border-left: 4px solid blue;">\n'
    html += f'  <h3 style="color: blue;">WHEN</h3>\n'
    html += f'  {condicion}\n'
    html += f'  <h3 style="color: blue;">DO</h3>\n'
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
        html += f'  <h3 style="color: orange;">IF</h3>\n'
        html += f'  {condicion}\n'
        html += f'  <h3 style="color: orange;">THEN</h3>\n'
        html += f'  <div style="margin-left: 20px;">\n{instrucciones_then}\n  </div>\n'
        html += f'</div>'
        p[0] = html

    elif len(p) == 8:
        instrucciones_else = p[6]
        html = f'<div class="if-block" style="margin-bottom: 20px; padding: 10px; border-left: 4px solid orange;">\n'
        html += f'  <h3 style="color: orange;">IF</h3>\n'
        html += f'  {condicion}\n'
        html += f'  <h3 style="color: orange;">THEN</h3>\n'
        html += f'  <div style="margin-left: 20px;">\n{instrucciones_then}\n  </div>\n'
        html += f'  <h3 style="color: orange;">ELSE</h3>\n'
        html += f'  <div style="margin-left: 20px;">\n{instrucciones_else}\n  </div>\n'
        html += f'</div>'
        p[0] = html

# <condition> → <unit_logic> | <unit_logic> AND <condition> | <unit_logic> OR <condition>
# <unit_logic> → NOT <unit_logic> | ( <condition> ) | <comparison>

def p_condicion(p):
    """condicion : unit_logic
                | unit_logic AND condicion
                | unit_logic OR condicion"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        html = p[1]
        html += f' <div style="font-weight: bold; margin: 10px;">{p[2]}</div>\n'
        html += p[3]
        p[0] = html

def p_unit_logic(p):
    """unit_logic : NOT unit_logic
                | LPAREN condicion RPAREN
                | comparison"""
    if len(p) == 2:
        # comparison
        p[0] = p[1]
    elif len(p) == 3:
        # NOT unit_logic
        unit = p[2]
        html = f'<div style="font-weight: bold; margin: 10px;">NOT</div>\n'
        html += unit
        p[0] = html
    elif len(p) == 4:
        # LPAREN condicion RPAREN
        cond = p[2]
        html = f'<div style="border: 1px dashed gray; padding: 10px; margin-bottom: 10px;">\n'
        html += cond
        html += f'</div>'
        p[0] = html

def p_comparison_sensor(p):
    """comparison : SENSOR operador_comp valor"""
    sensor = p[1]
    operador = p[2]
    valor = p[3]

    #SEMANTICA
    if sensor in REGLAS_SENSORES:
        regla_sensor = REGLAS_SENSORES[sensor]

        # 2. Validar el tipo de dato
        tipo_esperado = regla_sensor["tipo"] 

        if isinstance(tipo_esperado, list):
            if valor not in tipo_esperado:
                p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: {sensor} debe ser uno de {tipo_esperado}</div>"
                return

        elif tipo_esperado == "porcentaje": 
            if not str(valor).endswith("%"):
                p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: {sensor} requiere un porcentaje (%)</div>"
                return
            #rangos de valores
            if "rango" in regla_sensor: 
                min_val,max_val = regla_sensor["rango"]
                num=float(str(valor).replace("%",""))
                if not (min_val <= num <= max_val):
                    p[0] = f"<div style='color:red;'>Error Semántico: El valor de {sensor} debe estar entre {min_val}% y {max_val}%</div>"
                    return
                    
        elif tipo_esperado == "temperatura": 
            if not str(valor).endswith("°C"):
                p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: {sensor} requiere una temperatura en grados Celsius (°C)</div>"
                return
            #rangos de valores
            if "rango" in regla_sensor: 
                min_val,max_val = regla_sensor["rango"]
                num = float(str(valor).replace("°C", ""))
                if not (min_val <= num <= max_val):
                    p[0] = f"<div style='color:red;'>Error Semántico: El valor de {sensor} debe estar entre {min_val}°C y {max_val}°C</div>"
                    return
    #fin semantica
    
    html = f'  <div style="border: 1px solid green; padding: 20px; margin-bottom: 10px;">\n'
    html += f'    <h2>{sensor}</h2>\n'
    html += f'    <p>Condición: {operador} {valor}</p>\n'
    html += f'  </div>'
    p[0] = html

def p_comparison_actuador(p):
    """comparison : ACTUATOR ATTRIBUTE operador_comp valor"""
    actuador = p[1]
    atributo = p[2]
    operador = p[3]
    valor = p[4]
    
    html = f'  <div style="border: 1px solid green; padding: 20px; margin-bottom: 10px;">\n'
    html += f'    <h2>{actuador}{atributo}</h2>\n'
    html += f'    <p>Condición: {operador} {valor}</p>\n'
    html += f'  </div>'
    p[0] = html

def p_comparison_bool(p):
    """comparison : TRUE
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
