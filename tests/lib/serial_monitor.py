#! /usr/bin/env python3

import serial
import sys
import threading
import time
import serial

class SerialReaderWriter:
    def __init__(self, device: str = "/dev/ttyACM0", baudrate: int = 115200) -> None:
        self.device = device
        self.baudrate = baudrate
        self.serial = serial.Serial(device, baudrate, timeout=1)
        self.rx_shutdown_flag = threading.Event()
        self.rx_thr = threading.Thread()
        self.output_lock = threading.Lock()
    
    def synchronized_print(self, message: str):
        with self.output_lock:
            print(message)

    def rx_thread(self):
        self.synchronized_print("starting rx_thread")
        while not self.rx_shutdown_flag.is_set():
            data = self.serial.readline().decode('utf-8', errors="ignore").strip()
            if len(data) > 0:
                with open("logfile.txt", "w+") as f:
                    f.writelines(data)
                f.close()

            if len(data) > 0:
                print(f"{self.device} >>> {data}")
        self.synchronized_print("stopping rx_thread")

    def createRxThread(self):
        self.synchronized_print(f"creating rx_trhead")
        self.rx_thr = threading.Thread(target=self.rx_thread)
        self.rx_thr.start()

    def stopRxThread(self):
        self.rx_shutdown_flag.set()
        
        if self.rx_thr.is_alive():
            self.rx_thr.join()

    def disconnect(self):
        self.serial.close()
    

def main(device: str = "/dev/ttyACM0", baudrate: int = 115200):
    TIMEOUT = 1
    try:
        ser = SerialReaderWriter(device=device, baudrate=baudrate)
        ser.synchronized_print(f"Connected to {ser.device} at {ser.baudrate} baud")
        
        ser.createRxThread()
        while True:
            command = input(f"{ser.device} <<< ")
            
            if command == "quit" or command == "exit":
                break
            else:
                ser.serial.write(f"{command}\n".encode("utf-8"))
                
        ser.synchronized_print(f"wakeup: attempting to stop rx_thread")
        ser.stopRxThread()
    except serial.SerialException as e:
        ser.synchronized_print(f"Serial error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        ser.synchronized_print("\nExiting...")
    finally:
        ser.disconnect()
        ser.synchronized_print("Serial connection closed")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Handles serial tty communication on linux systems")
    parser.add_argument("--device", "-d", default="/dev/ttyACM0")
    parser.add_argument("--baudrate", "-b", default=115200)
    args = parser.parse_args()
    
    main(args.device, args.baudrate)
