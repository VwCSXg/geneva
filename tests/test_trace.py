import sys
import pytest
# Include the root of the project
sys.path.append("..")

import geneva.actions.trace
import geneva.layers.packet
import geneva.actions.strategy
import geneva.actions.utils
import evolve

from scapy.all import IP, TCP


def test_trace(logger):
    """
    Tests the trace action primitive.
    """
    trace = geneva.actions.trace.TraceAction(start_ttl=1, end_ttl=3)

    assert str(trace) == "trace{1:3}", "Trace returned incorrect string representation: %s" % str(trace)
    packet = geneva.layers.packet.Packet(IP(src="127.0.0.1", dst="127.0.0.1") / TCP(sport=2222, dport=3333, seq=100, ack=100, flags="S"))
    trace.run(packet, logger)

    print("Testing that trace will not run twice:")
    assert trace.run(packet, logger) == (None, None)

    trace = geneva.actions.trace.TraceAction(start_ttl=1, end_ttl=3)
    packet = geneva.layers.packet.Packet(TCP())
    assert trace.run(packet, logger) == (packet, None)

    s = "[TCP:flags:PA]-trace{1:3}-| \/ "
    assert str(geneva.actions.utils.parse(s, logger)) == s

    assert not trace.parse("10:4", logger)
    assert not trace.parse("10:hi", logger)
    assert not trace.parse("", logger)
