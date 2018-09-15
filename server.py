import json
import os
import time

import tornado.ioloop
import tornado.web
import tornado.websocket
import sys

loc = os.path.dirname(os.path.abspath(__file__))
sys.path.append(loc)
import msg
import config as cf

CONNECTED_SCREENS = []
scstatus = {}
# global MOVING, SHOWING
# MOVING  = False
# SHOWING = False


class GeoWallWebSocket(tornado.websocket.WebSocketHandler):
    """ The GeoWall implemententation: all data send to server is json,
     all responses are json """

    def check_origin(self, origin):

        return True

    def open(self):
        print("open")
        CONNECTED_SCREENS.append(self)
        scstatus['MOVING'] = False
        scstatus['SHOWING'] = False
        self.screen = ''
        self.size = [None, None]
        self.position = [None, None]
        self.last_position = None
        self.join_completed = False
        self.showing = False
        self.moving = False

    def on_message(self, message):
        try:
            pkg = json.loads(message)
            print(pkg)
        except Exception:
            pkg = msg.create_error_pkg(
                type='MSG ERROR',
                msg='cannot decode message')
            return self.write_message(pkg)
        # process messages
        # ----------------------------------------------------------
        if pkg['TYPE'] == msg.JOIN:
            print("JOIN")
            already_registered = False
            for s in CONNECTED_SCREENS:
                if s.screen == pkg['screen'] or s.position == pkg['position']:
                    already_registered = True
                    l = [y.screen for y in CONNECTED_SCREENS]
                    print('ALREADY REGISTERED!')
                    self.write_message(
                        msg.create_error_pkg(self.screen, msg.JOIN,
                                             'screen already connected %s' % l))
                    CONNECTED_SCREENS.remove(self)
            if not already_registered:
                self.screen = pkg['screen']
                self.size = pkg['size']
                self.position = pkg['position']
                # self.last_position = pkg['last_position']
                self.join_completed = True
            print(msg.create_slist_pkg(
                [s.screen for s in CONNECTED_SCREENS]))
        # ----------------------------------------------------------
        elif pkg['TYPE'] == msg.MESSAGE:
            print('message: ' + pkg['msg_type'] + ':' + pkg['msg'])
        # ----------------------------------------------------------
        elif pkg['TYPE'] == msg.MOVECFG:
            if scstatus['MOVING'] is False:
                print("SHOW CONFIG")
                scstatus['MOVING'] = True
                for s in pkg['conf']:
                    self.broadcastM(msg.create_move_pkg(
                                    s['z'],
                                    s['screen'],
                                    s['delay_m']
                                    ), s['screen'])
            else:
                time.sleep(1)  # Delay for 1 second
                print('previous show still running')
        # ----------------------------------------------------------
        elif pkg['TYPE'] == msg.MOVED:
            print('screen ' + pkg['screen'] + ' reacheed end moving')
            for c in CONNECTED_SCREENS:
                if c.screen == pkg['screen']:
                    c.moving = False
                    break
            for c in CONNECTED_SCREENS:
                if c.moving is True and c.screen != '':
                    scstatus['MOVING'] = True
                    print('still showing')
                    break
            else:
                scstatus['MOVING'] = False
                print('no more showing')
        # ----------------------------------------------------------
        elif pkg['TYPE'] == msg.SHOWCFG:
            if scstatus['SHOWING'] is False:
                print("SHOW CONFIG")
                scstatus['SHOWING'] = True
                for s in pkg['conf']:
                    self.broadcastX(msg.create_show_pkg(
                                    s['url'],
                                    s['screen'],
                                    s['delay_s']
                                    ), s['screen'])
            else:
                print('previous show still running')
                # self.write_message(msg.create_error_pkg(
                #     type='SHOW_ERROR',
                #     msg='previous show still running'))
        # ----------------------------------------------------------
        elif pkg['TYPE'] == msg.SHOWN:
            print('screen ' + pkg['screen'] + ' reacheed end slide')
            for c in CONNECTED_SCREENS:
                if c.screen == pkg['screen']:
                    c.showing = False
                    break
            for c in CONNECTED_SCREENS:
                if c.showing is True and c.screen != '':
                    scstatus['SHOWING'] = True
                    print('still showing')
                    break
            else:
                scstatus['SHOWING'] = False
                print('no more showing')
        # ----------------------------------------------------------
        elif pkg['TYPE'] == msg.ACTION:
            if pkg['action'][0].uppercase == 'SDG':
                conf = get_configuration_from_sdg(sdg=pkg['action'][1])
                self.broadcast_configuration(conf)
            elif pkg['action'][0].uppercase == 'PROJECT':
                conf = get_configuration_from_proj(proj=pkg['action'][1])
                self.broadcast_configuration(conf)
            elif pkg['action'][0].uppercase == 'IDLE':
                # TODO should be a loop of configurations to broadcast
                conf = get_configuration_from_idle()
                self.broadcast_configuration(conf)
            else:
                pkg = msg.create_error_pkg(
                    type='MSG ERROR',
                    msg='cannot decode message')
                return self.write_message(pkg)
        # ----------------------------------------------------------
        else:
            pkg = msg.create_error_pkg(
                'S11', 'unknown', 'unknown message type')
            self.write_message(pkg)

    def broadcastX(self, pkg, screen):
        """broadcast showing message to a screen"""
        for c in CONNECTED_SCREENS:
            if c.screen == screen:
                c.showing = True
                c.write_message(pkg)
                break

    def broadcastM(self, pkg, screen):
        """broadcast moving message to a screen"""
        for c in CONNECTED_SCREENS:
            if c.screen == screen:
                c.moving = True
                c.write_message(pkg)
                break

    def broadcastALL(self, pkg):
        """broadcast message to all screens"""
        for c in CONNECTED_SCREENS:
            c.write_message(pkg)

    def on_close(self):
        CONNECTED_SCREENS.remove(self)
        self.broadcastALL(msg.create_leave_pkg(self.screen))


app = tornado.web.Application([
    (r"/GeoWallWebSocket",
        GeoWallWebSocket),
    (r"/src/(.*)",
        tornado.web.StaticFileHandler,
        {"path": cf.REVEAL_HTML_DIR}),
    (r"/revealjs/(.*)",
        tornado.web.StaticFileHandler,
        {"path": cf.REVEAL_PATH}),
], debug=True, autoreload=True, serve_traceback=True)

if __name__ == '__main__':
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
