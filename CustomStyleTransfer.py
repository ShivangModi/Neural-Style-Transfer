import base64
import numpy as np
import tensorflow as tf

from PIL import Image
import matplotlib.pyplot as plt




class CustomStyleTransfer:
    def __init__(self, content, style, alpha, beta):
        self.content_layers = ['block5_conv2']
        self.style_layers = [f'block{i}_conv1' for i in range(1, 6)]

        self.num_content_layers = len(self.content_layers)
        self.num_style_layers = len(self.style_layers)

        self.content_weight = 1000*(alpha-1) + 10000
        self.style_weight = beta

        self.epochs = 10
        self.batch = 100

        self.content_img = self.__load_image(content)
        self.style_img = self.__load_image(style)

        self.style_targets = self.__model(self.style_img)['style']
        self.content_targets = self.__model(self.content_img)['content']

        self.image = tf.Variable(self.content_img)
        self.opt = tf.keras.optimizers.legacy.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

    @staticmethod
    def __load_image(img):
        max_dim = 512

        # img = tf.io.read_file(img)
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

    @staticmethod
    def __vgg_layers(layer_names):
        vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
        vgg.trainable = False

        outputs = [vgg.get_layer(name).output for name in layer_names]

        return tf.keras.Model([vgg.input], outputs)

    @staticmethod
    def __gram_matrix(input_tensor):
        result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
        input_shape = tf.shape(input_tensor)
        num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)

        return result/num_locations

    @staticmethod
    def __clip_0_1(image):
        return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)

    def style_content_loss(self, outputs):
        style_outputs = outputs['style']
        content_outputs = outputs['content']
        style_loss = tf.add_n([tf.reduce_mean((style_outputs[name] - self.style_targets[name]) ** 2)
                               for name in style_outputs.keys()])
        style_loss *= self.style_weight / self.num_style_layers

        content_loss = tf.add_n([tf.reduce_mean((content_outputs[name] - self.content_targets[name]) ** 2)
                                 for name in content_outputs.keys()])

        content_loss *= self.content_weight / self.num_content_layers
        loss = style_loss + content_loss
        return loss

    def train_step(self):
        with tf.GradientTape() as tape:
            outputs = self.__model(self.image)
            loss = self.style_content_loss(outputs)

        grad = tape.gradient(loss, self.image)
        self.opt.apply_gradients([(grad, self.image)])
        self.image.assign(self.__clip_0_1(self.image))

    def tensor_to_image(self):
        tensor = self.image * 255.0
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor) > 3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
        return Image.fromarray(tensor)
    
    def __model(self, inputs):
        vgg = self.__vgg_layers(self.style_layers + self.content_layers)
        vgg.trainable = False
        
        inputs = inputs*255
        preprocessed_inputs = tf.keras.applications.vgg19.preprocess_input(inputs)
        outputs = vgg(preprocessed_inputs)

        style_outputs, content_outputs = (outputs[:self.num_style_layers], outputs[self.num_style_layers:])
        style_outputs = [self.__gram_matrix(style_output) for style_output in style_outputs]

        style_dict = {style_name: value for style_name, value in zip(self.style_layers, style_outputs)}
        content_dict = {content_name: value for content_name, value in zip(self.content_layers, content_outputs)}
        return {'content': content_dict, 'style': style_dict}

# if __name__ == "__main__":
#     cst = CustomStyleTransfer('Image/DSC_0053.jpg', 'Image/width-420_Ss5zyUS.jpg', 10000, 0.08)
#     fig = None
#     for _ in range(cst.epochs):
#         for _ in range(cst.batch):
#             cst.train_step()
#             fig = cst.tensor_to_image()
#     print('finish')
