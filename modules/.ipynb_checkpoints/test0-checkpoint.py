import tensorflow as tf
batch_size  = 100
h_size      = 28
w_size      = 28
c_size      = 1
hidden_size = 100
x_raw       = tf.placeholder(tf.float32, shape=[batch_size, h_size, w_size, c_size]) # [100, 28, 28, 1] 
x_split     = tf.split(x_raw, h_size, axis=1) # [100, 28, 28, 1] -> list of [100, 1, 28, 1]

y = tf.placeholder(tf.float32, shape=[batch_size, 10])

U = tf.Variable(tf.random_normal([w_size, hidden_size], stddev=0.01))
W = tf.Variable(tf.random_normal([hidden_size, hidden_size], stddev=0.01)) # always square
V = tf.Variable(tf.random_normal([hidden_size, 10], stddev=0.01))
s = {}
s_init = tf.random_normal(shape=[batch_size, hidden_size], stddev=0.01)
s[-1] = s_init
# ===================
for t, x_split in enumerate(x_split):
    x = tf.reshape(x_split, [batch_size, w_size]) # [100, 1, 28, 1] -> [100, 28]
    s[t] = tf.nn.tanh(tf.matmul(x, U) + tf.matmul(s[t-1], W))

o = tf.nn.softmax(tf.matmul(s[h_size-1], V))

# ===================
cost = -tf.reduce_mean(tf.log(tf.reduce_sum(o*y, axis=1)))
learning_rate = 0.1
trainer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

sess = tf.InteractiveSession()
init = tf.global_variables_initializer()
init.run()

import tensorflow.examples.tutorials.mnist.input_data as input_data

mnist = input_data.read_data_sets("data/", one_hot=True, reshape=False)
trainimgs, trainlabels, testimgs, testlabels \
    = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels 
ntrain, ntest, dim, nclasses \
    = trainimgs.shape[0], testimgs.shape[0], trainimgs.shape[1], trainlabels.shape[1]

test_inputs = testimgs[:batch_size]
test_outputs = testlabels[:batch_size]

def accuracy(network, t):
    
    t_predict = tf.argmax(network, axis=1)
    t_actual = tf.argmax(t, axis=1)

    return tf.reduce_mean(tf.cast(tf.equal(t_predict, t_actual), tf.float32))

acc = accuracy(o, y)
for _ in range(20):
    for i in range(trainlabels.shape[0]//batch_size):
        inputs = trainimgs[i*batch_size:batch_size*(1+i)]
        outputs = trainlabels[i*batch_size:batch_size*(1+i)]
        feed = {x_raw:inputs, y:outputs}
        trainer.run(feed)
acc.eval({x_raw:test_inputs, y:test_outputs})
# >> 0.92000002
sess.close()