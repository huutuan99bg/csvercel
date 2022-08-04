from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return {"success": True, 'result': 'ok'}


@app.route('/api')
def test():
    return {"success": True, 'message': 'API is working'}

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)
