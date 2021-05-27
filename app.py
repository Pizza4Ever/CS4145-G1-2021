from flask import Flask, request, send_file

# This flask server is only necessary for hosting the image server.

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def home():
    # Determine what images to send here:
    image = 'GROENNN.jpg'
    return send_file('static/' + image, mimetype='image/gif')

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == "__main__":
    app.run(ssl_context='adhoc', host="0.0.0.0")
