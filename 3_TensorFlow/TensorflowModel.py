import tensorflow as tf
import os


class TensorflowModel(object):
    # session
    # loss
    # placeholder for training data X []
    # X_img
    # placeholder for training data y
    # y_img
    # trainStep
    strides = [1,1,1,1]
    padding = 'SAME'
    std_dev = 0.01
    init_bias = 0.1
    # loss
    blocks = []
    tv=0.0001
    # train_step
    summary_dir = "./_Summary"


    def __init__(self, char_width_px):
        self.session = tf.InteractiveSession()
        self.X = tf.placeholder(tf.float32, [None, char_width_px, char_width_px], name='X')
        output_width = char_width_px/2
        self.y = tf.placeholder(tf.float32, [None, output_width, output_width], name='y')
        self.X_img = tf.reshape(self.X, shape = (-1, char_width_px, char_width_px, 1))
        self.y_img = tf.reshape(self.y, shape = (-1, output_width, output_width, 1))
        self.phase_train = tf.placeholder(tf.bool, name='phase_train')
        self.learning_rate = tf.placeholder(tf.float32, name="learning_rate")
        self.keepProb = tf.placeholder(tf.float32, name="keepProb")
        self.train_writer = tf.train.SummaryWriter(os.path.join(self.summary_dir, 'train'),
                                              self.session.graph)
        self.validation_writer = tf.train.SummaryWriter(os.path.join(self.summary_dir, 'validation'))




    ########################## Layers of CNN ##################################
    # generate a CNN 2D block
    # x: input tensor
    # shape: [sz, sz, sz_model.add_block()in_filter, sz_out_filter]
    def get_conv2D_block(self, input_tensor, shape):
        sz_out_filter = shape[-1]
        # init weight
        W = tf.Variable(tf.truncated_normal(shape, self.std_dev, name='W'))
        # init bias
        b = tf.Variable(tf.constant(self.init_bias, shape=[sz_out_filter]), name='b')
        conv = tf.nn.conv2d(input_tensor, W, self.strides, self.padding) + b
        conv_bn = self.batch_norm(conv)
        return tf.nn.relu(conv_bn)

    def add_block(self, shape):
        x = (self.X_img if self.blocks == [] else self.blocks[-1])
        new_block = self.get_conv2D_block(x, shape)
        self.blocks.append(new_block)

    def add_block_group(self, shape, n):
        for _ in range(n):
            self.add_block(shape)

    def pool(self):
        return tf.nn.max_pool(self.blocks[-1], ksize=[1,2,2,1], strides=[1,2,2,1], padding=self.padding)

    def drop_out(self, pooled):
        return tf.sigmoid(tf.nn.dropout(pooled, keep_prob=self.keepProb))

    def batch_norm(self, x):
        out_filters = x.get_shape()[-1]
        beta = tf.Variable(tf.constant(0.0, shape=[out_filters]), name='beta', trainable=True)
        gamma = tf.Variable(tf.constant(1.0, shape=[out_filters]),name='gamma', trainable=True)
        batch_mean, batch_var = tf.nn.moments(x, [0, 1, 2], name='moments')
        ema = tf.train.ExponentialMovingAverage(decay=0.9)
        def mean_var_with_update():
            ema_apply_op = ema.apply([batch_mean, batch_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(batch_mean), tf.identity(batch_var)

        mean, var = tf.cond(self.phase_train,
                            mean_var_with_update,
                            lambda: (ema.average(batch_mean), ema.average(batch_var)))
        normed = tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
        return normed

    def compute_loss(self, dropped_out):
        self.tv_loss = self.tv * self.total_variation_loss(dropped_out, 80) # 80: img width
        self.mae_loss = tf.reduce_mean(tf.abs(self.y_img - dropped_out))
        self.loss = self.mae_loss + self.tv_loss

    def init_train_step(self, dropped_out):
        self.compute_loss(dropped_out)
         #tf.train.GradientDescentOptimizer(self.learning_rate).minimize(self.loss)
        self.train_step = tf.train.RMSPropOptimizer(self.learning_rate).minimize(self.loss)

    def total_variation_loss(self, x, side):
        """
        Total variation loss for regularization of image smoothness
        """
        loss = tf.nn.l2_loss(x[:, 1:, :, :] - x[:, :side - 1, :, :]) / side + \
               tf.nn.l2_loss(x[:, :, 1:, :] - x[:, :, :side - 1, :]) / side
        return loss

    # def get_block():
