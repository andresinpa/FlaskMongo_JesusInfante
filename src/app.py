from click import confirm
from flask import Flask, flash, redirect, render_template, request, url_for
from config import *
from bson import ObjectId 
from persona import Persona

con_bd = Conexion() #Creación de instancia de conexión
app = Flask(__name__)
app.secret_key = 'admin'

#----------------------------- CONSULTAS --------------------------------------------------- 
@app.route('/')
def index():
    personas = con_bd['Personas'] 
    PersonasRegistradas = personas.find()
    return render_template('index.html', personas = PersonasRegistradas)

@app.route('/ordenar') 
def ordenar():
    personas = con_bd['Personas']
    campo = request.args.get('campo') 
    tipo = request.args.get('tipo')
    if (tipo == 'Ascendente'):
        tipo = 1
    else:
        tipo = -1
        
    orden_por_tipo = personas.find().sort(campo, tipo)
    return render_template('index.html', orden=orden_por_tipo)


@app.route('/limite') 
def limite():
    personas = con_bd['Personas']
    limite = int(request.args.get('limite')) 
    primeras_personas = personas.find().limit(limite)
    return render_template('index.html', primeras_personas=primeras_personas)

@app.route('/mayor')
def mayor():
    personas =con_bd['Personas']
    mayor_que = int(request.args.get('mayor'))
    horas_semanales_mayor = personas.find({'horas_trabajo': {'$gt': mayor_que}})
    return render_template('index.html', mayor = horas_semanales_mayor)

@app.route('/menor')
def menor():
    personas =con_bd['Personas']
    menor_que = int(request.args.get('menor'))
    horas_semanales_menor = personas.find({'horas_trabajo': {'$lte': menor_que}})
    return render_template('index.html', menor = horas_semanales_menor)

@app.route('/filtro')
def filtro():
    personas =con_bd['Personas']
    campo = request.args.get('campo')
    if campo == "horas_trabajo":
        valor = int(request.args.get('valor'))
    else:
        valor = request.args.get('valor')
    filtro_campos = personas.find({campo: valor})
    return render_template('index.html', filtro = filtro_campos)

#------------------------ GUARDAR PERSONAS ----------------------------------------------
@app.route('/guardar_personas', methods=['POST'])
def agregarPersona():
    personas = con_bd['Personas']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    estado_civil = request.form['estado_civil']
    horas_trabajo = request.form['horas_trabajo']
    
    if nombre and apellido and telefono and estado_civil and horas_trabajo:
        persona = Persona(nombre ,apellido, telefono, estado_civil, int(horas_trabajo)) #Metodo constructor
        personas.insert_one(persona.format_doc()) #Insertando docuemnto dentro de la colección
        flash('Registro exitoso 👍')
        return redirect(url_for('index'))
    else:
        flash('Error: Todos los campos son obligatorios. 👀')
        return render_template("index.html")

#-------------------------------- ELIMINAR PERSONAS ------------------------------------------------
@app.route('/eliminar_persona/<string:id_persona>')
def eliminar(id_persona):
    _id = ObjectId(id_persona)
    personas= con_bd["Personas"]
    personas.delete_one({'_id': _id})
    return redirect(url_for('index'))
    
#----------------------------- ACTUALIZAR ------------------------------------------------------
@app.route("/editar_persona/<string:id_persona>", methods=["POST"])
def editar(id_persona):
    personas = con_bd['Personas']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    estado_civil = request.form['estado_civil']
    horas_trabajo = request.form['horas_trabajo']
    
    try:
        _id = ObjectId(id_persona)  # Convierte la cadena en un ObjectId
        if nombre and apellido and telefono and estado_civil and horas_trabajo:
            personas.update_one({'_id': _id}, {'$set': {'nombre': nombre, 'apellido': apellido, 'telefono': telefono, 'estado_civil': estado_civil, 'horas_trabajo': horas_trabajo}})
            return redirect(url_for('index'))
        else:
            return "Error"
    except Exception as e:
        return f"Error: {str(e)}"

def error_404(error):
    return render_template('error_404.html'), 404

if __name__ == '__main__':
    app.register_error_handler(404, error_404)
    app.run(debug=True)