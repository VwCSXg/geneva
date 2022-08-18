import os
import pytest

import actions.duplicate
import geneva.actions.utils
import engine
import evolve


def test_compression_strategy(logger):
    """
    Tests dns compression strategy.
    """
    with engine.Engine(53, "[UDP:dport:53]-tamper{DNS:qd:compress}-|", server_side=False, environment_id="compress_test", output_directory=geneva.actions.utils.RUN_DIRECTORY, log_level=geneva.actions.utils.CONSOLE_LOG_LEVEL):
        os.system("dig @8.8.8.8 google.com")
