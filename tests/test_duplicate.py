import sys
# Include the root of the project
sys.path.append("..")

import geneva.actions.duplicate
import geneva.layers.packet
import geneva.actions.strategy
import geneva.actions.utils

from scapy.all import IP, TCP


def test_duplicate(logger):
    """
    Tests the duplicate action primitive.
    """
    duplicate = geneva.actions.duplicate.DuplicateAction()
    assert str(duplicate) == "duplicate", "Duplicate returned incorrect string representation: %s" % str(duplicate)

    packet = geneva.layers.packet.Packet(IP(src="127.0.0.1", dst="127.0.0.1") / TCP(sport=2222, dport=3333, seq=100, ack=100, flags="S"))
    packet1, packet2 = duplicate.run(packet, logger)
    assert id(packet1) != id(packet2), "Duplicate aliased packet objects"
    duplicate.mutate()
