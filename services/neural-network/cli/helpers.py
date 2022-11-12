import os


def set_reasonable_logging_settings():
    """Set loggers to a verbosity level  appropriate for user interaction"""
    # tensorflow.org/datasets/cli#disable_tf_logs_on_import
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

    # Turn off tensorflow warnings (https://www.tensorflow.org/api_docs/python/tf/get_logger)
    from logging import ERROR

    from tensorflow import get_logger as get_tensorflow_logger

    get_tensorflow_logger().setLevel(ERROR)

    # Abseil (https://abseil.io/docs/python/guides/logging) is a tensorflow dependency and is
    # the cause of warnings about convolutional layer name output when exporting
    from absl import logging as absl_logging

    absl_logging.set_verbosity(absl_logging.ERROR)
