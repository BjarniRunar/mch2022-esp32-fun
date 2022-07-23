import gc

from upagekite.httpd import async_url
from upagekite.proto import asyncio, fuzzy_sleep_ms
from upagekite.websocket import websocket, ws_broadcast, OPCODES


##[ Helper routines! ]#########################################################

LOG_BUFFER = []
def _log_handler(msg):
    global LOG_BUFFER
    while len(LOG_BUFFER) > 200:
        LOG_BUFFER = LOG_BUFFER[1:]
    LOG_BUFFER.append(msg.strip())
    print(msg)


async def flush_log_to_websocket():
    global LOG_BUFFER
    while await fuzzy_sleep_ms(991):
        lines, LOG_BUFFER = LOG_BUFFER , []  # Swap in an empty buffer
        if lines:
            await ws_broadcast('mytest', '\n'.join(lines))
        del lines
        gc.collect()


##[ Web end-points ]##########################################################

@async_url('/websocket/')
@websocket('mytest')
async def web_websocket(opcode, msg, conn, wsock,
        websocket=True,
        first=False,
        eof=False):
    if websocket:
        if first:
            await conn.send('Welcome to the Websocket test!')
            await wsock.broadcast('%s has joined us, from %s'
                % (conn.uid, conn.remote_ip))
        if msg and (opcode == OPCODES.TEXT):
            await wsock.broadcast('%s said: %s' % (conn.uid, msg))
        elif eof:
            await wsock.broadcast('%s has left...' % conn.remote_ip)

    else:
        # This is the fallback non-websocket behaviour.
        return {
            'mimetype': 'text/html; charset="utf-8"',
            'body': """\
<html><head>
  <title>Websocket Test</title>
  <script type="text/javascript">
    var host = document.location.host;
    var wsp = (document.location.protocol == 'http:') ? 'ws' : 'wss';
    var counter = 0;
    const socket = new WebSocket(wsp + '://' + host + '/websocket/');
    socket.onopen = function () {
      setInterval(function() {
        socket.send('I am alive');
      }, 10000);
    };
    socket.onmessage = function(event) {
      var container = document.getElementById('log');
      container.innerHTML += '\\n'+event.data;
      if (event.data.indexOf('Captured new image') != -1) {
        document.getElementById('pic').innerHTML = '<img class="right" src="/cam.jpg?c='+counter+'">';
        counter += 1;
      }
    };
    setInterval(function() {
      document.getElementById('log').innerHTML = 'Cleared';
    }, 10 * 6000);
  </script>
</head><body>
  <h1>Websocket Test</h1>
  <h3>Logged</h3>
  <pre id=log>%s</pre>
</body></html>
""" % '\n'.join(LOG_BUFFER)}


def setup_websocket(global_app_env):
    global_app_env['uPK'].info = _log_handler
    global_app_env['uPK'].error = _log_handler

    asyncio.get_event_loop().create_task(flush_log_to_websocket())
