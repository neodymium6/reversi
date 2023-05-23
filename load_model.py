import tensorflow as tf
import numpy as np
import osero_lib


def Predict(ban):
    #ban=[0]*64
    model = tf.keras.models.load_model("my_osero_model")
    probability_model = tf.keras.Sequential([model, 
                                            tf.keras.layers.Softmax()])
    X=np.zeros((1,8,8,2))
    for i in range(64):
        if ban[i]==1:
            X[0,i//8,i%8,1]=1
        elif ban[i]==2:
            X[0,i//8,i%8,0]=1
    predictions = probability_model.predict(X)
    can_put_te=[0]*64
    for i in range(64):
        if osero_lib.CanPut(ban,i,2):
            can_put_te[i]=1
    predictions[0]=predictions[0]*can_put_te
    #print(predictions[0,np.argmax(predictions[0])])
    return np.argmax(predictions[0])