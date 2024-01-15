# Author: Nathan Trouvain at 08/07/2021 <nathan.trouvain@inria.fr>
# Licence: MIT License
# Copyright: Xavier Hinaut (2018) <xavier.hinaut@inria.fr>
from typing import Sequence

import numpy as np

from ..node import Node


def concat_forward(concat: Node, data):
    axis = concat.axis

    if not isinstance(data, np.ndarray):
        if len(data) > 1:
            return np.concatenate(data, axis=axis)
        else:
            return np.asarray(data)
    else:
        return data


def concat_initialize(concat: Node, x=None, **kwargs):
    if x is not None:
        if isinstance(x, np.ndarray):
            concat.set_input_dim(x.shape[1])
            concat.set_output_dim(x.shape[1])
        elif isinstance(x, Sequence):
            result = concat_forward(concat, x)
            concat.set_input_dim(tuple([u.shape[1] for u in x]))
            if result.shape[0] > 1:
                concat.set_output_dim(result.shape)
            else:
                concat.set_output_dim(result.shape[1])


class Concat(Node):
    """Concatenate vector of data along feature axis.

    This node is automatically created behind the scene when a node receives the input
    of more than one node.

    For more information on input concatenation, see
    :ref:`/user_guide/advanced_demo.ipynb#Input-to-readout-connections`

    :py:attr:`Concat.hypers` **list**

    ============= ======================================================================
    ``axis``      Concatenation axis.
    ============= ======================================================================
    """

    def __init__(self, axis=1, name=None):
        super(Concat, self).__init__(
            hypers={"axis": axis},
            forward=concat_forward,
            initializer=concat_initialize,
            name=name,
        )
