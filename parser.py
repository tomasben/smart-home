"""
∑ → <program>
<program> → <instruction> | <instruction> <new_line> <program>

<instruction> → <control_when> | <control_every> | <conditional> | <assignment>

<control_when> → when <condition> do <new_line> <action> <new_line> end
<control_every> → every <tk_val_time> do <new_line> <action> <new_line> end
<conditional> → if <condition> then <new_line> <action> <new_line> else <new_line><action> <new_line> end
                | if <condition> then <new_line> <action> <new_line> end

<condition> → <unit_logic> | <unit_logic> AND <condition> | <unit_logic> OR <condition>
<unit_logic> → NOT <unit_logic> | ( <condition> ) | <comparison>

<temp_sens> → sensor_temp_ <tk_suffix> | sensor_temp
<luz_sens> → sensor_luz_ <tk_suffix> | sensor_luz

<mov_sens> → sensor_movimiento_ <tk_suffix> | sensor_movimiento
<humo_sens> → sensor_humo_ <tk_suffix> | sensor_humo
<humedad_sens> → sensor_humedad_ <tk_suffix> | sensor_humedad

<comparison> → <comparison_sens_temp>
                    | <comparison_sens_humedad>
                    | <comparison_sens_luz>
                    | <comparison_sens_mov>
                    | <comparison_sens_humo>
                    | <comparison_foco>
                    | <comparison_aire>
                    | <comparison_persiana>
                    | <comparison_cerradura>
                    | <comparison_reloj>
                    | <comparison_altavoz>
                    | <comparison_alarma>

<comparison_sens_temp> → <temp_sens> <tk_rel_op> <tk_val_num> °C
<comparison_sens_humedad> → <humedad_sens> <tk_rel_op> <tk_val_num> %
<comparison_sens_luz> → <luz_sens> <tk_rel_op> <tk_val_num> lux
<comparison_sens_mov> → <mov_sens> == <tk_val_bool_sens>
                    | <mov_sens> != <tk_val_bool_sens>
<comparison_sens_humo> → <humo_sens> == <tk_val_bool_sens>
                    | <humo_sens> != <tk_val_bool_sens>

<comparison_foco> → <actuator_foco> .estado == <tk_val_bool>
                    | <actuator_foco> .estado != <tk_val_bool>
                    | <actuator_foco> .brillo <tk_rel_op> <tk_val_num> %
                    | <actuator_foco> .color == <tk_val_color>
                    | <actuator_foco> .color != <tk_val_color>
<comparison_aire> → <actuator_aire> .estado == <tk_val_bool>
                    | <actuator_aire> .estado != <tk_val_bool>
                    | <actuator_aire> .modo == <tk_val_mode>
                    | <actuator_aire> .modo != <tk_val_mode>
                    | <actuator_aire> .temp_obj <tk_rel_op> <tk_val_num> °C
                    | <actuator_aire> .temp_act <tk_rel_op> <tk_val_num> °C
<comparison_persiana> → <actuator_persiana> .posicion <tk_rel_op> <tk_val_num> %
<comparison_cerradura> → <actuator_cerradura> .estado == <tk_val_bool>
                        | <actuator_cerradura> .estado != <tk_val_bool>
<comparison_reloj> → <actuator_reloj> .hora <tk_rel_op> <tk_val_time>
                        | <actuator_reloj> .fecha <tk_rel_op> <tk_val_date>
<comparison_altavoz> → <actuator_altavoz> .volumen <tk_rel_op> <tk_val_num> %
                        | <actuator_altavoz>.mute == <tk_val_bool>
                        | <actuator_altavoz>.mute != <tk_val_bool>
                        | <actuator_altavoz>.mensaje == <tk_val_string>
                        | <actuator_altavoz>.mensaje != <tk_val_string>
                        | <actuator_altavoz>.email_notif == <tk_val_email>
                        | <actuator_altavoz> .email_notif != <tk_val_email>
<comparison_alarma> → <actuator_alarma> .estado == <tk_val_bool>
                        | <actuator_alarma> .estado != <tk_val_bool>
                        | <actuator_alarma> .activada == <tk_val_bool>
                        | <actuator_alarma> .activada != <tk_val_bool>

<action> → <unit_action> | <unit_action> <new_line> <action>
<unit_action> → <assignment> | <conditional>
<assignment> → <assign_foco>
                | <assign_aire>
                | <assign_persiana>
                | <assign_cerradura>
                | <assign_altavoz>
                | <assign_alarma>
<actuator_reloj> → reloj_ <tk_suffix> | reloj_
<actuator_foco> → foco_ <tk_suffix> | foco_
<assign_foco> → <actuator_foco> .estado = <tk_val_bool>
                | <actuator_foco> .brillo = <tk_val_num> %
                | <actuator_foco> .color = <tk_val_color>
<actuator_aire> → aire_ <tk_suffix> | aire_
<assign_aire> → <actuator_aire> .estado = <tk_val_bool>
                | <actuator_aire> .modo = <tk_val_mode>
                | <actuator_aire> .temp_obj = <tk_val_num> °C
<actuator_persiana> → persiana_ <tk_suffix> | persiana_
<assign_persiana> → <actuator_persiana> .posicion = <tk_val_num> %
<actuator_cerradura> → cerradura_ <tk_suffix> | cerradura_
<assign_cerradura> → <actuator_cerradura> .estado = <tk_val_bool>
<actuator_altavoz> → altavoz_ <tk_suffix> | altavoz_
<assign_altavoz> → <actuator_altavoz> .volumen = <tk_val_num> %
                | <actuator_altavoz> .mute = <tk_val_bool>
                | <actuator_altavoz> .mensaje = <tk_val_string>
                | <actuator_altavoz> .email_notif = <tk_val_email>
<actuator_alarma> → alarma_ <tk_suffix> | alarma_
<assign_alarma> → <actuator_alarma> .estado = <tk_val_bool>
                | <actuator_alarma> .activada = <tk_val_bool>
"""

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

