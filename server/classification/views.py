from os import environ, path

import numpy as np
import tensorflow as tf
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from tensorflow import keras

from .prediction import dog_breeds

environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Create your views here.

IMG_SIZE = 224
model_name = "custom-mobilenetv2-Adam.h5"
model = keras.models.load_model(
    path.join(settings.BASE_DIR, "classification", model_name)
)


def preprocess_image(path):
    image = tf.keras.utils.load_img(path, target_size=(IMG_SIZE, IMG_SIZE))
    image_array = tf.keras.utils.img_to_array(image)
    return tf.cast(tf.expand_dims(image_array, 0) / 255.0, dtype=tf.float32)


class DogBreedDectectionView(APIView):
    parser_classes = [MultiPartParser]

    http_method_names = ["post"]

    def post(self, *args, **kwargs):
        dog_image_file = self.request.FILES["image"]

        image = preprocess_image(dog_image_file.file)

        pred = model.predict(image)
        score = tf.nn.softmax(pred[0])

        max_idx = np.argmax(score)
        class_pred = dog_breeds[max_idx]

        top_5 = tf.math.top_k(score, 5)

        top_5_values = top_5.values.numpy()
        top_5_indices = top_5.indices.numpy()

        top_5 = {
            dog_breeds[top_5_indices[i]]: f"{round(top_5_values[i] * 100, 2)}%"
            for i in range(5)
        }

        return Response(
            {
                "breed": class_pred,
                "best confidence": f"{top_5[class_pred]}",
                "top 5": top_5,
            }
        )
