import json
import os
import sys

class ProfileParser(object):
    def __init__(self, path):
        self._profiles = []
        self._capi_dict = {}
        self._work_path = path

    def get_dict(self):
        return self._capi_dict

    def parse_markdown(self):
        os.environ['MXNET_PROFILER_AUTOSTART'] = '1'
        for file in os.listdir(self._work_path):
            if file == "index.md":
                continue
            try:
                file = os.path.join(self._work_path, file)
                os.system('notedown {} --run > /dev/null'.format(file))
            except OSError:
                print("[INFO] Error: ")
            with open('profile.json', 'r') as f:
                profile_res = json.load(f)
            self.parse_num_occurrences(profile_res)
            os.remove('profile.json')

    def parse_num_occurrences(self, data):
        for d in data['traceEvents']:
            if 'cat' not in d:
                continue
            if d['cat'] == 'MXNET_C_API':
                if d['name'] not in self._capi_dict:
                    self._capi_dict[d['name']] = 1
                else:
                    self._capi_dict[d['name']] += 1

    def run(self):
        self.parse_markdown()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    process_folder_path = sys.argv[1]
    process_folder_path_abs = os.path.abspath(process_folder_path)
    pp = ProfileParser(process_folder_path_abs)
    pp.run()
    print(pp.get_dict())
