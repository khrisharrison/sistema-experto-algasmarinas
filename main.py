from experta import *

# Base de conocimiento en formato matricial (especie x características)
BASE_CONOCIMIENTO = [
    # Especie             | Color      | Textura      | Forma    | Hábitat          | Longitud
    ("Ulva lactuca",       "verde",    "lisa",       "hoja",   "intermareal",     None),
    ("Porphyra umbilicalis", "rojo",  "gelatinosa",  None,     "rocoso",          "corta"),
    ("Laminaria digitata", "marron",   "aspera",     "cinta",  None,              "largo"),
    ("Fucus vesiculosus",  "marron",   "correosa",   "ramificada", "intermareal", "media"),
    ("Chondrus crispus",   "rojo",     "cartilaginoso", None,   "rocoso",          "corta"),
    ("Sargassum muticum",  "marron",   "aspera",     "ramificada", "flotante",    "largo"),
]

class AlgaFact(Fact):
    """Hechos sobre las características del alga"""
    pass

class SistemaExpertoAlgas(KnowledgeEngine):
    def __init__(self, base_conocimiento):
        super().__init__()
        self.base_conocimiento = base_conocimiento
    
    @DefFacts()
    def _iniciar(self):
        yield Fact(inicio=True)
    
    @Rule(AS.hechos << AlgaFact())
    def identificar_especie(self, hechos):
        """Regla dinámica que compara con la base de conocimiento"""
        # Convertir hechos a diccionario de manera compatible
        caracteristicas = {}
        for key, value in hechos.items():
            # Filtrar campos internos de Experta
            if not key.startswith('__') and not key.endswith('__'):
                caracteristicas[key] = value
        
        mejor_coincidencia = None
        max_coincidencias = 0
        
        # Buscar en todas las especies de la base de conocimiento
        for especie in self.base_conocimiento:
            nombre, *atributos = especie
            coincidencias = 0
            total_atributos = 0
            
            # Comparar cada característica
            for i, (caracteristica, valor_esperado) in enumerate([
                ('color', atributos[0]),
                ('textura', atributos[1]),
                ('forma', atributos[2]),
                ('habitat', atributos[3]),
                ('longitud', atributos[4])
            ]):
                if valor_esperado is not None:  # Solo considerar atributos definidos
                    total_atributos += 1
                    valor_actual = caracteristicas.get(caracteristica)
                    if valor_actual == valor_esperado:
                        coincidencias += 1
            
            # Calcular porcentaje de coincidencia
            if total_atributos > 0:
                porcentaje = (coincidencias / total_atributos) * 100
                
                # Actualizar mejor coincidencia si supera el 70% y tiene más coincidencias
                if porcentaje >= 70 and coincidencias > max_coincidencias:
                    max_coincidencias = coincidencias
                    mejor_coincidencia = nombre
        
        # Si encontramos una buena coincidencia, declarar el resultado
        if mejor_coincidencia:
            self.declare(Fact(especie=mejor_coincidencia))
    
    @Rule(Fact(especie=MATCH.especie))
    def imprimir_resultado(self, especie):
        print(f"\n[RESULTADO] El alga identificada es: {especie}")
        self.halt()  # Detener el motor después de encontrar una coincidencia
    
    @Rule(NOT(Fact(especie=MATCH.especie)))
    def especie_no_identificada(self):
        print("\n[RESULTADO] No se pudo identificar la especie con exactitud")
        print("Las especies más probables podrían ser:")
        for especie in self.base_conocimiento:
            print(f"- {especie[0]}")
        print("\nPor favor, consulte con un especialista para una identificación precisa.")

def obtener_respuesta(pregunta, opciones):
    print(f"\n{pregunta}")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    
    while True:
        try:
            respuesta = int(input("Seleccione una opción (número): "))
            if 1 <= respuesta <= len(opciones):
                # Tomar solo la primera palabra y convertir a minúsculas
                return opciones[respuesta-1].split()[0].lower()
            print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Ingrese un número válido.")

def menu_principal():
    print("\n" + "="*50)
    print("SISTEMA EXPERTO PARA IDENTIFICACIÓN DE ALGAS MARINAS")
    print("="*50)
    
    # Preguntas al usuario
    caracteristicas = {
        'color': obtener_respuesta(
            "¿De qué color es predominantemente el alga?",
            ['Verde', 'Rojo o rosado', 'Marrón o pardo', 'Azul', 'Otro color']
        ),
        'textura': obtener_respuesta(
            "¿Qué textura tiene al tacto?",
            ['Lisa', 'Áspera o rugosa', 'Gelatinosa', 'Correosa', 'Cartilaginosa']
        ),
        'forma': obtener_respuesta(
            "¿Qué forma general tiene?",
            ['Hoja o lámina', 'Cinta alargada', 'Ramificada', 'Tubular', 'Vesicular']
        ),
        'habitat': obtener_respuesta(
            "¿En qué tipo de hábitat se encontró?",
            ['Zona intermareal', 'Zona submareal', 'Sobre rocas', 'En arena', 'Flotante']
        ),
        'longitud': obtener_respuesta(
            "¿Cuál es su tamaño aproximado?",
            ['Corta (menos de 20 cm)', 'Media (20-50 cm)', 'Larga (más de 50 cm)']
        )
    }
    
    return caracteristicas

if __name__ == "__main__":
    motor = SistemaExpertoAlgas(BASE_CONOCIMIENTO)
    motor.reset()
    
    caracteristicas = menu_principal()
    
    # Insertar hechos en el sistema
    motor.declare(AlgaFact(**caracteristicas))
    
    # Ejecutar el sistema experto
    motor.run()