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
from lex import tokens
from semantica import REGLAS_ACTUADORES, REGLAS_SENSORES

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

def p_programa(p):
    "programa : instrucciones"
    css = """<style>
  :root {
      --bg-color: #0b0f19;
      --text-color: #e2e8f0;
      --accent-green: #00ff88;
      --accent-gray: #94a3b8;
      --glow-green: rgba(0, 255, 136, 0.3);
      --glow-gray: rgba(148, 163, 184, 0.2);
      --card-bg: rgba(20, 25, 35, 0.8);
  }
  body {
      background-color: var(--bg-color);
      background-image: 
          radial-gradient(circle at 15% 50%, rgba(0, 255, 136, 0.05), transparent 25%),
          radial-gradient(circle at 85% 30%, rgba(56, 189, 248, 0.05), transparent 25%);
      color: var(--text-color);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 40px;
  }
  .dashboard-container {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 25px;
      max-width: 1400px;
      margin: 0 auto;
  }
  .sensor-card {
      background-color: var(--card-bg);
      backdrop-filter: blur(10px);
      border-radius: 12px;
      box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: center;
  }
  .sensor-card::before {
      content: "";
      position: absolute;
      top: 0; left: 0; width: 100%; height: 4px;
      background: var(--accent-green);
      box-shadow: 0 0 10px var(--accent-green);
  }
  .sensor-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 40px 0 var(--glow-green);
  }
  .sensor-card h2 {
      margin-top: 0;
      color: var(--accent-green);
      font-size: 1.4rem;
      border-bottom: 1px solid rgba(0, 255, 136, 0.2);
      padding-bottom: 10px;
      text-transform: uppercase;
      letter-spacing: 2px;
  }
  .actuator-card {
      background-color: var(--card-bg);
      backdrop-filter: blur(10px);
      border-radius: 12px;
      box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: center;
  }
  .actuator-card::before {
      content: "";
      position: absolute;
      top: 0; left: 0; width: 100%; height: 4px;
      background: var(--accent-gray);
      box-shadow: 0 0 10px var(--accent-gray);
  }
  .actuator-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 40px 0 var(--glow-gray);
  }
  .actuator-card h1 {
      margin-top: 0;
      color: #cbd5e1;
      font-size: 1.5rem;
      border-bottom: 1px solid rgba(148, 163, 184, 0.2);
      padding-bottom: 10px;
      text-transform: uppercase;
      letter-spacing: 2px;
  }
  .actuator-card ul {
      list-style-type: none;
      padding: 0;
      margin-bottom: 0;
  }
  .actuator-card ul li {
      background: rgba(255, 255, 255, 0.05);
      margin-top: 8px;
      padding: 12px 15px;
      border-radius: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'Consolas', monospace;
      color: #60a5fa;
  }
  a {
      color: #38bdf8;
      text-decoration: none;
      font-weight: bold;
      transition: color 0.2s, text-shadow 0.2s;
  }
  a:hover {
      color: #7dd3fc;
      text-shadow: 0 0 10px rgba(56, 189, 248, 0.8);
  }
  .block-container {
      grid-column: 1 / -1;
      background: linear-gradient(145deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9));
      border-radius: 16px;
      padding: 25px;
      margin-bottom: 10px;
      border: 1px solid rgba(255,255,255,0.05);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }
  .block-header {
      font-weight: bold;
      font-size: 1.2rem;
      letter-spacing: 2px;
      margin-bottom: 15px;
      display: flex;
      align-items: center;
      text-transform: uppercase;
  }
  .block-header::before {
      content: "";
      display: inline-block;
      width: 12px; height: 12px;
      border-radius: 50%;
      margin-right: 10px;
  }
  .if-header { color: #fbbf24; }
  .if-header::before { background-color: #fbbf24; box-shadow: 0 0 8px #fbbf24; }
  .when-header { color: #60a5fa; }
  .when-header::before { background-color: #60a5fa; box-shadow: 0 0 8px #60a5fa; }
  .every-header { color: #34d399; }
  .every-header::before { background-color: #34d399; box-shadow: 0 0 8px #34d399; }
  .block-content {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
      margin-top: 15px;
      padding-top: 15px;
      border-top: 1px dashed rgba(255,255,255,0.1);
  }
  h1, h2 { font-weight: 600; margin-bottom: 0.5rem; }
  p { margin-bottom: 0; font-family: 'Consolas', monospace; color: #94a3b8; font-size: 1.1rem; }
</style>"""
    p[0] = f"<html>\n<head>\n<title>Smart Home Dashboard</title>\n{css}\n</head>\n<body>\n<div class='dashboard-container'>\n{p[1]}\n</div>\n</body>\n</html>"

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
    
    # 1. Validación Semántica
    prefijo = actuador.split("_")[0] + "_"
    image_tag = ""

    if atributo == ".brillo":
        num = float(str(valor).replace("%", ""))
        min_val, max_val = REGLAS_ACTUADORES[prefijo][atributo]["rango"]
        if not (min_val <= num <= max_val):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El {atributo} de {actuador} debe estar entre {min_val}% y {max_val}%</div>"
            return
        if num == 0:
            image_tag = '<img src="icon/foco_0_brillo.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
        elif num == 100:
            image_tag = '<img src="icon/foco_100_brillo.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
        else:
            image_tag = '<img src="icon/foco_50_brillo.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
    elif atributo == ".estado":
        if str(valor).lower() == "on":
            image_tag = '<img src="icon/foco_on.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
        else:
            image_tag = '<img src="icon/foco_off.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
    elif atributo == ".color":
        color_name = str(valor).lower()
        if color_name in ["blanco", "rojo", "azul"]:
            image_tag = f'<img src="icon/foco_{color_name}.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
            
    # 2. Generación HTML
    html = f'  <div class="actuator-card" style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li><span>{atributo} = {valor}</span> {image_tag}</li></ul>\n'
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

    prefijo = actuador.split("_")[0] + "_"
    if atributo == ".temp_obj":
        num = float(str(valor).replace("°C", ""))
        min_val, max_val = REGLAS_ACTUADORES[prefijo][atributo]["rango"]
        if not (min_val <= num <= max_val):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La temperatura objetivo debe estar entre {min_val}°C y {max_val}°C</div>"
            return
            
    image_tag = ""
    if atributo == ".estado":
        if str(valor).lower() == "on":
            image_tag = '<img src="icon/aire_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        else:
            image_tag = '<img src="icon/aire_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".modo":
        modo = str(valor).lower()
        if modo == "calor":
            image_tag = '<img src="icon/aire_modo_calor.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        elif modo == "frio":
            image_tag = '<img src="icon/aire_modo_frio.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        elif modo == "ventilacion":
            image_tag = '<img src="icon/aire_modo_vent.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".temp_obj":
        image_tag = '<img src="icon/aire_temperatura_obj_act.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'

    html = f'  <div class="actuator-card" style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li><span>{atributo} = {valor}</span> {image_tag}</li></ul>\n'
    html += f'  </div>'
    p[0] = html
