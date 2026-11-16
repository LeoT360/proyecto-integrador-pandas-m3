# Taller práctico: calidad de datos para la retención estudiantil

Proyecto de limpieza y análisis de un dataset sintético de estudiantes. El objetivo es dejar los datos confiables antes de responder preguntas sobre deserción.

## Cómo ejecutar

```bash
python -m venv .venv
source .venv/bin/activate   # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Estructura

```
├── main.py                 Orquesta todo el flujo
├── config.py               Rutas, VALIDOS y registrar()
├── explorar.py             Primera mirada y diccionario
├── auditar.py              Conteo de problemas de calidad
├── limpieza.py             Numéricos, categorías y fechas
├── tratamiento.py          Duplicados, faltantes e imposibles
├── variables.py            desertor y cuartil_asistencia
├── graficos.py             Los 4 gráficos
├── preguntas.py            Las 5 preguntas de negocio
├── guardar.py              Guarda dataset_limpio y decisiones
├── requirements.txt
├── LEEME_ambiente.txt
└── Data/
    ├── raw/datos_estudiantes.csv
    └── processed/
        ├── dataset_limpio.csv
        ├── decisiones.csv
        └── graficos/
```

## Mis decisiones y respuestas

### Alumno: Jesús Leonardo Torre Melgarejo
### Documento: 1020497992

### 0. Diccionario de datos

| Columna | Tipo | Rol | Descripción |
|---------|------|-----|-------------|
| id_estudiante | texto | identificación | Código único del estudiante |
| programa | categórica | explicativa | Carrera en la que está matriculado |
| facultad | categórica | explicativa | Facultad del programa |
| jornada | categórica | explicativa | Diurna, nocturna o fin de semana |
| semestre | numérica | explicativa | Semestre que cursa |
| promedio_acumulado | numérica | explicativa | Promedio de notas (escala 0-5) |
| creditos_aprobados | numérica | explicativa | Créditos ya aprobados |
| materias_reprobadas | numérica | explicativa | Materias perdidas |
| asistencia_pct | numérica | explicativa | Porcentaje de asistencia |
| sesiones_tutoria | numérica | explicativa | Veces que fue a tutoría |
| cambios_programa | numérica | explicativa | Si cambió de programa |
| estrato | categórica | explicativa | Estrato socioeconómico (1-6) |
| beca | categórica | explicativa | Si recibe beca (sí/no) |
| trabaja | categórica | explicativa | Si trabaja mientras estudia |
| horas_trabajo_semana | numérica | explicativa | Horas que trabaja a la semana |
| distancia_km | numérica | explicativa | Kilómetros casa-institución |
| edad | numérica | explicativa | Edad en años |
| genero | categórica | explicativa | Género registrado |
| ciudad_procedencia | categórica | explicativa | Ciudad de origen |
| tipo_colegio | categórica | explicativa | Público o privado |
| fecha_matricula | fecha | explicativa | Fecha de matrícula |
| estado | categórica | resultado | Activo, graduado o desertor |
| motivo_retiro | categórica | resultado | Razón del retiro (solo desertores) |

### 1. Diagnóstico de calidad

- Nulos reales en promedio, distancia, ciudad, tipo de colegio y motivo_retiro.
- Faltantes disfrazados: guiones en asistencia y horas de trabajo, 999 en distancia.
- 300 asistencias con signo %.
- 150 filas duplicadas.
- 12 edades fuera de 15-60 y 17 promedios mayores a 5.
- Fechas en dos formatos distintos.

Lo que más dañaba el análisis eran los promedios > 5: un 78 en escala de 0-5 sube el promedio de toda la institución.

### 2. Decisiones de limpieza

- Se quitó el % de asistencia y se convirtió a número; los guiones pasaron a nulo.
- Horas de trabajo: guiones a nulo; si no trabaja se puso 0; valores > 100 se reemplazaron por la mediana de quienes sí trabajan.
- Distancia 999 se trató como nulo.
- Programa, jornada, género y ciudad se unificaron a una sola escritura.
- Fechas se pasaron a datetime con ambos formatos.
- Se eliminaron 150 duplicados.
- Filas sin promedio se eliminaron (una nota no se inventa).
- Ciudad y tipo de colegio nulos se rellenaron con "Sin dato".
- Edades imposibles se reemplazaron por la mediana.
- Promedios > 5 se volvieron nulos y se eliminaron esas filas.

### 3. Respuestas a las cinco preguntas

1. **Programa con mayor deserción**: Ingeniería Industrial (~40 %) con 1.271 estudiantes.
2. **Beca**: los becados desertan menos. Eso no prueba que la beca cause la permanencia; puede ser que quien recibe beca ya tenía mejores condiciones.
3. **Jornada con menor promedio**: Nocturna (aprox. 3.46) con 2.666 estudiantes.
4. **Materias reprobadas**: los desertores tienen más materias reprobadas que los activos. Se excluyen graduados porque no pertenecen a ninguno de los dos grupos.
5. **Asistencia**: la deserción baja de Q1 a Q4. Hay asociación clara, pero no prueba causa.

### 4. Reflexión 1 – Asociación y causalidad

Si los becados desertan menos, no significa que la beca cause la permanencia. Puede ser que los que reciben beca ya venían con mejor promedio, más apoyo familiar o más motivación. Para hablar de causa habría que comparar grupos parecidos que solo se diferencien en la beca, y eso este dataset no permite.

### 5. Reflexión 2 – Variables que no se deben usar para predecir

`motivo_retiro` solo se conoce cuando el estudiante ya desertó. Usarla para “predecir” sería hacer trampa: es información del futuro. Lo mismo pasaría con cualquier columna que se llena después del evento que queremos anticipar.

### 6. Reflexión 3 – Variables sensibles

Género, estrato y ciudad pueden estar asociados a la deserción por desigualdades reales. Usarlos para decidir quién recibe apoyo puede reforzar sesgos: se estaría tratando diferente a la gente por características que no controla. Mejor enfocarse en variables de comportamiento académico (asistencia, materias reprobadas, promedio) que sí se pueden intervenir.
