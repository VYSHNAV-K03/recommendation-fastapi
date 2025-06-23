import numpy as np
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Embedding, Flatten, Dot, Concatenate,Dense

class Autoencoder(Model):
    def __init__(self, input_dim):
        super(Autoencoder, self).__init__()
        self.encoder = Sequential([
            Dense(64, activation='relu'),
            Dense(32, activation='relu')
        ])
        self.decoder = Sequential([
            Dense(64, activation='relu'),
            Dense(input_dim, activation='sigmoid')
        ])

    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded



def build_ncf_model(num_users, num_items, embedding_size=50):
    user_input = Input(shape=(1,))
    item_input = Input(shape=(1,))
    
    user_embedding = Embedding(input_dim=num_users, output_dim=embedding_size)(user_input)
    item_embedding = Embedding(input_dim=num_items, output_dim=embedding_size)(item_input)

    user_vec = Flatten()(user_embedding)
    item_vec = Flatten()(item_embedding)

    concatenated = Concatenate()([user_vec, item_vec])
    x = Dense(64, activation='relu')(concatenated)
    x = Dense(32, activation='relu')(x)
    output = Dense(1, activation='linear')(x)

    model = Model(inputs=[user_input, item_input], outputs=output)
    model.compile(optimizer='adam', loss='mse')
    return model