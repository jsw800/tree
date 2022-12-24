import argparse
from . import available_effects

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true', help='Run in test mode (using point cloud viewer, requires pptk)')
    # parser.add_argument('-r', '--remote', action='store_true', help='Run on remote tree')
    # parser.add_argument('--url', help='The hostname/IP and port of the remote tree server')
    parser.add_argument('coords_file', help='Path to a csv containing coords of the output tree')
    parser.add_argument('effect', help='Name of the effect to run, (one of ' + ', '.join(available_effects()) + ')')
    return parser.parse_args()