#--------------------ASIGNACIONES--------------------
#foco
def p_asignacion_foco(p):
    """asignacion : ACT_FOCO ATTR_ESTADO ASSIGN ON
                  | ACT_FOCO ATTR_ESTADO ASSIGN OFF
                  | ACT_FOCO ATTR_BRILLO ASSIGN PERCENT
                  | ACT_FOCO ATTR_COLOR ASSIGN COLOR"""
    
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
    
    # 1. Validación Semántica (Ahora es súper corta, solo validamos el rango numérico)
    if atributo == ".brillo":
        num = float(str(valor).replace("%", ""))
        if not (0 <= num <= 100):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El brillo de {actuador} debe estar entre 0% y 100%</div>"
            return
            
    # 2. Generación HTML
    html = f'  <div style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li>{atributo} = {valor}</li></ul>\n'
    html += f'  </div>'
    p[0] = html
#aire
def p_asignacion_aire(p):
    """asignacion : ACT_AIRE ATTR_ESTADO ASSIGN ON
                  | ACT_AIRE ATTR_ESTADO ASSIGN OFF
                  | ACT_AIRE ATTR_MODO ASSIGN MODO
                  | ACT_AIRE ATTR_TEMP_OBJ ASSIGN TEMP"""
                  
    actuador = p[1]
    atributo = p[2]
    valor = p[4]

    if atributo == ".temp_obj":
        num = float(str(valor).replace("°C", ""))
        if not (16 <= num <= 30):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La temperatura objetivo debe estar entre 16°C y 30°C</div>"
            return
            
    html = f'  <div style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li>{atributo} = {valor}</li></ul>\n'
    html += f'  </div>'
    p[0] = html
