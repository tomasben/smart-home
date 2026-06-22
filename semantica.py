REGLAS_ACTUADORES = {
    "foco_": {
        ".estado": {"valores": ["ON", "OFF"], "permiso": "RW"},
        ".brillo": {"valores": "porcentaje", "permiso": "RW", "rango": (0, 100)},
        ".color": {"valores": ["blanco", "rojo", "azul"], "permiso": "RW"}
    },
    "aire_": {
        ".estado": {"valores": ["ON", "OFF"], "permiso": "RW"},
        ".modo": {"valores": ["FRIO", "CALOR", "VENT"], "permiso": "RW"},
        ".temp_obj": {"valores": "temperatura", "permiso": "RW", "rango": (16, 30)},
        ".temp_act": {"valores": "temperatura", "permiso": "R", "rango": (-10, 50)}
    },
    "persiana_": {
        ".posicion": {"valores": "porcentaje", "permiso": "RW", "rango": (0, 100)}
    },
    "cerradura_": {
        ".estado": {"valores": ["ON", "OFF"], "permiso": "RW"}
    },
    "reloj_": {
        ".hora": {"valores": "hora", "permiso": "R"},
        ".fecha": {"valores": "fecha", "permiso": "R"}
    },
    "altavoz_": {
        ".volumen": {"valores": "porcentaje", "permiso": "RW", "rango": (0, 100)},
        ".mute": {"valores": ["ON", "OFF"], "permiso": "RW"},
        ".mensaje": {"valores": "string", "permiso": "RW"},
        ".email_notif": {"valores": "email", "permiso": "RW"}
    },
    "alarma_": {
        ".estado": {"valores": ["ON", "OFF"], "permiso": "RW"},
        ".activada": {"valores": ["ON", "OFF"], "permiso": "RW"}
    }
}

REGLAS_SENSORES = {
    "sensor_temp": {"tipo": "temperatura", "rango": (-10, 50)},
    "sensor_humedad": {"tipo": "porcentaje", "rango": (0, 100)},
    "sensor_luz": {"tipo": "lux", "rango": (0, 1000)},
    "sensor_movimiento": {"tipo": "booleano", "valores": ["TRUE", "FALSE"]},
    "sensor_humo": {"tipo": "booleano", "valores": ["TRUE", "FALSE"]}
}
