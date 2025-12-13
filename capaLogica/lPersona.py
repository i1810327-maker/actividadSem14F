from capaDatos.dPersona import DPersona

class LPersona:

    def __init__(self):
        self.__dPersona = DPersona()

    def mostrarPersona(self):
        return self.__dPersona.mostrarPersona()

    def nuevaPersona(self, persona: dict):
        self.__dPersona.nuevaPersona(persona)

    def actualizarPersona(self, persona: dict, docIdentidad: str):
        return self.__dPersona.actualizarPersona(persona, docIdentidad)

    def eliminarPersona(self, docidentidad: str):
        return self.__dPersona.eliminarPersona(docidentidad)    