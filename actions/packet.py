import copy
import random

import actions.layer


_SUPPORTED_LAYERS = [
    actions.layer.IPLayer,
    actions.layer.TCPLayer,
    actions.layer.UDPLayer
]
SUPPORTED_LAYERS = _SUPPORTED_LAYERS


class Packet():
    """
    Defines a Packet class, a convenience wrapper around
    scapy packets for ease of use.
    """
    def __init__(self, packet=None):
        """
        Initializes the packet object.
        """
        self.packet = packet
        self.layers = self.setup_layers()
        self.sleep = 0

    def __str__(self):
        """
        Defines string representation for the packet.
        """
        return self._str_packet(self.packet)

    @staticmethod
    def _str_packet(packet):
        """
        Static method to print a scapy packet.
        """
        if packet.haslayer("TCP"):
            return "TCP %s:%d --> %s:%d [%s] %s: %s" % (
                packet["IP"].src,
                packet["TCP"].sport,
                packet["IP"].dst,
                packet["TCP"].dport,
                packet["TCP"].sprintf('%TCP.flags%'),
                str(packet["TCP"].chksum),
                Packet._str_load(packet["TCP"], "TCP"))
        elif packet.haslayer("UDP"):
            return "UDP %s:%d --> %s:%d %s: %s" % (
                packet["IP"].src,
                packet["UDP"].sport,
                packet["IP"].dst,
                packet["UDP"].dport,
                str(packet["UDP"].chksum),
                Packet._str_load(packet["UDP"], "UDP"))
        load = ""
        if hasattr(packet["IP"], "load"):
            load = str(bytes(packet["IP"].load))
        return "%s --> %s: %s" % (
            packet["IP"].src,
            packet["IP"].dst,
            load)

    @staticmethod
    def _str_load(packet, protocol):
        """
        Prints packet payload
        """
        return str(packet[protocol].payload)

    def __bytes__(self):
        """
        Returns packet's binary representation.
        """
        return bytes(self.packet)

    def show(self, **kwargs):
        """
        Calls scapy's show method.
        """
        return self.packet.show(**kwargs)

    def show2(self, **kwargs):
        """
        Calls scapy's show method.
        """
        return self.packet.show2(**kwargs)

    def read_layers(self):
        """
        Generator that yields parsed Layer objects from the protocols in the given packet.
        """
        iter_packet = self.packet
        while iter_packet:
            if iter_packet.name.lower() == "raw":
                return
            parsed_layer = Packet.parse_layer(iter_packet)
            if parsed_layer:
                yield parsed_layer
                iter_packet = parsed_layer.get_next_layer()
            else:
                iter_packet = iter_packet.payload

    def has_supported_layers(self):
        """
        Checks if this packet contains supported layers.
        """
        return bool(self.layers)

    def setup_layers(self):
        """
        Sets up a lookup dictionary for the given layers in this packet.
        """
        layers = {}
        for layer in self.read_layers():
            layers[layer.name.upper()] = layer
        return layers

    def copy(self):
        """
        Deep copies this packet. This method is required because it is not safe
        to use copy.deepcopy on this entire packet object, because the parsed layers
        become disassociated with the underlying packet layers, which breaks layer
        setting.
        """
        return Packet(copy.deepcopy(self.packet))

    @staticmethod
    def parse_layer(to_parse):
        """
        Takes a given scapy layer object and returns a Geneva Layer object.
        """
        for layer in SUPPORTED_LAYERS:
            if layer.name_matches(to_parse.name):
                return layer(to_parse)

    def haslayer(self, layer):
        """
        Checks if a given layer is in the packet.
        """
        return self.packet.haslayer(layer)

    def __getitem__(self, item):
        """
        Returns a layer.
        """
        return self.packet[item]

    def set(self, str_protocol, field, value):
        """
        Sets the given protocol field to the given value.

        Raises AssertionError if the protocol is not present.
        """
        assert self.haslayer(str_protocol), "Given protocol %s is not in packet." % str_protocol
        assert str_protocol in self.layers, "Given protocol %s is not permitted." % str_protocol

        # Recalculate the checksums
        if self.haslayer("IP"):
            del self.packet["IP"].chksum
        if self.haslayer("TCP"):
            del self.packet["TCP"].chksum

        return self.layers[str_protocol].set(self.packet, field, value)

    def get(self, str_protocol, field):
        """
        Retrieves the value of a given field for a given protocol.

        Raises AssertionError if the protocol is not present.
        """
        assert self.haslayer(str_protocol), "Given protocol %s is not in packet." % str_protocol
        assert str_protocol in self.layers, "Given protocol %s is not permitted." % str_protocol

        return self.layers[str_protocol].get(field)

    def gen(self, str_protocol, field):
        """
        Generates a value of a given field for a given protocol.

        Raises AssertionError if the protocol is not present.
        """
        assert self.haslayer(str_protocol), "Given protocol %s is not in packet." % str_protocol
        assert str_protocol in self.layers, "Given protocol %s is not permitted." % str_protocol

        return self.layers[str_protocol].gen(field)

    @classmethod
    def parse(cls, str_protocol, field, value):
        """
        Parses a given value for a given field of a given protocool.

        Raises AssertionError if the protocol is not present.
        """
        parsing_layer = None
        for layer in SUPPORTED_LAYERS:
            if layer.name_matches(str_protocol):
                parsing_layer = layer(None)

        assert parsing_layer, "Given protocol %s is not permitted." % str_protocol

        return parsing_layer.parse(field, value)

    def get_random_layer(self):
        """
        Retrieves a random layer from this packet.
        """
        return self.layers[random.choice(list(self.layers.keys()))]

    def get_random(self):
        """
        Retrieves a random protocol, field, and value from this packet.
        """
        layer = self.get_random_layer()
        field, value = layer.get_random()
        return layer.protocol, field, value

    @staticmethod
    def gen_random():
        """
        Generates a possible random protocol, field, and value.
        """
        # layer is a Geneva Layer class - to instantiate it, we must give it a layer
        # to use. Every Geneva Layer stores the underlying scapy layer it wraps,
        # so simply invoke that as a default.
        layer = random.choice(SUPPORTED_LAYERS)
        layer_obj = layer(layer.protocol())
        field, value = layer_obj.gen_random()
        return layer.protocol, field, value

    @staticmethod
    def get_supported_protocol(protocol):
        """
        Checks if the given protocol exists in the SUPPORTED_LAYERS list.
        """
        for layer in SUPPORTED_LAYERS:
            if layer.name_matches(protocol.upper()):
                return layer

        return None
