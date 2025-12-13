from conexion import ConexionDB

class DPersona:

    def __init__(self):
        self.__db = ConexionDB().conexionSupabase()
        self.__nombreTabla = "estudiantee"

    def __ejecutarConsulta(self, consulta, tipoConsulta = None):
        try:
            if tipoConsulta == "SELECT":
                resultado = consulta.execute().data
                return resultado
            else:
                resultado = consulta.execute()
                return resultado
        except Exception as e:
            raise e

    def mostrarPersona(self):
        consulta = self.__db.table(self.__nombreTabla).select("*")
        return self.__ejecutarConsulta(consulta, "SELECT")

    def nuevaPersona(self, persona: dict):
        consulta = self.__db.table(self.__nombreTabla).insert(persona)
        return self.__ejecutarConsulta(consulta)

    def actualizarPersona(self, persona: dict, docIdentidad: str):
        consulta = self.__db.table(self.__nombreTabla).update(persona).eq('dni', docIdentidad)
        return self.__ejecutarConsulta(consulta)

    def eliminarPersona(self, docIdentidad: str):
        consulta = self.__db.table(self.__nombreTabla).delete().eq('dni', docIdentidad)
        return self.__ejecutarConsulta(consulta)