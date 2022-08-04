from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Test ok'


@app.route('/api')
def test():
    return 'Running'

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)
