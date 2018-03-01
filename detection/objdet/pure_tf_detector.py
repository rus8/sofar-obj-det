""" Pure TensorFlow inference

Detector class provides method to perform detection using
TensorFlow and some postprocessing routines.
"""

import json

import cv2
import numpy as np
import tensorflow as tf

from .cython_utils.cy_yolo_findboxes import yolo_box_constructor
from .cython_utils.cy_yolo2_findboxes import box_constructor


class Detector:

    def __init__(self, pb_path, meta_path, gpu_name='', gpu_usage=0.0):
        """
        Initializes detector using files generated y Darkflow.

        :param pb_path: Path to protobuf file with saved TensorFlow model.
        :param meta_path: Path to meta file produced by Darkflow.
        :param gpu_name: Name of device to use according to TensorFlow conventions.
        :param gpu_usage: GPU usage in interval [0, 1].
        """
        self.graph = tf.Graph()
        device_name = gpu_name \
            if gpu_usage > 0.0 else None
        with tf.device(device_name):
            with self.graph.as_default() as g:
                self.build_from_pb(pb_path, meta_path, gpu_usage)
        return

    def build_from_pb(self, pb_path, meta_path, gpu_usage):
        """
        Build tensorflow graph from protobuf file. Setup metaparams and creates
        TensorFlow session.

        :param pb_path: Path to protobuf file with saved TensorFlow model.
        :param meta_path: Path to meta file produced by Darkflow.
        :param gpu_usage: GPU usage in interval [0, 1].
        """
        with tf.gfile.FastGFile(pb_path, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        tf.import_graph_def(
            graph_def,
            name=""
        )

        with open(meta_path, 'r') as fp:
            self.meta = json.load(fp)

        # Placeholders
        self.inp = tf.get_default_graph().get_tensor_by_name('input:0')
        self.feed = dict()  # other placeholders
        self.out = tf.get_default_graph().get_tensor_by_name('output:0')

        self.setup_meta_ops(gpu_usage)

        return

    def setup_meta_ops(self, gpu_usage):
        """
        Setup some metaparams and and create TensorFlow session.

        :param gpu_usage: GPU usage in interval [0, 1].
        """
        cfg = dict({
            'allow_soft_placement': False,
            'log_device_placement': False
        })

        utility = min(gpu_usage, 1.)
        if utility > 0.0:
            # self.say('GPU mode with {} usage'.format(utility))
            cfg['gpu_options'] = tf.GPUOptions(
                per_process_gpu_memory_fraction=utility)
            cfg['allow_soft_placement'] = True
        else:
            # self.say('Running entirely on CPU')
            cfg['device_count'] = {'GPU': 0}


        self.sess = tf.Session(config=tf.ConfigProto(**cfg))
        self.sess.run(tf.global_variables_initializer())

        return

    def resize_input(self, im):
        """
        Resize image to size specified in metaparams, which is required
         for network input.

        :param im: Original image.
        :return: Resized image.
        """
        h, w, c = self.meta['inp_size']
        imsz = cv2.resize(im, (w, h))
        imsz = imsz / 255.
        imsz = imsz[:, :, ::-1]
        return imsz

    def findboxes(self, net_out, thresh):
        """
        Use cython functions adapted from Darkflow
        to perform postprocessing.

        :param net_out: Network output.
        :param thresh: Threshold for prediction confidence.
        :return: Bounding boxes of detected objects.
        """

        meta = self.meta
        boxes = []
        # boxes = yolo_box_constructor(meta, net_out, thresh)
        boxes = box_constructor(meta, net_out)

        return boxes

    def process_box(self, b, h, w, threshold):
        """
        Process bounding box to scale it for corresponding original image size
        and use meta data to find predicted class name.

        :param b: Bounding box.
        :param h: Original image height.
        :param w: Original image width.
        :param threshold: Threshold for prediction confidence.
        :return: Bounding box coordinates, predicted class name,
                and prediction confidence.
        """
        max_indx = np.argmax(b.probs)
        max_prob = b.probs[max_indx]
        label = self.meta['labels'][max_indx]
        if max_prob > threshold:
            left = int((b.x - b.w / 2.) * w)
            right = int((b.x + b.w / 2.) * w)
            top = int((b.y - b.h / 2.) * h)
            bot = int((b.y + b.h / 2.) * h)
            if left < 0:  left = 0
            if right > w - 1: right = w - 1
            if top < 0:   top = 0
            if bot > h - 1:   bot = h - 1
            mess = '{}'.format(label)
            return (left, right, top, bot, mess, max_prob)
        return None

    # def postprocess(self, net_out, im, thresh):
    #     """
    #     Takes network output, collects bounding boxes and return them.
    #
    #     :param net_out:
    #     :param im: Image
    #     :param thresh:
    #     :return:
    #     """
    #     meta = self.meta
    #     threshold = thresh
    #     colors, labels = meta['colors'], meta['labels']
    #
    #     boxes = self.findboxes(net_out)
    #
    #     h, w, _ = im.shape
    #     boxes = []
    #     for b in boxes:
    #         boxResults = self.process_box(b, h, w, threshold)
    #         if boxResults is None:
    #             continue
    #         left, right, top, bot, label, max_indx, confidence = boxResults
    #         boxes.append(boxResults)

    def return_predict(self, im, threshold):
        """
        Main function to use to perform detection.

        Performs prediction and constructs dictionary for each bounding box in the following
        format:
        {'bottomright': {'x': 264, 'y': 213}, 'confidence': 0.3534133, 'label': 'car', 'topleft': {'x': 193, 'y': 174}}

        :param im: Input image.
        :param threshold: Threshold for prediction confidence.
        :return: List of bounding boxes.
        """
        assert isinstance(im, np.ndarray), \
            'Image is not a np.ndarray'
        h, w, _ = im.shape
        im = self.resize_input(im)
        this_inp = np.expand_dims(im, 0)
        feed_dict = {self.inp: this_inp}

        out = self.sess.run(self.out, feed_dict)[0]
        boxes = self.findboxes(out, threshold)
        boxesInfo = list()
        for box in boxes:
            tmpBox = self.process_box(box, h, w, threshold)
            if tmpBox is None:
                continue
            boxesInfo.append({
                "label": tmpBox[4],
                "confidence": tmpBox[5],
                "topleft": {
                    "x": tmpBox[0],
                    "y": tmpBox[2]},
                "bottomright": {
                    "x": tmpBox[1],
                    "y": tmpBox[3]}
            })
        return boxesInfo