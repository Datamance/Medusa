# -*- coding: utf-8 -*-

"""Main module.

We should be able to have workers that are just generators - they continuously yield to the pipeline.

We should also be able to have workers that do one thing then return.
"""

import sys
import asyncio
import struct

# import typing


class Master:
    """Master class, coordinates all the workers."""

    def __init__(self):
        """Constructor."""
        self._process_pool = []

    async def _spawn_worker(self, worker_file: str):
        """Spawns the worker.

        TODO:
            + Check the worker file being imported.
                - Does it have a main() function?
                - Are the args for that function properly annotated?
                - Does it return what it says it returns?

            If all of these check out, then we can create a new temp file where we:
                1) Import the module.main function
                2) while True
                    a) Read bytes from sys.stdin
                    b) struct-unpack those bytes according to the types specified in the signature
                    c) feed them to the module.main(), the result of which we store in a variable
                    d) struct-pack that variable according to return signature
                    e) write those bytes to sys.stdout

            In the main thread, we will have the event loop always managing the input and output
            queues for all of these processes.

            This means that, with each process, the user has to have some way to be explicit about
            where they want the return args to go.

            This also means that each queue has to have some concept of argument "slots" whereby the recieving
            worker doesn't execute until all arguments have been recieved from various parts of the pipeline.
            This is going to allow for situations where some queues grow larger than others, but processing
            order is always maintained.

        """

        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-u",
            worker_file,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        self._process_pool.append(process)


if __name__ == "__main__":
    print(asyncio.subprocess, asyncio, struct)
