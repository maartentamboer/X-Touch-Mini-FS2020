from SimConnect import *
from SimConnect.Enum import *
from SimConnect.Constants import *
import time
from ctypes import *
from ctypes.wintypes import *

from nbformat import current_nbformat
from MSFSPythonSimConnectMobiFlightExtension.src.simconnect_mobiflight import SimConnectMobiFlight

class CustomSimconnect(SimConnectMobiFlight):
    def __init__(self):
        super().__init__()

        # Workaround for Simconnect 0.4.24
        self.dll.RequestSystemState.argtypes = [
            HANDLE,
            SIMCONNECT_DATA_REQUEST_ID,
            c_char_p
        ]
    
    def handle_state_event(self, ObjData):
        dwRequestID = ObjData.dwRequestID
        if dwRequestID in self.Requests:
            _request = self.Requests[dwRequestID]
            _request.outData = cast(ObjData.szString, c_char_p).value
        else:
            LOGGER.warn("Event ID: %d Not Handled." % (dwRequestID))

class SystemStateRequest(object):
    def __init__(self, sm, attempts=10):
        self._sm = sm
        self._attempts = attempts
        self._request_id = 0

        # Make it compatible with original Simconnect dispatcher
        self.outData = None
        self.LastID = 0

    def _request_system_state(self, szState):
        p_szState = c_char_p(szState.encode())
        self._request_id = self._sm.new_request_id().value
        self._sm.Requests[self._request_id] = self
        self._sm.dll.RequestSystemState(self._sm.hSimConnect, self._request_id, p_szState)
        last_id_tmp = DWORD(0)
        self._sm.dll.GetLastSentPacketID(self._sm.hSimConnect, last_id_tmp)
        self.LastID = last_id_tmp.value

    def get_system_state(self, szState):
        current_attempt = 0
        self._request_system_state(szState)
        while current_attempt < self._attempts and self.outData is None:
            time.sleep(0.1)
            self._attempts += 1
        return self.outData