#persiana 
def p_asignacion_persiana(p):
    """asignacion : ACT_PERSIANA ATTR_POSICION ASSIGN PERCENT"""
    
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
    
    prefijo = actuador.split("_")[0] + "_"
    if atributo == ".posicion":
        num = float(str(valor).replace("%", ""))
        min_val, max_val = REGLAS_ACTUADORES[prefijo][atributo]["rango"]
        if not (min_val <= num <= max_val):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La posicion de {actuador} debe estar entre {min_val}% y {max_val}%</div>"
            return
            
    # 2. Generación HTML
    image_tag = '<img src="icon/persiana.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'

    html = f'  <div class="actuator-card" style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li><span>{atributo} = {valor}</span> {image_tag}</li></ul>\n'
    html += f'  </div>'
    p[0] = html
#ceradura
def p_asignacion_cerradura(p):
    """asignacion : ACT_CERRADURA ATTR_ESTADO ASSIGN ON
                  | ACT_CERRADURA ATTR_ESTADO ASSIGN OFF"""
                  
    actuador = p[1]
    atributo = p[2]
    valor = p[4]
            
    image_tag = ""
    if str(valor).lower() == "on":
        image_tag = '<img src="icon/cerradura_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    else:
        image_tag = '<img src="icon/cerradura_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'

    html = f'  <div class="actuator-card" style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li><span>{atributo} = {valor}</span> {image_tag}</li></ul>\n'
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
    
    prefijo = actuador.split("_")[0] + "_"
    if atributo == ".volumen":
        num = float(str(valor).replace("%", ""))
        min_val, max_val = REGLAS_ACTUADORES[prefijo][atributo]["rango"]
        if not (min_val <= num <= max_val):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El volumen de {actuador} debe estar entre {min_val}% y {max_val}%</div>"
            return
    elif atributo == ".email_notif":
        email_str = str(valor)
        usuario = email_str.split("@")[0]
        valor = f'<a href="mailto:{email_str}">Contactar a {usuario}</a>'

    # 2. Generación HTML
    image_tag = ""
    if atributo == ".volumen":
        image_tag = '<img src="icon/altavoz_vol.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".mute":
        if str(valor).lower() == "on":
            image_tag = '<img src="icon/altavoz_mute_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        else:
            image_tag = '<img src="icon/altavoz_mute_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".mensaje":
        image_tag = '<img src="icon/altavoz_mensaje.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".email_notif":
        image_tag = '<img src="icon/altavoz_email.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'

    html = f'  <div class="actuator-card" style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li><span>{atributo} = {valor}</span> {image_tag}</li></ul>\n'
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
            
    image_tag = ""
    if atributo == ".estado":
        if str(valor).lower() == "on":
            image_tag = '<img src="icon/alarma_estado_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        else:
            image_tag = '<img src="icon/alarma_estado_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".activada":
        if str(valor).lower() == "on":
            image_tag = '<img src="icon/alarma_activada_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        else:
            image_tag = '<img src="icon/alarma_activada_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'

    html = f'  <div class="actuator-card" style="border: 1px solid gray; padding: 20px;">\n'
    html += f'    <h1>{actuador}</h1>\n'
    html += f'    <ul><li><span>{atributo} = {valor}</span> {image_tag}</li></ul>\n'
    html += f'  </div>'
    p[0] = html

