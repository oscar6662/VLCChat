from queue import Queue, Empty
import sys
from serial import Serial, SerialException
from queue import Queue


class Controller():
    def __init__(self, serial: Serial, recipient: str):
        self.s = serial
        self.recipient = recipient
        self.send_queue = Queue(maxsize=10)
        self.receive_queue = Queue(maxsize=10)

    def enqueue_message_for_sending(self, string: str):
        self.send_queue.put((string, self.recipient), timeout=0.1)

    def get_message(self) -> str | None:
        try:
            return self.receive_queue.get(timeout=0.1)
        except Empty:
            return None

    def send_from_queue(self):
        # Get message from send queue
        try:
            (message, recipient) = self.send_queue.get(timeout=0.1)
            self.send_queue.task_done()
        except Empty:
            return
        
        # Write message for transmission to serial
        raw_output = bytes(f"m[{message}\0,{recipient}]\n", "ascii")
        self.s.write(raw_output)

        # Await for transmission completion
        response = self.receive()
        if "1" not in response:
            print("Error: Not sent")
        while self.receive() != "m[D]":
            pass

    def receive(self) -> str:
        # Read from serial
        input = self.s.read_until().decode("ascii").strip()

        # Check if received message is of type DATA
        if input.startswith("m[R,D,"):
            self.receive_queue.put((input[6:-1].strip()))
        return input

    def event_loop(self):
        try:
            # Alternate between receiving and sending messages
            while True:
                self.receive()
                self.send_from_queue()
        except SerialException:
            sys.exit()

