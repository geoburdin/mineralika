from __future__ import division, print_function
# coding=utf-8

import os
import PIL
import numpy as np
import tensorflow as tf

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.models import model_from_json

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model_on_xception_weights.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(lr=1e-6),
              metrics=['accuracy'])

# Define a flask app
app = Flask(__name__)
# print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(299, 299))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds


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
        preds = model_predict(file_path, loaded_model)
        print(preds)
        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        result = ''
        class_names = ('agate', 'amethyst', 'aquamarine', 'azurite', 'beryl', 'calcite', 'chalcedony', 'corundum', 'diamond', 'elbaite', 'fluorite', 'gypsum', 'opal', 'pyrite', 'quartz', 'rhodochrosite', 'spinel', 'topaz')
        result = str(class_names[np.argmax(preds)])
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)