#--------------------FIN DE LAS ASIGNACIONES--------------------

#--------------------FUNCIONES DE BLOQUES--------------------
def p_bloque_every(p):
    """bloque_every : EVERY HORA DO instrucciones END
                    | EVERY TIME_DURATION DO instrucciones END"""
    
    hora = p[2]
    instrucciones_do = p[4]
    
    html = f'<div class="block-container" style="border-left: 4px solid #34d399;">\n'
    html += f'  <div class="block-header every-header">EVERY {hora} DO</div>\n'
    html += f'  <div class="block-content">\n{instrucciones_do}\n  </div>\n'
    html += f'</div>'
    
    p[0] = html

def p_bloque_when(p):
    "bloque_when : WHEN condicion DO instrucciones END"
    
    condicion = p[2]
    instrucciones_do = p[4]

    html = f'<div class="block-container" style="border-left: 4px solid #60a5fa;">\n'
    html += f'  <div class="block-header when-header">WHEN</div>\n'
    html += f'  <div class="condition-area" style="display: flex; flex-wrap: wrap; align-items: center; gap: 15px; margin: 0 15px 20px 15px;">\n{condicion}\n  </div>\n'
    html += f'  <div class="block-header when-header">DO</div>\n'
    html += f'  <div class="block-content">\n{instrucciones_do}\n  </div>\n'
    html += f'</div>'
    
    p[0] = html


def p_bloque_if(p):
    """bloque_if : IF condicion THEN instrucciones END
                | IF condicion THEN instrucciones ELSE instrucciones END"""

    condicion = p[2]  
    instrucciones_then = p[4] 
    if len(p) == 6:
        html = f'<div class="block-container" style="border-left: 4px solid #fbbf24;">\n'
        html += f'  <div class="block-header if-header">IF</div>\n'
        html += f'  <div class="condition-area" style="display: flex; flex-wrap: wrap; align-items: center; gap: 15px; margin: 0 15px 20px 15px;">\n{condicion}\n  </div>\n'
        html += f'  <div class="block-header if-header">THEN</div>\n'
        html += f'  <div class="block-content">\n{instrucciones_then}\n  </div>\n'
        html += f'</div>'
        p[0] = html

    elif len(p) == 8:
        instrucciones_else = p[6]
        html = f'<div class="block-container" style="border-left: 4px solid #fbbf24;">\n'
        html += f'  <div class="block-header if-header">IF</div>\n'
        html += f'  <div class="condition-area" style="display: flex; flex-wrap: wrap; align-items: center; gap: 15px; margin: 0 15px 20px 15px;">\n{condicion}\n  </div>\n'
        html += f'  <div class="block-header if-header">THEN</div>\n'
        html += f'  <div class="block-content">\n{instrucciones_then}\n  </div>\n'
        html += f'  <div class="block-header if-header" style="margin-top: 15px;">ELSE</div>\n'
        html += f'  <div class="block-content">\n{instrucciones_else}\n  </div>\n'
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
        html += f' <div style="font-weight: bold; font-size: 1.2rem; color: #cbd5e1; padding: 0 10px;">{p[2]}</div>\n'
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
        html = f'<div style="font-weight: bold; font-size: 1.2rem; color: #f87171; margin-right: 10px;">NOT</div>\n'
        html += unit
        p[0] = html
    elif len(p) == 4:
        # LPAREN condicion RPAREN
        cond = p[2]
        html = f'<div style="display: flex; align-items: center; border: 1px dashed rgba(255,255,255,0.2); padding: 10px; border-radius: 8px; gap: 10px;">\n'
        html += f'<span style="font-size: 1.5rem; color: #cbd5e1;">(</span>\n'
        html += cond
        html += f'<span style="font-size: 1.5rem; color: #cbd5e1;">)</span>\n'
        html += f'</div>'
        p[0] = html

