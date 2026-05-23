import random
import pandas as pd

random.seed(42)

MUNICIPIOS = [
    "San Marcos", "La Esperanza", "Villa Nueva", "El Progreso", "Santa Rosa",
    "Quetzaltenango", "Totonicapán", "Sololá", "Chimaltenango", "Escuintla",
    "Retalhuleu", "Suchitepéquez", "Jutiapa", "Jalapa", "Zacapa",
    "Chiquimula", "Izabal", "Alta Verapaz", "Baja Verapaz", "Petén",
    "Huehuetenango", "Ixcán", "San Pedro", "Cobán", "Flores",
    "Mixco", "Amatitlán", "Palencia", "Chinautla", "San Juan Sacatepéquez",
    "Santa Catarina", "Villa Canales", "Fraijanes", "San Raymundo", "Chuarrancho",
    "San José Pinula", "San Pedro Ayampuc", "Tajumulco", "Sibinal", "Tejutla",
    "Malacatán", "El Quiché", "Nebaj", "Chichicastenango", "Jacaltenango",
    "Barillas", "Todos Santos", "San Mateo", "Olintepeque", "Zunil",
]

def generar_mesa_normal(mesa_id, municipio):
    c1 = random.randint(10, 80)
    c2 = random.randint(10, 80)
    c3 = random.randint(10, 80)
    c4 = random.randint(10, 80)
    c5 = random.randint(10, 80)
    nulos = random.randint(0, 20)
    total = c1 + c2 + c3 + c4 + c5 + nulos
    return {
        "mesa_id": mesa_id,
        "municipio": municipio,
        "candidato_1": c1,
        "candidato_2": c2,
        "candidato_3": c3,
        "candidato_4": c4,
        "candidato_5": c5,
        "votos_nulos": nulos,
        "total_votos": total,
        "capacidad_mesa": 200,
        "tiene_anomalia": False,
        "tipo_anomalia": None,
    }

def inyectar_total_incorrecto(fila):
    diferencia = random.randint(10, 30)
    signo = random.choice([-1, 1])
    fila["total_votos"] = fila["total_votos"] + signo * diferencia
    fila["tiene_anomalia"] = True
    fila["tipo_anomalia"] = "total_incorrecto"
    return fila

def inyectar_participacion_extrema(fila):
    # total_votos > 190, distribución entre candidatos coherente
    total = random.randint(191, 199)
    c1 = random.randint(30, 50)
    c2 = random.randint(30, 50)
    c3 = random.randint(30, 50)
    c4 = random.randint(20, 40)
    c5 = random.randint(20, 30)
    nulos = max(0, total - c1 - c2 - c3 - c4 - c5)
    fila.update({
        "candidato_1": c1, "candidato_2": c2, "candidato_3": c3,
        "candidato_4": c4, "candidato_5": c5,
        "votos_nulos": nulos, "total_votos": total,
        "tiene_anomalia": True, "tipo_anomalia": "participacion_extrema",
    })
    return fila

def inyectar_votos_nulos_cero(fila):
    total = random.randint(161, 185)
    c1 = random.randint(30, 50)
    c2 = random.randint(30, 50)
    c3 = random.randint(30, 50)
    c4 = random.randint(20, 40)
    resto = total - c1 - c2 - c3 - c4
    c5 = max(10, resto)
    fila.update({
        "candidato_1": c1, "candidato_2": c2, "candidato_3": c3,
        "candidato_4": c4, "candidato_5": c5,
        "votos_nulos": 0, "total_votos": total,
        "tiene_anomalia": True, "tipo_anomalia": "votos_nulos_cero",
    })
    return fila

# Generar 50 mesas
filas = []
for i in range(1, 51):
    mesa_id = f"Mesa_{i:03d}"
    municipio = MUNICIPIOS[i - 1]
    filas.append(generar_mesa_normal(mesa_id, municipio))

# Índices de anomalías (fijos con seed)
# 4 total_incorrecto: índices 5, 12, 23, 37
# 3 participacion_extrema: índices 8, 19, 44
# 3 votos_nulos_cero: índices 2, 31, 48

anomalias = {
    "total_incorrecto":    [5, 12, 23, 37],
    "participacion_extrema": [8, 19, 44],
    "votos_nulos_cero":    [2, 31, 48],
}

for idx in anomalias["total_incorrecto"]:
    filas[idx] = inyectar_total_incorrecto(filas[idx])

for idx in anomalias["participacion_extrema"]:
    filas[idx] = inyectar_participacion_extrema(filas[idx])

for idx in anomalias["votos_nulos_cero"]:
    filas[idx] = inyectar_votos_nulos_cero(filas[idx])

df = pd.DataFrame(filas)

columnas = [
    "mesa_id", "municipio",
    "candidato_1", "candidato_2", "candidato_3", "candidato_4", "candidato_5",
    "votos_nulos", "total_votos", "capacidad_mesa",
    "tiene_anomalia", "tipo_anomalia",
]
df = df[columnas]

df.to_csv("data/metadata.csv", index=False)
print(f"Generado: data/metadata.csv — {len(df)} filas")
print(f"Anómalas: {df['tiene_anomalia'].sum()}")
print(df['tipo_anomalia'].value_counts(dropna=False))
