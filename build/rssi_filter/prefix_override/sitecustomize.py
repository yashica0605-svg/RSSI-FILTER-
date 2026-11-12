import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yashi-05/rssi_ws/rssi_filter/install/rssi_filter'