#SENSOR TEMPERATURA
def p_comparison_sensor_temp(p):
    """comparison : SENS_TEMP operador_comp TEMP"""
    sensor = p[1]
    operador = p[2]
    valor = p[3]
    
    prefijo = sensor.split("_")[0] + "_" + sensor.split("_")[1]
    min_val, max_val = REGLAS_SENSORES[prefijo]["rango"]
    num = float(str(valor).replace("°C", ""))
    if not (min_val <= num <= max_val):
        p[0] = f"<div style='color:red;'>Error Semántico: Valor de temperatura fuera de rango ({min_val}° a {max_val}°)</div>"
        return
        
    image_tag = '<img src="icon/sens_temp.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    p[0] = f'<div class="sensor-card" style="border: 1px solid green; padding: 20px;"><div style="display: flex; justify-content: space-between; align-items: center;"><h2>{sensor}</h2> {image_tag}</div><p>Condición: {operador} {valor}</p></div>'

#SENSOR HUMEDAD
def p_comparison_sensor_humedad(p):
    """comparison : SENS_HUMEDAD operador_comp PERCENT"""
    sensor = p[1]
    operador = p[2]
    valor = p[3]
    
    prefijo = sensor.split("_")[0] + "_" + sensor.split("_")[1]
    min_val, max_val = REGLAS_SENSORES[prefijo]["rango"]
    num = float(str(valor).replace("%", ""))
    if not (min_val <= num <= max_val):
        p[0] = f"<div style='color:red;'>Error Semántico: Valor de humedad fuera de rango ({min_val}% a {max_val}%)</div>"
        return
        
    image_tag = '<img src="icon/sens_humedad.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    p[0] = f'<div class="sensor-card" style="border: 1px solid green; padding: 20px;"><div style="display: flex; justify-content: space-between; align-items: center;"><h2>{sensor}</h2> {image_tag}</div><p>Condición: {operador} {valor}</p></div>'

#SENSOR LUZ
def p_comparison_sensor_luz(p):
    """comparison : SENS_LUZ operador_comp LUX"""

    sensor = p[1]
    operador = p[2]
    valor = p[3]
    
    prefijo = sensor.split("_")[0] + "_" + sensor.split("_")[1]
    min_val, max_val = REGLAS_SENSORES[prefijo]["rango"]
    num = float(str(valor).replace("lux", ""))
    if not (min_val <= num <= max_val):
        p[0] = f"<div style='color:red;'>Error Semántico: Valor de Iluminancia fuera de rango ({min_val}lux a {max_val}lux)</div>"
        return
        
    image_tag = '<img src="icon/sens_luz.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    p[0] = f'<div class="sensor-card" style="border: 1px solid green; padding: 20px;"><div style="display: flex; justify-content: space-between; align-items: center;"><h2>{sensor}</h2> {image_tag}</div><p>Condición: {operador} {valor}</p></div>'

