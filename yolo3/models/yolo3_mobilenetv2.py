"""YOLO_v3 Model Defined in Keras."""

from tensorflow.keras.layers import UpSampling2D, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2

from yolo3.models.layers import compose, DarknetConv2D, DarknetConv2D_BN_Leaky, Depthwise_Separable_Conv2D_BN_Leaky, make_last_layers, make_depthwise_separable_last_layers, make_spp_depthwise_separable_last_layers


def yolo_mobilenetv2_body(inputs, num_anchors, num_classes):
    """Create YOLO_V3 MobileNetV2 model CNN body in Keras."""
    mobilenetv2 = MobileNetV2(input_tensor=inputs, weights='imagenet', include_top=False)

    # input: 416 x 416 x 3
    # out_relu: 13 x 13 x 1280
    # block_13_expand_relu: 26 x 26 x 576
    # block_6_expand_relu: 52 x 52 x 192

    f1 = mobilenetv2.get_layer('out_relu').output
    # f1 :13 x 13 x 1280
    x, y1 = make_last_layers(f1, 576, num_anchors * (num_classes + 5))

    x = compose(
            DarknetConv2D_BN_Leaky(288, (1,1)),
            UpSampling2D(2))(x)

    f2 = mobilenetv2.get_layer('block_13_expand_relu').output
    # f2: 26 x 26 x 576
    x = Concatenate()([x,f2])

    x, y2 = make_last_layers(x, 192, num_anchors*(num_classes+5))

    x = compose(
            DarknetConv2D_BN_Leaky(96, (1,1)),
            UpSampling2D(2))(x)

    f3 = mobilenetv2.get_layer('block_6_expand_relu').output
    # f3 : 52 x 52 x 192
    x = Concatenate()([x, f3])
    x, y3 = make_last_layers(x, 96, num_anchors*(num_classes+5))

    return Model(inputs = inputs, outputs=[y1,y2,y3])


def yololite_mobilenetv2_body(inputs, num_anchors, num_classes):
    '''Create YOLO_v3 Lite MobileNetV2 model CNN body in keras.'''
    mobilenetv2 = MobileNetV2(input_tensor=inputs, weights='imagenet', include_top=False)

    # input: 416 x 416 x 3
    # out_relu: 13 x 13 x 1280
    # block_13_expand_relu: 26 x 26 x 576
    # block_6_expand_relu: 52 x 52 x 192

    f1 = mobilenetv2.get_layer('out_relu').output
    # f1 :13 x 13 x 1280
    x, y1 = make_depthwise_separable_last_layers(f1, 576, num_anchors * (num_classes + 5), block_id_str='17')

    x = compose(
            DarknetConv2D_BN_Leaky(288, (1,1)),
            UpSampling2D(2))(x)

    f2 = mobilenetv2.get_layer('block_13_expand_relu').output
    # f2: 26 x 26 x 576
    x = Concatenate()([x,f2])

    x, y2 = make_depthwise_separable_last_layers(x, 192, num_anchors * (num_classes + 5), block_id_str='18')

    x = compose(
            DarknetConv2D_BN_Leaky(96, (1,1)),
            UpSampling2D(2))(x)

    f3 = mobilenetv2.get_layer('block_6_expand_relu').output
    # f3 : 52 x 52 x 192
    x = Concatenate()([x, f3])
    x, y3 = make_depthwise_separable_last_layers(x, 96, num_anchors * (num_classes + 5), block_id_str='19')

    return Model(inputs = inputs, outputs=[y1,y2,y3])


