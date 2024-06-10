from io import BytesIO

import numpy as np
import tensorflow as tf
from fastapi import APIRouter, UploadFile

from classification.ml import dog_breeds, model, preprocess_image

router = APIRouter(prefix="/classification")


@router.post("/dog-breeds")
async def predict_dog_breed(image_file: UploadFile):
    content_bytes = await image_file.read()
    image = preprocess_image(BytesIO(content_bytes))
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

    return {
        "breed": class_pred,
        "best confidence": f"{top_5[class_pred]}",
        "top 5": top_5,
    }