#SENSOR MOVIMIENTO
def p_comparison_sensor_mov(p):
    """comparison : SENS_MOVIMIENTO EQUAL TRUE
                  | SENS_MOVIMIENTO EQUAL FALSE
                  | SENS_MOVIMIENTO NEGATE TRUE
                  | SENS_MOVIMIENTO NEGATE FALSE"""
    sensor = p[1]
    operador = p[2]
    valor = p[3]

    image_tag = '<img src="icon/sens_movimiento.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    p[0] = f'<div class="sensor-card" style="border: 1px solid green; padding: 20px;"><div style="display: flex; justify-content: space-between; align-items: center;"><h2>{p[1]}</h2> {image_tag}</div><p>Condición: {p[2]} {p[3]}</p></div>'

#SENSOR HUMO
def p_comparison_sensor_humo(p):
    """comparison : SENS_HUMO EQUAL TRUE
                  | SENS_HUMO EQUAL FALSE
                  | SENS_HUMO NEGATE TRUE
                  | SENS_HUMO NEGATE FALSE"""

    sensor = p[1]
    operador = p[2]
    valor = p[3]

    image_tag = '<img src="icon/sens_humo.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    p[0] = f'<div class="sensor-card" style="border: 1px solid green; padding: 20px;"><div style="display: flex; justify-content: space-between; align-items: center;"><h2>{p[1]}</h2> {image_tag}</div><p>Condición: {p[2]} {p[3]}</p></div>'

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
    
    prefijo = actuador.split("_")[0] + "_"
    image_tag = ""

    if atributo in [".estado", ".color"]:
        if operador not in ["==", "!="]:
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: No puedes usar '{operador}' en {atributo}. Usa == o !=</div>"
            return
        if atributo == ".estado":
            if str(valor).lower() == "on":
                image_tag = '<img src="icon/foco_on.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
            else:
                image_tag = '<img src="icon/foco_off.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
        elif atributo == ".color":
            color_name = str(valor).lower()
            if color_name in ["blanco", "rojo", "azul"]:
                image_tag = f'<img src="icon/foco_{color_name}.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'

    elif atributo == ".brillo":
        num = float(str(valor).replace("%", ""))
        min_val, max_val = REGLAS_ACTUADORES[prefijo][atributo]["rango"]
        if not (min_val <= num <= max_val):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El {atributo} de {actuador} debe estar entre {min_val}% y {max_val}%</div>"
            return
        if num == 0:
            image_tag = '<img src="icon/foco_0_brillo.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
        elif num == 100:
            image_tag = '<img src="icon/foco_100_brillo.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
        else:
            image_tag = '<img src="icon/foco_50_brillo.png" width="40" style="vertical-align: middle; margin-right: 10px;" />'
            
    p[0] = f'<div class="actuator-card" style="border: 1px solid gray; padding: 20px;"><h1>{actuador}</h1><ul><li><span>{atributo} {operador} {valor}</span> {image_tag}</li></ul></div>'

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
    
    prefijo = actuador.split("_")[0] + "_"
    if atributo in [".estado", ".modo"]:
        if operador not in ["==", "!="]:
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: No puedes usar '{operador}' en {atributo}. Usa == o !=</div>"
            return
    elif atributo == ".temp_obj":
        num = float(str(valor).replace("°C", ""))
        min_val, max_val = REGLAS_ACTUADORES[prefijo][atributo]["rango"]
        if not (min_val <= num <= max_val):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La temperatura objetivo debe estar entre {min_val}°C y {max_val}°C</div>"
            return
    elif atributo == ".temp_act":
        num = float(str(valor).replace("°C", ""))
        min_val, max_val = REGLAS_ACTUADORES[prefijo][atributo]["rango"]
        if not (min_val <= num <= max_val):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La temperatura actual debe estar entre {min_val}°C y {max_val}°C</div>"
            return
            
    image_tag = ""
    if atributo == ".estado":
        if str(valor).lower() == "on":
            image_tag = '<img src="icon/aire_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        else:
            image_tag = '<img src="icon/aire_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".modo":
        modo = str(valor).lower()
        if modo == "calor":
            image_tag = '<img src="icon/aire_modo_calor.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        elif modo == "frio":
            image_tag = '<img src="icon/aire_modo_frio.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        elif modo == "ventilacion":
            image_tag = '<img src="icon/aire_modo_vent.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo in [".temp_obj", ".temp_act"]:
        image_tag = '<img src="icon/aire_temperatura_obj_act.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'

    p[0] = f'<div class="actuator-card" style="border: 1px solid gray; padding: 20px;"><h1>{actuador}</h1><ul><li><span>{atributo} {operador} {valor}</span> {image_tag}</li></ul></div>'

