
import json
# import screen_conf
# Different message types
MESSAGE = 0
ERROR = 1
JOIN = 2
MOVE = 3
MOVED = 4
SHOW = 5
SHOWN = 6
ACTION = 7
LEAVE = 8
SLIST = 9
SHOWCFG = 10
MOVECFG = 11

ACTIONS = {
    'SDG': ['CLIMATE', 'WATER', 'FOOD'],
    'IDLE': ['RAND'],
    'PROJECT': []
}


def create_message_pkg(screen, type, msg):
    """create a generic message"""
    pkgdata = {
        'screen': screen,
        'TYPE': MESSAGE,
        'msg_type': type,
        'msg': msg}
    return json.dumps(pkgdata)


def create_error_pkg(screen, type, msg):
    """report an error"""
    pkgdata = {
        'screen': screen,
        'TYPE': ERROR,
        'err_type': type,
        'msg': msg}
    return json.dumps(pkgdata)


def create_join_pkg(screen, size, position, master=False):
    """used by a screen to register to the websocket"""
    if not len(position) == 2 and len(size) == 2:
        create_error_pkg(
            screen=screen,
            type='VALUE_ERROR',
            msg='size and position arguments must be of len=2')
    else:
        pkgdata = {
            'TYPE': JOIN,
            'screen': screen,
            'size': size,
            'position': position,
            'master': False}
        return json.dumps(pkgdata)


def create_move_pkg(z, screen, delay_m=0):
    """message to indicate a new screen position"""
    pkgdata = {'TYPE': MOVE, 'z': z,
               'screen': screen, 'delay_m': delay_m}
    return json.dumps(pkgdata)


def create_move_conf_pkg(conf):
    """message to indicate a new screen position"""
    pkgdata = {'TYPE': MOVECFG, 'conf': conf}
    return json.dumps(pkgdata)


def create_moved_pkg(screen):
    """message to notify one resource has been shown"""
    pkgdata = {'TYPE': MOVED, 'screen': screen}
    return json.dumps(pkgdata)


def create_show_pkg(url, screen, delay_s=0):
    """message to ask to display a Web resource"""
    pkgdata = {'TYPE': SHOW, 'url': url,
               'screen': screen, 'delay_s': delay_s}
    return json.dumps(pkgdata)


def create_show_conf_pkg(conf):
    """message to ask to display a Web resource"""
    pkgdata = {'TYPE': SHOWCFG, 'conf': conf}
    return json.dumps(pkgdata)


def create_shown_pkg(screen):
    """message to notify one resource has been shown"""
    pkgdata = {'TYPE': SHOWN, 'screen': screen}
    return json.dumps(pkgdata)


def create_action_pkg(action):
    """message to ask for execution of an action"""
    a = action.split(':')
    pkgdata = {'TYPE': ACTION, 'action': a}
    return json.dumps(pkgdata)


def create_leave_pkg(screen):
    """leave the websocket channel"""
    pkgdata = {'TYPE': LEAVE, 'name': screen}
    return json.dumps(pkgdata)


def create_slist_pkg(screens):
    """message to dispatch the registered screens"""
    pkgdata = {'TYPE': SLIST, 'screens': screens}
    return json.dumps(pkgdata)
