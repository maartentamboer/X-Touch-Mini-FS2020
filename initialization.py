from globalstorage import GlobalStorage


class Initialization:
    def __init__(self, json_data):
        self._global_storage = GlobalStorage()
        if json_data:
            self._global_variables(json_data.get('global_variables', None))

    def _global_variables(self, json_data):
        if not json_data:
            return

        for elem in json_data:
            self._global_storage.set_global_variable(elem['name'], elem['value'])
