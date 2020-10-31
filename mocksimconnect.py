

class MockEvent:
    def __init__(self, key):
        self._key = key

    def __call__(self, value=0):
        print('MockEvent::__call__', self._key, value)


class MockAircraftEvents:
    @staticmethod
    def find(key):
        return MockEvent(key)


class MockAircraftRequests:
    @staticmethod
    def get(key):
        print('MockAircraftRequests::get', key)
        return 0

    @staticmethod
    def set(key, value):
        print('MockAircraftRequests::set', key, value)
        return True