#persiana 
def p_asignacion_persiana(p):
    """asignacion : ACT_PERSIANA ATTR_POSICION ASSIGN PERCENT"""
    
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
    
    # 1. Validación Semántica (Ahora es súper corta, solo validamos el rango numérico)
    if atributo == ".posicion":
        num = float(str(valor).replace("%", ""))
        if not (0 <= num <= 100):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La posicion de {actuador} debe estar entre 0% y 100%</div>"
            return
            
    # 2. Generación HTML
    html = f'  <div style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li>{atributo} = {valor}</li></ul>\n'
    html += f'  </div>'
    p[0] = html
#ceradura
def p_asignacion_cerradura(p):
    """asignacion : ACT_CERRADURA ATTR_ESTADO ASSIGN ON
                  | ACT_CERRADURA ATTR_ESTADO ASSIGN OFF"""
                  
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
            
    html = f'  <div style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li>{atributo} = {valor}</li></ul>\n'
    html += f'  </div>'
    p[0] = html
#altavoz
def p_asignacion_altavoz(p):
    """asignacion : ACT_ALTAVOZ ATTR_VOLUMEN ASSIGN PERCENT
                    | ACT_ALTAVOZ ATTR_MUTE ASSIGN ON
                    | ACT_ALTAVOZ ATTR_MUTE ASSIGN OFF
                    | ACT_ALTAVOZ ATTR_MENSAJE ASSIGN STRING
                    | ACT_ALTAVOZ ATTR_EMAIL_NOTIF ASSIGN EMAIL"""
    
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
    
    # 1. Validación Semántica (Ahora es súper corta, solo validamos el rango numérico)
    if atributo == ".volumen":
        num = float(str(valor).replace("%", ""))
        if not (0 <= num <= 100):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El volumen de {actuador} debe estar entre 0% y 100%</div>"
            return

    # 2. Generación HTML
    html = f'  <div style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li>{atributo} = {valor}</li></ul>\n'
    html += f'  </div>'
    p[0] = html
#alarma
def p_asignacion_alarma(p):
    """asignacion : ACT_ALARMA ATTR_ESTADO ASSIGN ON
                  | ACT_ALARMA ATTR_ESTADO ASSIGN OFF
                  | ACT_ALARMA ATTR_ACTIVADA ASSIGN ON
                  | ACT_ALARMA ATTR_ACTIVADA ASSIGN OFF"""
                  
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
            
    html = f'  <div style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li>{atributo} = {valor}</li></ul>\n'
    html += f'  </div>'
    p[0] = html

#--------------------FIN DE LAS ASIGNACIONES--------------------

#--------------------FUNCIONES DE BLOQUES--------------------
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

#SENSOR TEMPERATURA
def p_comparison_sensor_temp(p):
    """comparison : SENS_TEMP operador_comp TEMP"""
    sensor = p[1]
    operador = p[2]
    valor = p[3]
    
    num = float(str(valor).replace("°C", ""))
    if not (-10 <= num <= 50):
        p[0] = f"<div style='color:red;'>Error Semántico: Valor de temperatura fuera de rango (-10° a 50°)</div>"
        return
        
    p[0] = f'<div style="border:1px solid green; padding: 20px;"><h2>{sensor}</h2><p>Condición: {operador} {valor}</p></div>'

#SENSOR HUMEDAD
def p_comparison_sensor_humedad(p):
    """comparison : SENS_HUMEDAD operador_comp PERCENT"""
    sensor = p[1]
    operador = p[2]
    valor = p[3]
    
    num = float(str(valor).replace("%", ""))
    if not (0 <= num <= 100):
        p[0] = f"<div style='color:red;'>Error Semántico: Valor de humedad fuera de rango (0% a 100%)</div>"
        return
        
    p[0] = f'<div style="border:1px solid green; padding: 20px;"><h2>{sensor}</h2><p>Condición: {operador} {valor}</p></div>'

