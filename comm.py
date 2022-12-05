import argparse
from threading import Thread
from serial import Serial
import time
from cli import CLI
from controller import Controller

def run(serial, source, destination, retransmissions, fec):
    try:
        # Open serial port
        s = Serial(serial, 115200, timeout=1)
        time.sleep(0.5)
    except:
        print("Could not open port. Please try again.")
        exit()

    # Set device address
    s.write(bytes("a[%s]\n" % source, "ascii"))
    time.sleep(0.5)
    s.write(bytes("a[%s]\n" % source, "ascii"))
    time.sleep(0.5)

    # Set number of retransmissions
    s.write(bytes("c[1,0,%s]\n" % retransmissions, "ascii"))
    time.sleep(0.1)

    # Set FEC threshold
    s.write(bytes("c[0,1,%s]\n" % fec, "ascii"))
    time.sleep(0.1)

    print("Ready")

    # Instantiate a gateway thread that sends and receives messages.
    gateway = Controller(s, destination)
    gateway_thread = Thread(target=gateway.event_loop)
    gateway_thread.start()

    # Instantiate client
    cli = CLI(gateway)
    cli.event_loop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('serial')
    parser.add_argument('source')
    parser.add_argument('destination')
    parser.add_argument('-r', '--retransmissions', default=5)
    parser.add_argument('-f', '--fec', default=30)

    args = parser.parse_args()

    run(args.serial, args.source, args.destination, args.retransmissions, args.fec)
