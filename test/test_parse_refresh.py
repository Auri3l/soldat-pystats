import io
import base64
from piestats.status import Status

# A response from soldat server. Info on this here: http://wiki.soldat.pl/index.php/Refresh
response = base64.b64decode('''BkNCZWJlZQAAAAAAAAAAAAAAAAAAAAAAAAtaYW15aHJ1c2hrYQAAAAAAAAAAAAAAAAAKU2xhdlsxMTA5XQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD//////////////////////////////////////xAACAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANABAACgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAdDIyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAgEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKw4HDKASBe6Tgru6QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHY3RmX0FzaAAAAAAAAAAAAKDxBABKwgQAHgAE''')  # noqa


# Just need a class that stores a bytestream internally and has a
# recv method which gets bytes out of that and increases position
class FakeSocket():
  def __init__(self, data):
    self.fake_sock = io.BytesIO(data)

  def recv(self, n):
    return self.fake_sock.read(n)


def test_parse():

  # It doesn't actually connect unless you run get_info which we're not
  parser = Status('127.0.0.1', 23073, None)

  # Simple class that has a recv method to satisfy the parser function
  fake_socket = FakeSocket(response)

  r = parser.parse_refresh(fake_socket)

  # Regurgitate these back
  assert r['ip'] == '127.0.0.1'
  assert r['port'] == 23073

  # Parsed out of the decode base64 packet
  assert r['map'] == 'ctf_Ash'
  assert r['mode'] == 4

  # Trivial player name parsing
  names = ['CBebee', 'Zamyhrushka', 'Slav[1109]']
  for i, name in enumerate(names):
    assert r['players'][i]['name'] == name
