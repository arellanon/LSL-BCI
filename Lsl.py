import matplotlib.pyplot as plt
from pylsl import resolve_stream, StreamInlet

print('Resolving a Control stream...')
streams = resolve_stream('type', 'EEG')
print('paso1')
inlet = StreamInlet(streams[0])
print('paso2')
while True:
    try:
        sample, timestamp = inlet.pull_sample()
        print(sample)
    except Exception as e:
        print(e)
