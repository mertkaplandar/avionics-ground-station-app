import struct
import serial
import time

class HYIPacket:
    def __init__(self, port, baudrate):
        self.serial_port = serial.Serial(port, baudrate)
        self.counter = 1  # Initialize the counter value

    def __float_to_bytes__(self, f):
        return struct.pack('f', f)

    def create_packet(self, team_id=0, altitude=0.0, rocket_gps_altitude=0.0, rocket_latitude=0.0, rocket_longitude=0.0,
                      payload_gps_altitude=0.0, payload_latitude=0.0, payload_longitude=0.0,
                      stage_gps_altitude=0.0, stage_latitude=0.0, stage_longitude=0.0,
                      gyro_x=0.0, gyro_y=0.0, gyro_z=0.0,
                      accel_x=0.0, accel_y=0.0, accel_z=0.0,
                      angle=0.0, status=0):
        packet = bytearray(78)  # Creating a byte array of length 78

        # Fixed starting bytes
        packet[0] = 0xFF
        packet[1] = 0xFF
        packet[2] = 0x54
        packet[3] = 0x52

        # Team ID and Counter value
        packet[4] = team_id
        packet[5] = self.counter

        # Conversion of float values
        float_values = [
            altitude, rocket_gps_altitude, rocket_latitude, rocket_longitude,
            payload_gps_altitude, payload_latitude, payload_longitude,
            stage_gps_altitude, stage_latitude, stage_longitude,
            gyro_x, gyro_y, gyro_z,
            accel_x, accel_y, accel_z,
            angle
        ]

        index = 6
        for f in float_values:
            byte_array = self.__float_to_bytes__(f)
            for i in range(4):
                packet[index] = byte_array[i]
                index += 1

        # Status information
        packet[74] = status

        # Calculating checksum
        self.checksum = sum(packet[4:75]) % 256
        packet[75] = self.checksum 

        # Fixed bits
        packet[76] = 0x0D
        packet[77] = 0x0A

        return packet

    def return_packet(self, packet):
        formatted_packet = "[" + "][".join(f"{byte:02X}" for byte in packet) + "]"
        return formatted_packet

    def connect(self):
        try:
            if not self.serial_port.is_open:
                self.serial_port.open()
            print(f"Connected to {self.serial_port.port}")
            self.counter = 0
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")

    def disconnect(self):
        try:
            if self.serial_port.is_open:
                self.serial_port.close()
            print(f"Disonnected to {self.serial_port.port}")
        except serial.SerialException as e:
            print(f"Failed to disconnect: {e}")

    def write_serial_port(self, packet):
        try:
            if self.serial_port.is_open:
                self.serial_port.write(packet)
                print("Packet sent successfully.")
                if self.counter > 255:
                    self.counter = 0
                else:
                    self.counter = (self.counter + 1) % 256
            else:
                print("Serial port is not open.")
        except serial.SerialException as e:
            print(f"Failed to write to serial port: {e}")
            self.connect()

if __name__ == "__main__":
    port = "COM4"
    baudrate = 19200
    hyi = HYIPacket(port, baudrate)

    # Creating a sample packet with example values
    packet = hyi.create_packet(
        team_id=5,
        altitude=10.2,
        rocket_gps_altitude=1461.55,
        rocket_latitude=39.925019,
        rocket_longitude=32.836954,
        payload_gps_altitude=1361.61,
        payload_latitude=41.104593,
        payload_longitude=29.024411,
        stage_gps_altitude=1666.61,
        stage_latitude=41.091485,
        stage_longitude=29.061412,
        gyro_x=1.51,
        gyro_y=0.49,
        gyro_z=0.61,
        accel_x=0.0411,
        accel_y=0.0140,
        accel_z=-0.9552,
        angle=5.08,
        status=1
    )

    # Print the packet
    # print(hyi.print_packet(packet))
    
    # Connect to serial port and send the packet
    hyi.connect()
    time.sleep(3)
    for i in range(100):
        hyi.write_serial_port(packet)
        print(hyi.counter_value)
        time.sleep(1)
    print(hyi.print_packet(packet))
