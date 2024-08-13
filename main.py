from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='./')
@app.route('/')
def index():
    return app.send_static_file('./live2d.html')

@app.route('/assets/<path:path>')
def serve_static(path):
    return send_from_directory('./assets/',path)

if __name__ == '__main__':
    app.run(port=4800, debug=True, host="0.0.0.0")