def yololite_spp_mobilenetv2_body(inputs, num_anchors, num_classes):
    '''Create YOLO_v3 Lite SPP MobileNetV2 model CNN body in keras.'''
    mobilenetv2 = MobileNetV2(input_tensor=inputs, weights='imagenet', include_top=False)

    # input: 416 x 416 x 3
    # out_relu: 13 x 13 x 1280
    # block_13_expand_relu: 26 x 26 x 576
    # block_6_expand_relu: 52 x 52 x 192

    f1 = mobilenetv2.get_layer('out_relu').output
    # f1 :13 x 13 x 1280
    #x, y1 = make_depthwise_separable_last_layers(f1, 512, num_anchors * (num_classes + 5), block_id_str='14')
    x, y1 = make_spp_depthwise_separable_last_layers(f1, 576, num_anchors * (num_classes + 5), block_id_str='17')

    x = compose(
            DarknetConv2D_BN_Leaky(288, (1,1)),
            UpSampling2D(2))(x)

    f2 = mobilenetv2.get_layer('block_13_expand_relu').output
    # f2: 26 x 26 x 576
    x = Concatenate()([x,f2])

    x, y2 = make_depthwise_separable_last_layers(x, 192, num_anchors * (num_classes + 5), block_id_str='18')

    x = compose(
            DarknetConv2D_BN_Leaky(96, (1,1)),
            UpSampling2D(2))(x)

    f3 = mobilenetv2.get_layer('block_6_expand_relu').output
    # f3 : 52 x 52 x 192
    x = Concatenate()([x, f3])
    x, y3 = make_depthwise_separable_last_layers(x, 96, num_anchors * (num_classes + 5), block_id_str='19')

    return Model(inputs = inputs, outputs=[y1,y2,y3])


def tiny_yolo_mobilenetv2_body(inputs, num_anchors, num_classes):
    '''Create Tiny YOLO_v3 MobileNetV2 model CNN body in keras.'''
    mobilenetv2 = MobileNetV2(input_tensor=inputs, weights='imagenet', include_top=False)

    # input: 416 x 416 x 3
    # out_relu: 13 x 13 x 1280
    # block_13_expand_relu: 26 x 26 x 576
    # block_6_expand_relu: 52 x 52 x 192

    x1 = mobilenetv2.get_layer('block_13_expand_relu').output

    x2 = mobilenetv2.get_layer('out_relu').output
    x2 = DarknetConv2D_BN_Leaky(576, (1,1))(x2)

    y1 = compose(
            DarknetConv2D_BN_Leaky(1280, (3,3)),
            #Depthwise_Separable_Conv2D_BN_Leaky(filters=1280, kernel_size=(3, 3), block_id_str='17'),
            DarknetConv2D(num_anchors*(num_classes+5), (1,1)))(x2)

    x2 = compose(
            DarknetConv2D_BN_Leaky(288, (1,1)),
            UpSampling2D(2))(x2)
    y2 = compose(
            Concatenate(),
            DarknetConv2D_BN_Leaky(576, (3,3)),
            #Depthwise_Separable_Conv2D_BN_Leaky(filters=576, kernel_size=(3, 3), block_id_str='18'),
            DarknetConv2D(num_anchors*(num_classes+5), (1,1)))([x2,x1])

    return Model(inputs, [y1,y2])


def tiny_yololite_mobilenetv2_body(inputs, num_anchors, num_classes):
    '''Create Tiny YOLO_v3 Lite MobileNetV2 model CNN body in keras.'''
    mobilenetv2 = MobileNetV2(input_tensor=inputs, weights='imagenet', include_top=False)

    # input: 416 x 416 x 3
    # out_relu: 13 x 13 x 1280
    # block_13_expand_relu: 26 x 26 x 576
    # block_6_expand_relu: 52 x 52 x 192

    x1 = mobilenetv2.get_layer('block_13_expand_relu').output

    x2 = mobilenetv2.get_layer('out_relu').output
    x2 = DarknetConv2D_BN_Leaky(576, (1,1))(x2)

    y1 = compose(
            #DarknetConv2D_BN_Leaky(1280, (3,3)),
            Depthwise_Separable_Conv2D_BN_Leaky(filters=1280, kernel_size=(3, 3), block_id_str='17'),
            DarknetConv2D(num_anchors*(num_classes+5), (1,1)))(x2)

    x2 = compose(
            DarknetConv2D_BN_Leaky(288, (1,1)),
            UpSampling2D(2))(x2)
    y2 = compose(
            Concatenate(),
            #DarknetConv2D_BN_Leaky(576, (3,3)),
            Depthwise_Separable_Conv2D_BN_Leaky(filters=576, kernel_size=(3, 3), block_id_str='18'),
            DarknetConv2D(num_anchors*(num_classes+5), (1,1)))([x2,x1])

    return Model(inputs, [y1,y2])
