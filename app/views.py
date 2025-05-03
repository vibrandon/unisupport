from flask import render_template, jsonify
from app import app

# Home Route
@app.route("/")
def home():
    return render_template('home.html', title="UniSupport")

@app.route("/avail")
def avail():
    result = {'status_code': 200,'data':"hello"}
    return jsonify(result)

# Error Handlers
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500
