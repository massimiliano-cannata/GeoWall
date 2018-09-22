from tinydb import TinyDB, Query
from jinja2 import Environment, FileSystemLoader
import os
import json
from io import IOBase

import config as cf
import traceback

class project(object):
    """Generic object for handling project data."""
    def __init__(self, initial_data=None):
        if initial_data:
            try:
                self._data = json.loads(initial_data)
            except json.JSONDecodeError as e:
                with open(initial_data) as f:
                    self._data = json.load(f)
            except Exception as e:
                traceback.print_exc()
                raise ValueError('initial_data: wrong parameter type')
        else:
                self._data = None
        self.db = cf.TINY_DB

    def __load__(self, projname):
        q = Query()
        res = self.db.search(pr.title == projname)[0]
        if len(res) == 1:
            self._data = res[0]
        elif len(res) == 0:
            print("Project %s not found" % projname)
        else:
            print("multiple project found: error !!!")

    def __save__(self):
        db.upsert(self._data, title == self._data["title"])

    def create_reveal_info_slides(self, theme, column, delay_s=0):
        self._j2env = Environment(
            loader=FileSystemLoader(cf.REVEAL_TEMPL_DIR),
            trim_blocks=True)

        fname = cf.REVEAL_HTML_DIR + "%s_info.html" % self._data["title"]
        furl = cf.REVEAL_URL + "%s_info.html" % self._data["title"]
        # create info.html
        with open(fname, 'w') as f:
            html = self._j2env.get_template(cf.PROJECT_INFO_TEMPL).render(
                reveal_url=cf.REVEAL_URL,
                theme=self._data["slide_theme"],
                title=self._data["title"],
                main_goal=self._data["main_goal"]
            )
            f.write(html)

        # create impact.html
        fname = cf.REVEAL_HTML_DIR + self._data["title"] \
            + "_" + cf.PROJECT_INFO_TEMPL
        furl = cf.REVEAL_URL + self._data["title"] \
            + "_" + cf.PROJECT_INFO_TEMPL
        with open(fname, 'w') as f:
            html = self._j2env.get_template(cf.PROJECT_IMPACT_TEMPL).render(
                theme=self._data["theme"],
                impact=self._data["impact"],
                main_goal=self._data["main_goal"]
            )
            f.write(html)

        # update project json
        if "row_info_slides" in self._data:
            # prepare info slides
            found = False
            # aggiorna la configurazione info
            for x in self._data["row_info_slides"]:
                if x["column"] == column:
                    x["delay_s"] = delay_s
                    x["url"] = furl
                    found = True
            if not found:
                self._data["info_slides"].append({
                    "screen": screen,
                    "delay_s": delay_s,
                    "viewDistance": 3,
                    "url": furl})
