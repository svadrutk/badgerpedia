from flask import Flask, render_template, request, session
import dbSearch
import enrollment
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key' # secret key for session management; change this to something more secure

# constants to store the filters
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
    global creds, requirements, departments, class_level, breadths, genEds
    query = request.form.get('q') # get the query from the form
    if query == '':
        session.pop('query', None)
    else:
        if not query and 'query' in session:
            query = session['query']
        else:
            session['query'] = query
    rows = dbSearch.search_db(query, creds, requirements, breadths, genEds, class_level)
    if rows is None:
        return render_template('results.html', data=[], length=0) # if no results, return empty list

    global results
    results = {tuple_item[1]: tuple_item[0] for tuple_item in rows}

    # reset the filters
    creds = []
    requirements = []
    departments = []
    class_level = []
    breadths = []
    genEds = []

    return render_template('results.html', data=rows, length=len(rows))


@app.route('/show_info', methods=['POST'])
def show_info():
    value = request.form['class-button'] # get class code from button
    print(value)
    f = dbSearch.getData(value) # get the data for the class
    capacity = enrollment.get_capacity(enrollment.get_enrollment(enrollment.get_class_codes(value))) # get enrollment stats for the class from the API

    # calculate the term based on the current month
    currMonth = time.localtime().tm_mon
    if currMonth >= 5 and currMonth < 9:
        term =  "Fall " + str(time.localtime().tm_year)
    elif currMonth > 9:
        term = "Spring " + str(time.localtime().tm_year)
    else:
        term = "Summer " + str(time.localtime().tm_year)


    # get the times for the class
    timesDict = enrollment.extract_class_info(enrollment.get_enrollment(enrollment.get_class_codes(value)))


    return render_template('info.html', data=f, capacity=capacity, term = term, times = timesDict)



############################################################################################
# Filter functions
############################################################################################

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
    app.run(debug=True, host = '0.0.0.0', port = 8000)