#SENSOR LUZ
def p_comparison_sensor_luz(p):
    """comparison : SENS_LUZ operador_comp LUX"""

    sensor = p[1]
    operador = p[2]
    valor = p[3]
    
    num = float(str(valor).replace("lux", ""))
    if not (0 <= num <= 1000):
        p[0] = f"<div style='color:red;'>Error Semántico: Valor de Iluminancia fuera de rango (0lux a 1000lux)</div>"
        return
        
    p[0] = f'<div style="border:1px solid green; padding: 20px;"><h2>{sensor}</h2><p>Condición: {operador} {valor}</p></div>'

#SENSOR MOVIMIENTO
def p_comparison_sensor_mov(p):
    """comparison : SENS_MOVIMIENTO EQUAL TRUE
                  | SENS_MOVIMIENTO EQUAL FALSE
                  | SENS_MOVIMIENTO NEGATE TRUE
                  | SENS_MOVIMIENTO NEGATE FALSE"""
    sensor = p[1]
    operador = p[2]
    valor = p[3]

    p[0] = f'<div style="border:1px solid green; padding: 20px;"><h2>{p[1]}</h2><p>Condición: {p[2]} {p[3]}</p></div>'

#SENSOR HUMO
def p_comparison_sensor_humo(p):
    """comparison : SENS_HUMO EQUAL TRUE
                  | SENS_HUMO EQUAL FALSE
                  | SENS_HUMO NEGATE TRUE
                  | SENS_HUMO NEGATE FALSE"""

    sensor = p[1]
    operador = p[2]
    valor = p[3]

    p[0] = f'<div style="border:1px solid green; padding: 20px;"><h2>{p[1]}</h2><p>Condición: {p[2]} {p[3]}</p></div>'

#---------------COMPARACIONES DE ACTUADORES---------------

# COMPARACIÓN PARA FOCO
def p_comparison_actuador_foco(p):
    """comparison : ACT_FOCO ATTR_ESTADO operador_comp ON
                  | ACT_FOCO ATTR_ESTADO operador_comp OFF
                  | ACT_FOCO ATTR_BRILLO operador_comp PERCENT
                  | ACT_FOCO ATTR_COLOR operador_comp COLOR"""
    
    actuador = p[1]
    atributo = p[2]
    operador = p[3]
    valor = p[4]
    
    if atributo in [".estado", ".color"]:
        if operador not in ["==", "!="]:
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: No puedes usar '{operador}' en {atributo}. Usa == o !=</div>"
            return
    elif atributo == ".brillo":
        num = float(str(valor).replace("%", ""))
        if not (0 <= num <= 100):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El brillo de {actuador} debe estar entre 0% y 100%</div>"
            return
            
    p[0] = f'<div style="border:1px solid green; padding:20px;"><h2>{actuador}{atributo}</h2><p>Condición: {operador} {valor}</p></div>'

# COMPARACIÓN PARA AIRE (Incluye la temperatura actual que es de solo lectura)
def p_comparison_actuador_aire(p):
    """comparison : ACT_AIRE ATTR_ESTADO operador_comp ON
                  | ACT_AIRE ATTR_ESTADO operador_comp OFF
                  | ACT_AIRE ATTR_MODO operador_comp MODO
                  | ACT_AIRE ATTR_TEMP_OBJ operador_comp TEMP
                  | ACT_AIRE ATTR_TEMP_ACT operador_comp TEMP"""
                  
    actuador = p[1]
    atributo = p[2]
    operador = p[3]
    valor = p[4]
    
    if atributo in [".estado", ".modo"]:
        if operador not in ["==", "!="]:
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: No puedes usar '{operador}' en {atributo}. Usa == o !=</div>"
            return
    elif atributo == ".temp_obj":
        num = float(str(valor).replace("°C", ""))
        if not (16 <= num <= 30):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La temperatura objetivo debe estar entre 16°C y 30°C</div>"
            return
    elif atributo == ".temp_act":
        num = float(str(valor).replace("°C", ""))
        if not (-10 <= num <= 50):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La temperatura actual debe estar entre -10°C y 50°C</div>"
            return
            
    p[0] = f'<div style="border:1px solid green; padding:20px;"><h2>{actuador}{atributo}</h2><p>Condición: {operador} {valor}</p></div>'

