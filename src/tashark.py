import os
import datetime
import pyshark
import subprocess
import sys
import argparse
import db_utils

frames = []
interface = ""
file_name = ""
pcap_file_name = ""


def capture_file():
    cap = pyshark.FileCapture(pcap_file_name)
    number_of_packets = 0
    for p in cap:
        number_of_packets = number_of_packets + 1
        if p.__contains__('HTTP'):
            http_layer = p.__getitem__('HTTP')
            if http_layer.get('http.request') and http_layer.get('file_data'):
                frames.append(http_layer.get_field('file_data'))

    print(f"Packets received: {str(number_of_packets)}")
    print(f"Frames: {str(len(frames))}")

    if len(frames) > 0:
        save_file()


def save_file():
    os.chdir('..')
    print('Saving frames into /frames/' + file_name)
    create_directory('frames')
    file = open('frames/' + file_name, "w")
    for f in frames:
        file.write(str(f) + "\n")
    db_utils.add_all(frames)
    file.close()


def create_directory(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError as error:
        print()


def get_file_name(extension):
    dt = datetime.datetime.now()
    return dt.strftime("%Y_%b_%d_%H_%M_%S") + "." + extension


def start_packet_sniffing():
    global pcap_file_name
    global tshark_process

    create_directory('tshark_logs')
    pcap_file_name = get_file_name('pcap')
    os.chdir('tshark_logs')
    # tshark_process = subprocess.Popen(args=['tshark', '-i', interface, '-w', pcap_file_name], stdout=subprocess.PIPE)

    subprocess.call(['tshark', '-i', interface, '-w', pcap_file_name])


def main(argv):
    global interface
    global file_name
    parser = argparse.ArgumentParser(description='Available options:')

    parser.add_argument('-i', '--interface', type=str,
                        help='Name of the interface')

    parser.add_argument('-f', '--file', type=str,
                        help='File name')

    args = parser.parse_args()

    interface = args.interface

    if not interface:
        parser.print_help()

    file_name = args.file + '.ta' if args.file else get_file_name('ta')
    # if args.file:
    #     file_name = args.file + '.ta'
    # else:
    #     file_name = get_file_name('ta')

    print('Interface is ', interface)
    print('File name is ', file_name)

    start_packet_sniffing()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        capture_file()
        sys.exit(1)
