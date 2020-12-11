#Importar librerías
from flask import Flask , render_template, request, redirect, url_for, flash
import mysql.connector 

app = Flask(__name__)

#Conexion MYSQL
mysql = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="momento_3"
)

#Configuraciones
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    cur = mysql.cursor()
    sql = f"SELECT * FROM assignation"
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return render_template('home.html', user = result)

@app.route('/assignation')
def assignation():
    return render_template('assignation.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method=='POST':
        id = request.form['id']
        name = request.form['name']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        city = request.form['city']
        neighborhood = request.form['neighborhood']
        cellPhone = request.form['cellPhone']
        cur = mysql.cursor()
        sql = f"INSERT INTO assignation (id,name,lastname,birthdate,city,neighborhood,cellPhone) VALUES ('{id}','{name}','{lastname}','{birthdate}','{city}','{neighborhood}','{cellPhone}')"
        cur.execute(sql)
        mysql.commit()
        flash('Usuario registrado correctamente')
        return redirect(url_for('assignation'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_user(id):
    cur = mysql.cursor()    
    sql = f"SELECT * FROM assignation WHERE id = '{id}'"
    cur.execute(sql)
    result = cur.fetchall()    
    return render_template('edit_user.html', edit = result[0])

@app.route('/update/<id>', methods=['POST'])
def update_user(id):
    if request.method=='POST':
        id = request.form['id']
        name = request.form['name']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        city = request.form['city']
        neighborhood = request.form['neighborhood']
        cellPhone = request.form['cellPhone']
        cur = mysql.cursor()
        sql = f"UPDATE assignation SET id='{id}',name='{name}',lastname='{lastname}',birthdate='{birthdate}',city='{city}',neighborhood='{neighborhood}',cellPhone='{cellPhone}' WHERE id='{id}'"
        cur.execute(sql)
        mysql.commit()
        flash('Usuario actualizado correctamente')
        return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete_user(id):
    cur = mysql.cursor()
    sql = 'DELETE FROM assignation WHERE id = {0}'.format(id)
    cur.execute(sql)
    mysql.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(port=3000, debug=True)