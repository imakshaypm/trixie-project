import cv2
import tensorflow as tf
from keras.models import model_from_json
import numpy as np

CATEGORIES = ["Angry", "Disgusted", "Fearful", "Happy", "Neutral", "Sad", "Surprised"]


def prepare(filepath):
    IMG_SIZE = 48  # 50 in txt-based
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


def em_predict():
    json_file = open('emotion_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    emotion_model = model_from_json(loaded_model_json)

    # load weights into new model
    emotion_model.load_weights("emotion_model.h5")

    # model = tf.keras.models.load_model("emotion_model.h5")

    prediction = emotion_model.predict([prepare('image.png')])
    result = str(CATEGORIES[int(np.argmax(prediction[0]))])
    # print(emotion_model.summary())
    return result

# em_predict()