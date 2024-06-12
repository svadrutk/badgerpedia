from flask import Flask, render_template, request, session
import dbSearch
import enrollment
import time
import urllib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # secret key for session management; change this to something more secure

# Initialize the session with default filter values
@app.before_request
def make_session_permanent():
    session.permanent = False
    if 'filters' not in session:
        session['filters'] = {
            'creds': [],
            'requirements': [],
            'departments': [],
            'class_level': [],
            'breadths': [],
            'genEds': []
        }

@app.route('/')
def index(data = None, capacity = None, term = None, times = None):
    session['filters'] = {
        'creds': [],
        'requirements': [],
        'departments': [],
        'class_level': [],
        'breadths': [],
        'genEds': []
    }
    print("Filters reset.")

    if data is not None and capacity is not None and term is not None and times is not None:
        print("Data: ", data)
        return render_template('class_info.html', length = 0, data=data, capacity=capacity, term=term, times=times)
    else:
        print("wtf")
        return render_template('base.html', length=0)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')  # get the query from the form
    if query == '':
        session.pop('query', None)
    else:
        if not query and 'query' in session:
            query = session['query']
        else:
            session['query'] = query

    filters = session['filters']
    rows = dbSearch.search_db(query, filters['creds'], filters['requirements'], filters['breadths'], filters['genEds'], filters['class_level'])
    if rows is None:
        return render_template('results.html', data=[], length=0)  # if no results, return empty list

    global results
    results = {tuple_item[1]: tuple_item[0] for tuple_item in rows}

    return render_template('results.html', data=rows, length=len(rows))

@app.route('/class/<path:class_code>')
def show_info(class_code):
    decoded_class_code = urllib.parse.unquote(class_code)
    print(decoded_class_code)
    f = dbSearch.getData(decoded_class_code)  # get the data for the class
    capacity = enrollment.get_capacity(enrollment.get_enrollment(enrollment.get_class_codes(decoded_class_code)))  # get enrollment stats for the class from the API

    # calculate the term based on the current month
    currMonth = time.localtime().tm_mon
    if currMonth >= 5 and currMonth < 9:
        term = "Fall " + str(time.localtime().tm_year)
    elif currMonth > 9:
        term = "Spring " + str(time.localtime().tm_year)
    else:
        term = "Summer " + str(time.localtime().tm_year)

    # get the times for the class
    timesDict = enrollment.extract_class_info(enrollment.get_enrollment(enrollment.get_class_codes(decoded_class_code)))

    if 'HX-Request' in request.headers:
        return render_template('class_info_raw.html', data=f, capacity=capacity, term=term, times=timesDict)
    else:
        return render_template('class_info.html', data=f, capacity=capacity, term=term, times=timesDict)


############################################################################################
# Filter functions
############################################################################################

@app.route('/filter_credits', methods=['GET'])
def filter_credits():
    filters = session['filters']
    filters['creds'] = request.args.getlist('values')
    session['filters'] = filters
    print(filters['creds'])
    return search()

@app.route('/filter_requirements', methods=['GET'])
def filter_requirements():
    filters = session['filters']
    filters['requirements'] = request.args.getlist('values')
    session['filters'] = filters
    print(filters['requirements'])
    return search()

@app.route('/filter_department', methods=['GET'])
def filter_departments():
    filters = session['filters']
    filters['departments'] = request.args.getlist('values')
    session['filters'] = filters
    print(filters['departments'])
    return search()

@app.route('/filter_classlevel', methods=['GET'])
def filter_class_level():
    filters = session['filters']
    filters['class_level'] = request.args.getlist('values')
    session['filters'] = filters
    print(filters['class_level'])
    print(filters['breadths'])
    print(filters['creds'])
    return search()

@app.route('/filter_breadths', methods=['GET'])
def filter_breadths():
    filters = session['filters']
    filters['breadths'] = request.args.getlist('values')
    session['filters'] = filters
    print(filters['breadths'])
    return search()

@app.route('/filter_genEd', methods=['GET'])
def filter_genEd():
    filters = session['filters']
    filters['genEds'] = request.args.getlist('values')
    session['filters'] = filters
    print(filters['genEds'])
    return search()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