# COMPARACIÓN PARA PERSIANA 
def p_comparison_actuador_persiana(p):
    """comparison : ACT_PERSIANA ATTR_POSICION operador_comp PERCENT"""
    
    actuador = p[1]
    atributo = p[2]
    operador = p[3]
    valor = p[4]
    
    prefijo = actuador.split("_")[0] + "_"
    if atributo == ".posicion":
        num = float(str(valor).replace("%", ""))
        min_val, max_val = REGLAS_ACTUADORES[prefijo][atributo]["rango"]
        if not (min_val <= num <= max_val):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: La posición debe estar entre {min_val}% y {max_val}%</div>"
            return
            
    image_tag = '<img src="icon/persiana.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    p[0] = f'<div class="actuator-card" style="border: 1px solid gray; padding: 20px;"><h1>{actuador}</h1><ul><li><span>{atributo} {operador} {valor}</span> {image_tag}</li></ul></div>'

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
            
    image_tag = ""
    if str(valor).lower() == "on":
        image_tag = '<img src="icon/cerradura_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    else:
        image_tag = '<img src="icon/cerradura_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    p[0] = f'<div class="actuator-card" style="border: 1px solid gray; padding: 20px;"><h1>{actuador}</h1><ul><li><span>{atributo} {operador} {valor}</span> {image_tag}</li></ul></div>'

# COMPARACIÓN PARA RELOJ 
def p_comparison_actuador_reloj(p):
    """comparison : ACT_RELOJ ATTR_HORA operador_comp HORA
                  | ACT_RELOJ ATTR_FECHA operador_comp FECHA"""
    
    image_tag = ""
    if str(p[2]) == ".hora":
        image_tag = '<img src="icon/reloj_hora.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif str(p[2]) == ".fecha":
        image_tag = '<img src="icon/reloj_fecha.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    p[0] = f'<div class="actuator-card" style="border: 1px solid gray; padding: 20px;"><h1>{p[1]}</h1><ul><li><span>{p[2]} {p[3]} {p[4]}</span> {image_tag}</li></ul></div>'

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
    
    prefijo = actuador.split("_")[0] + "_"
    if atributo in [".mute", ".mensaje", ".email_notif"]:
        if operador not in ["==", "!="]:
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: No puedes usar '{operador}' en {atributo}. Usa == o !=</div>"
            return
        if atributo == ".email_notif":
            email_str = str(valor)
            usuario = email_str.split("@")[0]
            valor = f'<a href="mailto:{email_str}">Contactar a {usuario}</a>'
    elif atributo == ".volumen":
        num = float(str(valor).replace("%", ""))
        min_val, max_val = REGLAS_ACTUADORES[prefijo][atributo]["rango"]
        if not (min_val <= num <= max_val):
            p[0] = f"<div style='color:red; border:2px solid red; padding:10px;'>Error Semántico: El volumen debe estar entre {min_val}% y {max_val}%</div>"
            return
            
    image_tag = ""
    if atributo == ".volumen":
        image_tag = '<img src="icon/altavoz_vol.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".mute":
        if str(valor).lower() == "on":
            image_tag = '<img src="icon/altavoz_mute_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        else:
            image_tag = '<img src="icon/altavoz_mute_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".mensaje":
        image_tag = '<img src="icon/altavoz_mensaje.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".email_notif":
        image_tag = '<img src="icon/altavoz_email.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'

    p[0] = f'<div class="actuator-card" style="border: 1px solid gray; padding: 20px;"><h1>{actuador}</h1><ul><li><span>{atributo} {operador} {valor}</span> {image_tag}</li></ul></div>'

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
            
    image_tag = ""
    if atributo == ".estado":
        if str(valor).lower() == "on":
            image_tag = '<img src="icon/alarma_estado_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        else:
            image_tag = '<img src="icon/alarma_estado_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
    elif atributo == ".activada":
        if str(valor).lower() == "on":
            image_tag = '<img src="icon/alarma_activada_on.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'
        else:
            image_tag = '<img src="icon/alarma_activada_off.jpg" width="40" style="vertical-align: middle; margin-left: 10px;" />'

    p[0] = f'<div class="actuator-card" style="border: 1px solid gray; padding: 20px;"><h1>{actuador}</h1><ul><li><span>{atributo} {operador} {valor}</span> {image_tag}</li></ul></div>'

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
