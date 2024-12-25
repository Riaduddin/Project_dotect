import tensorflow.keras.backend as K
import tensorflow as tf
def euclidean_distance(vectors):
    (featsA, featsB) = vectors

     # Reshape to ensure 2D tensors if necessary
    featsA = tf.reshape(featsA, (tf.shape(featsA)[0], -1))  # Reshape to (batch_size, embedding_dim)
    featsB = tf.reshape(featsB, (tf.shape(featsB)[0], -1))  # Reshape to (batch_size, embedding_dim)

    sumSquared = K.sum(K.square(featsA - featsB), axis=1, keepdims=True)
    return K.sqrt(K.maximum(sumSquared, K.epsilon()))  # To avoid division by zero

# Define the contrastive loss function
def contrastive_loss(y, y_pred,margin):
    # Contrastive Loss
    squared_preds = K.square(y_pred)
    squared_margin = K.square(K.maximum(margin - y_pred, 0))
    loss = K.mean(y * squared_preds + (1 - y) * squared_margin)
    return loss

# Define the combined loss function (contrastive loss + binary cross-entropy)
def combined_loss(y_true, y_pred):
    # Contrastive loss
    margin = 1.0
    contrastive_loss_value = contrastive_loss(y_true,y_pred,margin)

    # Binary Cross-Entropy Loss (for additional training signal)
    bce_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=y_true, logits=y_pred)  # Can use either featsA or featsB
    bce_loss = tf.reduce_mean(bce_loss)

    # Combine both losses
    return contrastive_loss_value + bce_loss