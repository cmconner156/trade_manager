import argparse

def get_settings():
  parser = argparse.ArgumentParser()

  parser.add_argument('-s', '--settings-file', action='store', required=True,
                    dest='settings_file', default=None, help="Path to settings.yaml")

  args = parser.parse_args()