# COMPARACIÓN PARA PERSIANA 
def p_comparison_actuador_persiana(p):
    """comparison : ACT_PERSIANA ATTR_POSICION operador_comp PERCENT"""
    
    actuador = p[1]
    atributo = p[2]
    operador = p[3]
    valor = p[4]
    
    if atributo == ".posicion":
        num = float(str(valor).replace("%", ""))
        if not (0 <= num <= 100):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La posición debe estar entre 0% y 100%</div>"
            return
            
    p[0] = f'<div style="border:1px solid green; padding:20px;"><h2>{actuador}{atributo}</h2><p>Condición: {operador} {valor}</p></div>'

# COMPARACIÓN PARA CERRADURA 
def p_comparison_actuador_cerradura(p):
    """comparison : ACT_CERRADURA ATTR_ESTADO operador_comp ON
                  | ACT_CERRADURA ATTR_ESTADO operador_comp OFF"""
    
    actuador = p[1]
    atributo = p[2]
    operador = p[3]
    valor = p[4]
    
    if operador not in ["==", "!="]:
        p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: No puedes usar '{operador}' en {atributo}. Usa == o !=</div>"
        return
            
    p[0] = f'<div style="border:1px solid green; padding:20px;"><h2>{actuador}{atributo}</h2><p>Condición: {operador} {valor}</p></div>'

# COMPARACIÓN PARA RELOJ 
def p_comparison_actuador_reloj(p):
    """comparison : ACT_RELOJ ATTR_HORA operador_comp HORA
                  | ACT_RELOJ ATTR_FECHA operador_comp FECHA"""
    
    p[0] = f'<div style="border:1px solid green; padding:20px;"><h2>{p[1]}{p[2]}</h2><p>Condición: {p[3]} {p[4]}</p></div>'

# COMPARACIÓN PARA ALTAVOZ 
def p_comparison_actuador_altavoz(p):
    """comparison : ACT_ALTAVOZ ATTR_VOLUMEN operador_comp PERCENT
                  | ACT_ALTAVOZ ATTR_MUTE operador_comp ON
                  | ACT_ALTAVOZ ATTR_MUTE operador_comp OFF
                  | ACT_ALTAVOZ ATTR_MENSAJE operador_comp STRING
                  | ACT_ALTAVOZ ATTR_EMAIL_NOTIF operador_comp EMAIL"""
    
    actuador = p[1]
    atributo = p[2]
    operador = p[3]
    valor = p[4]
    
    if atributo in [".mute", ".mensaje", ".email_notif"]:
        if operador not in ["==", "!="]:
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: No puedes usar '{operador}' en {atributo}. Usa == o !=</div>"
            return
    elif atributo == ".volumen":
        num = float(str(valor).replace("%", ""))
        if not (0 <= num <= 100):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El volumen debe estar entre 0% y 100%</div>"
            return
            
    p[0] = f'<div style="border:1px solid green; padding:20px;"><h2>{actuador}{atributo}</h2><p>Condición: {operador} {valor}</p></div>'

# COMPARACIÓN PARA ALARMA 
def p_comparison_actuador_alarma(p):
    """comparison : ACT_ALARMA ATTR_ACTIVADA operador_comp ON
                  | ACT_ALARMA ATTR_ACTIVADA operador_comp OFF
                  | ACT_ALARMA ATTR_ESTADO operador_comp ON
                  | ACT_ALARMA ATTR_ESTADO operador_comp OFF"""
    
    actuador = p[1]
    atributo = p[2]
    operador = p[3]
    valor = p[4]
    
    if operador not in ["==", "!="]:
        p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: No puedes usar '{operador}' en {atributo}. Usa == o !=</div>"
        return
            
    p[0] = f'<div style="border:1px solid green; padding:20px;"><h2>{actuador}{atributo}</h2><p>Condición: {operador} {valor}</p></div>'

#---------------FIN DE LAS COMPARACIONES---------------

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
