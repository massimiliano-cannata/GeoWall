

import webview
import threading
import time
import websocket
import time
import json
import sys
import msg
#sys.path.append('/home/maxi/GIT/geostation/')



__screen_name__ = None
__screen_size__ = None
__screen_position__ = [1, 1]


class Screens():
    """screen tracking list"""
    def __init__(self):
        self.screens = {}

    def add_screen(self, name, size, position, last_position):
        self.screen[name] = {
            'size': size,
            'position': position,
            'last_position': None
        }


class Api():
    """Class to register to JScript events append
    rise Python reaction"""
    def __init__(self, ws):
        self.ws = ws

    def shown(self, params):
        self.ws.send(msg.create_shown_pkg(__screen_name__))


def on_message(ws, message):
    """ The screen react to MOVE and SHOW messages only"""
    try:
        pkg = json.loads(message)
    except Exception:
        return ws.send(
            msg.create_error_pkg(u'Format error'))
    if pkg['TYPE'] == msg.MOVE:
        # MOVE THE screen
        pass
    if pkg['TYPE'] == msg.SHOW:
        time.sleep(pkg['delay_s'])
        webview.load_url(pkg['url'])
        webview.evaluate_js(
        """
        if (window.hasOwnProperty('Reveal')) {
            Reveal.addEventListener( 'slidechanged', function( event ) {
                if(Reveal.isLastSlide()){
                    pywebview.api.shown()
                }
            } )
        };
        """
        )
    # else:
    #     print(
    #         msg.create_error_pkg(u'Unknown TYPE'))
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    pkg = msg.create_join_pkg(__screen_name__,
                              __screen_size__,
                              __screen_position__)
    print(pkg)
    ws.send(pkg)


def create_app():
    pass
    # webview.load_html(__url__)
    # webview.evaluate_js("""
    # Reveal.addEventListener( 'slidechanged', function( event ) {
    #     if(Reveal.isLastSlide()){
    #         pywebview.api.shown()
    #     }
    # } );
    # """)


def main(args):
    global __screen_name__, __screen_size__, __screen_position__
    __screen_name__ = str(args[1])
    __screen_size__ = [int(x) for x in args[2].split('x')]
    __screen_position__ = [int(x) for x in args[3].split(':')]

    # start the websocket in a thread
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        'ws://localhost:8080/GeoWallWebSocket',
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)

    #ws.on_open = on_open
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst._runninng = True
    wst.start()

    print("ws init...")
    if ws.sock.connected:
        ws.send(msg.create_join_pkg())
    print("ws created...")

    # initialize Api object with websocket
    api = Api(ws)

    # run the webview in a thread
    # t = threading.Thread(target=create_app)
    t = threading.Thread()
    t.start()
    webview.create_window(__screen_name__, js_api=api)

    # Create a non-resizable webview window with 800x600 dimensions
    # webview.create_window("screen %s" % __screen_name__,
    #                       "http://www.google.com",
    #                       width=800, height=600,
    #                       resizable=True,
    #                       js_api=api)

    """print("loading webview...")
    webview.load_html("created ws...")
    time.sleep(5)

    if ws.sock.connected:
        ws.send(create_view_pkg())

    webview.toggle_fullscreen()
    time.sleep(5)"""


if __name__ == '__main__':
    main(sys.argv)
