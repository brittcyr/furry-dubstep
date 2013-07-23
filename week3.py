import hashlib

blocks = []
with open('video_unknown.mp4', 'rb') as f:
    data = f.read(1024)
    while data:
        blocks.insert(0, data)
        data = f.read(1024)

h = ''
for data in blocks:
    h = hashlib.sha256(data + h).digest()

print h.encode('hex')
