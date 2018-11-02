from __future__ import division, print_function
# coding=utf-8

import os

import numpy as np
import tensorflow as tf
from skimage import io, transform

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

flower_dict = {0: 'dasiy', 1: 'dandelion', 2: 'roses', 3: 'sunflowers', 4: 'tulips'}

sess = tf.Session()

saver = tf.train.import_meta_graph('E:/hust-flowerclassify/models/model.ckpt.meta') # create the network
saver.restore(sess, tf.train.latest_checkpoint('E:/hust-flowerclassify/models/')) # load the parameters
print('model loaded,now begin...')

def model_predict(img_path):
    data = []
    img = io.imread(img_path)
    img = transform.resize(img, (100, 100))
    img = np.asarray(img)
    data.append(img)



    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    feed_dict = {x: data}

    logits = graph.get_tensor_by_name("logits_eval:0")


    classification_result = sess.run(logits, feed_dict)
    print(tf.argmax(classification_result))
    # index = tf.argmax(classification_result, 1).eval()
    index = np.reshape(classification_result, 5)
    index = np.argmax(index)
    return flower_dict[index]

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path)
        return preds

    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
