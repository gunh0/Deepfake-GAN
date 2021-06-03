# %%
from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from tensorflow.keras import metrics
from tensorflow.keras.datasets import mnist
import numpy as np
from tensorflow.python.keras.backend_config import epsilon

# %%
batch_size = 100
original_dim = 784   # Height X Width
latent_dim = 2
intermediate_dim = 256
epochs = 50
epsilon_std = 1

# %%


def sampling(args: tuple):
    z_mean, z_log_var = args
    epsilon = K.random_normal(
        shape=(K.shape(z_mean)[0], latent_dim), mean=0, stddev=epsilon_std)
    return z_mean + K.exp(z_log_var/2)*epsilon


# %%
x = Input(shape=(original_dim,), name="input")   # Encoder
h = Dense(intermediate_dim, activation='relu', name="encoding")(x)
z_mean = Dense(latent_dim, name="mean")(h)
z_log_var = Dense(latent_dim, name="log-variance")(h)
z = Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var])
encoder = Model(x, [z_mean, z_log_var, z], name="encoder")
