
def vggCut():
    import keras_vggface
    import tensorflow.keras as keras
    modelVggCut = keras_vggface.VGGFace(
        model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')

    modelVggCut.compile(
        optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return modelVggCut
