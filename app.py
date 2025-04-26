from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from datetime import datetime
import os
from itertools import combinations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///samples.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SampleResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    m = db.Column(db.Integer, nullable=False)
    n = db.Column(db.Integer, nullable=False)
    k = db.Column(db.Integer, nullable=False)
    j = db.Column(db.Integer, nullable=False)
    s = db.Column(db.Integer, nullable=False)
    run_number = db.Column(db.Integer, nullable=False)
    result_count = db.Column(db.Integer, nullable=False)
    results = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def validate_parameters(m, n, k, j, s):
    if not (45 <= m <= 54):
        return False, "m must be between 45 and 54"
    if not (7 <= n <= 25):
        return False, "n must be between 7 and 25"
    if not (4 <= k <= 7):
        return False, "k must be between 4 and 7"
    if not (s <= j <= k):
        return False, "j must be between s and k"
    if not (3 <= s <= 7):
        return False, "s must be between 3 and 7"
    return True, ""

def generate_combinations(numbers, k):
    return list(map(list, combinations(numbers, k)))

def find_optimal_groups(n_numbers, k, j, s):
    numbers = list(range(1, n_numbers + 1))
    k_combinations = generate_combinations(numbers, k)
    
    valid_groups = []
    for group in k_combinations:
        j_combinations = generate_combinations(group, j)
        for j_group in j_combinations:
            s_combinations = generate_combinations(j_group, s)
            if len(s_combinations) > 0:
                valid_groups.append(group)
                break
    
    return valid_groups

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    m = int(data['m'])
    n = int(data['n'])
    k = int(data['k'])
    j = int(data['j'])
    s = int(data['s'])
    
    valid, error = validate_parameters(m, n, k, j, s)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Generate random numbers if user didn't provide them
    if 'numbers' not in data or not data['numbers']:
        numbers = np.random.choice(range(1, m + 1), n, replace=False).tolist()
    else:
        numbers = [int(x) for x in data['numbers']]
    
    results = find_optimal_groups(len(numbers), k, j, s)
    
    # Save to database
    run_number = SampleResult.query.filter_by(
        m=m, n=n, k=k, j=j, s=s
    ).count() + 1
    
    result = SampleResult(
        m=m, n=n, k=k, j=j, s=s,
        run_number=run_number,
        result_count=len(results),
        results=str(results)
    )
    db.session.add(result)
    db.session.commit()
    
    return jsonify({
        'numbers': numbers,
        'results': results,
        'filename': f"{m}-{n}-{k}-{j}-{s}-{run_number}-{len(results)}"
    })

@app.route('/results')
def get_results():
    results = SampleResult.query.all()
    return jsonify([{
        'id': r.id,
        'filename': f"{r.m}-{r.n}-{r.k}-{r.j}-{r.s}-{r.run_number}-{r.result_count}",
        'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for r in results])

@app.route('/results/<int:result_id>', methods=['GET', 'DELETE'])
def manage_result(result_id):
    result = SampleResult.query.get_or_404(result_id)
    
    if request.method == 'DELETE':
        db.session.delete(result)
        db.session.commit()
        return '', 204
    
    return jsonify({
        'filename': f"{result.m}-{result.n}-{result.k}-{result.j}-{result.s}-{result.run_number}-{result.result_count}",
        'results': eval(result.results),
        'timestamp': result.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
