# using python libraries in the code

def b64enc(blob):
    from base64 import b64encode
    return b64encode(blob)

res = remote_exec(b64enc, [b"abc", b"def"])

assert res == [b'YWJj', b'ZGVm']
