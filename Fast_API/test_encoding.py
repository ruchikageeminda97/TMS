# test_encoding.py
with open('.env', 'rb') as f:
    content = f.read()
    print(content[:10])