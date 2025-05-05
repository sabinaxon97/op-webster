from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Replace with your actual RDS PostgreSQL credentials
DB_HOST = "sabinasabitova.c32geugqgvkj.ap-southeast-1.rds.amazonaws.com"
DB_NAME = "db_sabina3t"
DB_USER = "sabina"
DB_PASS = "sabinasabitova23"

def get_connection():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route('/')
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tbl_sabina_air_quality_dataset ORDER BY row_id")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return render_template('index.html', rows=rows, columns=columns)

@app.route('/add', methods=['POST'])
def add():
    data = [request.form.get(col) for col in request.form]
    cols = ', '.join(request.form.keys())
    placeholders = ', '.join(['%s'] * len(data))

    query = f"INSERT INTO tbl_sabina_air_quality_dataset ({cols}) VALUES ({placeholders})"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:row_id>', methods=['POST'])
def delete(row_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tbl_sabina_air_quality_dataset WHERE row_id = %s", (row_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
