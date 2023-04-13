from flask import Flask, render_template, request, redirect, url_for, session, send_file
import requests
import os
from werkzeug.utils import secure_filename
import base64
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def main():
  return render_template("index1.html")


API_URL = "https://api-inference.huggingface.co/models/sunilrufus/Leaf_disease"
headers = {"Authorization": "Bearer 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"}
app.config["IMAGE_UPLOADS"] = "./"
app.config['UPLOAD_FOLDER'] = 'static/'


def query(filename):
  with open(filename, "rb") as f:
    data = f.read()
  response = requests.post(API_URL, headers=headers, data=data)
  return response.json()


@app.route('/image')
def get_image():
  filename = 'leaf_blight_tomato.jpg'
  return send_file(filename, mimetype='image/jpg')


@app.route('/cv', methods=['POST'])
def success():
  if request.method == 'POST':
    f = request.files['file']
    """f.save(f.filename)
    f.save(
      os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))"""

    #with open(f.filename, "rb") as f:
    data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    print(response)
    encoded_image = base64.b64encode(data).decode('utf-8')
    output = response.json()
    try:
      out1 = "The probability of prediction for the leaf is " + str(output[0]['score'] * 100) + " % " + "- " + str(output[0]['label'])
      out2 = " and " + str(output[1]['score'] * 100) + " % " + "- " + str(output[1]['label'])
      out = out1 + out2
    finally:
      out = response.json()
    #return response.json()
    return render_template("ackno.html", name=out, encoded_image=encoded_image)
    


app.run(host='0.0.0.0', port=81)
