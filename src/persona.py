class Persona:
    def __init__(self, nombre, apellido, telefono, estado_civil, horas_trabajo):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.estado_civil = estado_civil
        self.horas_trabajo = horas_trabajo
    def format_doc(self): #Definir la estructura del documento
        return{
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'estado_civil': self.estado_civil,
            'horas_trabajo': self.horas_trabajo,
        }