from experta import *

class AlgaFact(Fact):
    """Hechos sobre las características del alga"""
    pass

class SistemaExpertoAlgas(KnowledgeEngine):
    @DefFacts()
    def _iniciar(self):
        """Hechos iniciales"""
        yield Fact(inicio=True)

    # Reglas de identificación
    @Rule(
        AlgaFact(color='verde'),
        AlgaFact(textura='lisa'),
        AlgaFact(forma='hoja'),
        AlgaFact(habitat='intermareal')
    )
    def alga_ulva(self):
        self.declare(Fact(especie="Ulva lactuca (Lechuga de mar)"))

    @Rule(
        AlgaFact(color='rojo'),
        AlgaFact(textura='gelatinosa'),
        AlgaFact(longitud='corta'),
        AlgaFact(habitat='rocoso')
    )
    def alga_porphyra(self):
        self.declare(Fact(especie="Porphyra umbilicalis (Nori)"))

    @Rule(
        Fact(especie=MATCH.especie),
        salience=-1000  # Baja prioridad
    )
    def imprimir_resultado(self, especie):
        print(f"\n[RESULTADO] El alga identificada es: {especie}")

    @Rule(
        NOT(Fact(especie=MATCH.w)),
        salience=-1001
    )
    def especie_no_identificada(self):
        print("\n[RESULTADO] No se pudo identificar la especie con las características proporcionadas")

def obtener_respuesta(pregunta, opciones):
    """Muestra preguntas con opciones y valida la respuesta"""
    print(f"\n{pregunta}")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    
    while True:
        try:
            respuesta = int(input("Seleccione una opción (número): "))
            if 1 <= respuesta <= len(opciones):
                return opciones[respuesta-1].split(' ')[0].lower()  # Toma solo la primera palabra
            print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Ingrese un número válido.")


if __name__ == "__main__":
    motor = SistemaExpertoAlgas()
    motor.reset()

    # Preguntas al usuario
    caracteristicas = {
        'color': obtener_respuesta(
            "¿De qué color es el alga?",
            ['verde', 'rojo', 'marron', 'azul', 'otro']
        ),
        'textura': obtener_respuesta(
            "¿Qué textura tiene?",
            ['lisa', 'aspera', 'gelatinosa', 'escamosa']
        ),
        'habitat': obtener_respuesta(
            "¿Dónde se encontró?",
            ['intermareal', 'submareal', 'rocoso', 'arenal']
        ),
        'forma': obtener_respuesta(
            "¿Qué forma tiene?",
            ['hoja', 'cinta', 'ramificada', 'tubular']
        ),
        'longitud': obtener_respuesta(
            "¿Cuál es su longitud aproximada?",
            ['corta (<20cm)', 'media (20-50cm)', 'largo (>50cm)']
        )
    }

    # Insertar hechos en el sistema
    for clave, valor in caracteristicas.items():
        motor.declare(AlgaFact(**{clave: valor}))
    
    # Ejecutar el sistema experto
    motor.run()