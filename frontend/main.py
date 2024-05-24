from flask import Flask, render_template, request, session
import dbSearch

app = Flask(__name__)
app.secret_key = 'your_secret_key'

creds = []
requirements = []
departments = []
class_level = []
breadths = []
genEds = []

@app.route('/')
def index():
    return render_template('base.html', length=0)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('q')
    if query == '':
        session.pop('query', None)
    else:
        if not query and 'query' in session:
            query = session['query']
        else:
            session['query'] = query
    rows = dbSearch.search_db(query, creds, requirements, breadths, genEds, class_level)
    if rows is None:
        return render_template('results.html', data=[], length=0)
    global results
    results = {tuple_item[1]: tuple_item[0] for tuple_item in rows}
    return render_template('results.html', data=rows, length=len(rows))


@app.route('/show_info', methods=['POST'])
def show_info():
    value = request.form['class-button']
    f = dbSearch.getData(value)
    return render_template('info.html', data=f)

@app.route('/course/<int:course_id>')
def course_details(course_id):
    f = dbSearch.getData(course_id)
    return render_template('info.html', data=f)

@app.route('/filter_credits', methods=['POST'])
def filter_credits():
    global creds
    creds = request.json.get('values', [])
    print(creds)
    return search()

@app.route('/filter_requirements', methods=['POST'])
def filter_requirements():
    global requirements
    requirements = request.json.get('values', [])
    print(requirements)
    return search()

@app.route('/filter_department', methods=['POST'])
def filter_departments():
    global departments
    departments = request.json.get('values', [])
    print(departments)
    return search()

@app.route('/filter_classlevel' , methods=['POST'])
def filter_class_level():
    global class_level
    class_level = request.json.get('values', [])
    print(class_level)
    return search()

@app.route('/filter_breadths', methods=['POST'])
def filter_breadths():
    global breadths
    breadths = request.json.get('values', [])
    print(breadths)
    return search()

@app.route('/filter_genEd', methods=['POST'])
def filter_genEd():
    global genEds
    genEds = request.json.get('values', [])
    print(genEds)
    return search()

if __name__ == '__main__':
    app.run(debug=True)
