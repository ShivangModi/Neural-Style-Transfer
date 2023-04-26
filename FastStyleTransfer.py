import base64
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf


class FastStyleTransfer:
    def __init__(self):
        self.__model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    @staticmethod
    def __load_image(img):
        max_dim = 512

        img = base64.b64decode(img.split("base64,")[-1])
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)

        shape = tf.cast(tf.shape(img)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        img = tf.image.resize(img, new_shape)
        img = img[tf.newaxis, :]
        return img

    def predict(self, content_img, style_img):
        content_img = self.__load_image(content_img)
        style_img = self.__load_image(style_img)
        convert = self.__model(tf.constant(content_img), tf.constant(style_img))[0]
        return np.squeeze(convert)
