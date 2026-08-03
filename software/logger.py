"""Serial logger for the bow-grip biofeedback wearable.

Reads the CSV stream from the ESP32, validates every row, and writes one
CSV per session. Reports a live corruption rate so data quality is known
at collection time rather than discovered later.

    pip install pyserial

    python3 logger.py S1_A1_s01.csv              # motor off  (A phases)
    python3 logger.py S1_B1_s01.csv --mode F     # motor on   (B phases)
"""
import serial, csv, time, argparse

ap = argparse.ArgumentParser()
ap.add_argument('file', help='output CSV filename')
ap.add_argument('--port', default='/dev/cu.usbserial-0001')
ap.add_argument('--mode', default='R', choices=['R', 'F'],
                help='R = record (motor off), F = feedback (motor on)')
a = ap.parse_args()

ser = serial.Serial(a.port, 115200, timeout=2)
time.sleep(1)
ser.write(a.mode.encode())
print('Mode:', a.mode, '| Logging to', a.file, '- press Ctrl+C to stop')


def valid(p):
    """Reject anything that is not a complete, correctly typed row."""
    if len(p) != 11:
        return False
    try:
        for x in p[:4]:
            int(x)
        for x in p[4:10]:
            float(x)
    except ValueError:
        return False
    return p[10] in ('R', 'F')


with open(a.file, 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['wallclock_iso', 't_ms', 'fsr1', 'fsr2', 'emg',
                'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mode'])
    kept = rejected = 0
    try:
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if not line or line.startswith('#'):
                continue
            p = line.split(',')
            if valid(p):
                w.writerow([time.strftime('%Y-%m-%dT%H:%M:%S'), *p])
                kept += 1
                if kept % 500 == 0:
                    print(f'{kept} clean  |  {100*rejected/(kept+rejected):.1f}% rejected')
            else:
                rejected += 1
    except KeyboardInterrupt:
        total = kept + rejected
        pct = 100 * rejected / total if total else 0
        print(f'Stopped. {kept} clean rows, {rejected} rejected ({pct:.1f}%) -> {a.file}')
