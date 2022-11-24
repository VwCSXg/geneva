from scapy.packet import Raw

from geneva.layers.layer import Layer

class RawLayer(Layer):
    """
    Defines an interface for the scapy Raw layer.
    """
    name = "Raw"
    protocol = Raw
    _fields = []
    fields = []