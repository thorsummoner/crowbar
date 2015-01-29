"""docstring for Profiler"""

from gi.repository import Gtk
import signal

from profile_selector import ProfileSelector
import loader

from pprint import pprint

class Profiler(Gtk.Window):
    """docstring for Profiler"""

    profiles = list()
    profiles_store_class = Gtk.ListStore
    profiles_store = None

    def __init__(self):
        super(Profiler, self).__init__()

        self.set_title="Configuration Profiles"

        self.set_default_size(240, 80)

        self.profiles = Profiler.reload_profiles()

        self._gui_main()
        self._bind_events()


    def _bind_events(self):
        """Bind all """
        self.connect("delete-event", Gtk.main_quit)

    def _gui_main(self):
        box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        box.pack_start(ProfileSelector(self.profiles), False, False, 0)

    def main(self):
        """docstring for Main"""
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.show_all()
        Gtk.main()

    @staticmethod
    def reload_profiles():
        """Read and parse all config files.
        Returns:
            list: of dicts, the parsed configs named by...
        """
        raw_configs = loader.read_configs()

        config = {
            'byName': dict(),
            'byFileName': dict(),
            'byFilePath': dict(),
        }

        for raw_config in raw_configs:
            body_lines = raw_config['body'].splitlines()
            proper_name = body_lines.pop(0).lstrip('# ').rstrip()
            config_lines = {
                'ListStore': Gtk.ListStore(bool, str, str),
                'list_raw': [],
                'raw': raw_config['body'],
                'name': proper_name,
                'file_name': raw_config['name'],
                'file_path': raw_config['path'],
            }
            config['byName'][proper_name] = config_lines
            config['byFileName'][raw_config['name']] = config_lines
            config['byFilePath'][raw_config['path']] = config_lines
            for line in body_lines:
                # bool, str, str
                raw_values = [
                    not line.startswith('#'),
                    line.lstrip('# '),
                    line
                ]
                config_lines['list_raw'].append(raw_values)
                config_lines['ListStore'].append(raw_values)

        return config
            # body_store = Gtk.ListStore(bool, str, str)
            #     body_store.append(
            #         [not line.startswith('#'), line.lstrip('# '), line]
            #     )

            # return [name, proper_name, body_store, body]
            # config_store = self.new_config_store(body=body)
            # if name == PROFILE_DEFAULT:
            #     self.configs_store.prepend(config_store)
            #     self.profile.set_active(0)
            # else:
            #     self.configs_store.append(config_store)

