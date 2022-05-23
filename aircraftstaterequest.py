# Part of code adapted from https://github.com/odwdinc/Python-SimConnect licensed under GPLv3
# Original Author: odwdinc
# All rights belong to the original author

from SimConnect import *
from SimConnect.Enum import *
from SimConnect.Constants import *
import time
import ctypes
from ctypes import *
from ctypes.wintypes import *
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
            rtype = _request.definitions[0][1].decode()
            if 'string' in rtype.lower():
                pS = cast(ObjData.szString, c_char_p)
                _request.outData = pS.value
            else:
                _request.outData = cast(
                    ObjData.dwData, POINTER(c_double * len(_request.definitions))
                ).contents[0]
        else:
            LOGGER.warn("Event ID: %d Not Handled." % (dwRequestID))

class SystemStateRequest(object):

    def get(self):
        return self.value

    def set(self, _value):
        self.value = _value

    @property
    def value(self):
        self.DATA_REQUEST_ID = self.sm.new_request_id()
        self.outData = None
        self.sm.Requests[self.DATA_REQUEST_ID.value] = self
        if (self.LastData + self.time) < millis():
            if self.get_sys_state_data(self):
                self.LastData = millis()
            else:
                return None
        return self.outData

    def __init__(self, _deff, _sm, _time=10, _dec=None, _settable=False, _attemps=10):
        self.DATA_DEFINITION_ID = None
        self.definitions = []
        self.description = _dec
        self._name = None
        self.definitions.append(_deff)
        self.outData = None
        self.attemps = _attemps
        self.sm = _sm
        self.time = _time
        self.defined = False
        self.settable = _settable
        self.LastData = 0
        self.LastID = 0

    def request_sys_state_data(self, _Request):
        _Request.outData = None
        rtype = _Request.definitions[0][1].decode()
        if 'string' in rtype.lower():
            pyarr = bytearray(_Request.definitions[0][0])
            dataarray = (ctypes.c_char * len(pyarr))(*pyarr)
        else:
            return

        pStr = cast(
            dataarray, c_char_p
        )
        
        self.sm.dll.RequestSystemState(
            self.sm.hSimConnect,
            _Request.DATA_REQUEST_ID.value,
            pStr
        )
        temp = DWORD(0)
        self.sm.dll.GetLastSentPacketID(self.sm.hSimConnect, temp)
        _Request.LastID = temp.value

    def get_sys_state_data(self, _Request):
        self.request_sys_state_data(_Request)
        attemps = 0
        while _Request.outData is None and attemps < _Request.attemps:
            time.sleep(.01)
            attemps += 1
        if _Request.outData is None:
            return False

        return True

class SystemStateRequestHelper:
    def __init__(self, _sm, _time=10, _attemps=10):
        self.sm = _sm
        self.dic = []
        self.time = _time
        self.attemps = _attemps

    def __getattr__(self, _name):
        if _name in self.list:
            key = self.list.get(_name)
            setable = False
            if key[3] == 'Y':
                setable = True
            ne = SystemStateRequest((key[1], key[2]), self.sm, _dec=key[0], _settable=setable, _time=self.time, _attemps=self.attemps)
            setattr(self, _name, ne)
            return ne
        return None

    def get(self, _name):
        if getattr(self, _name) is None:
            return None
        return getattr(self, _name).value

class SystemRequests():
    def find(self, key):
        if key in self.sysreq.list:
            rqest = getattr(self.sysreq, key)
            return rqest
        return None

    def get(self, key):
        request = self.find(key)
        if request is None:
            return None
        return request.value

    def __init__(self, _sm, _time=10, _attemps=10):
        self.sm = _sm
        self.sysreq = self.__SystemStateRequest(_sm, _time, _attemps)
    
    class __SystemStateRequest(SystemStateRequestHelper):
        list = {
            "AIRCRAFT_LOADED": ["Requests the full path name of the last loaded aircraft flight dynamics file. These files have a .AIR extension.", b'AircraftLoaded', b'String', 'N'],
            "DIALOG_MODE": ["Requests whether the simulation is in Dialog mode or not. ", b'DialogMode', b'String', 'N'],
            "FLIGHT_LOADED": ["Requests the full path name of the last loaded flight. Flight files have the extension .FLT.", b'FlightLoaded', b'String', 'N'],
            "FLIGHT_PLAN": ["Requests the full path name of the active flight plan. An empty string will be returned if there is no active flight plan.", b'FlightPlan', b'String', 'N'],
            "SIM": ["Requests the state of the simulation. If 1 is returned, the user is in control of the aircraft, if 0 is returned, the user is navigating the UI.", b'Sim', b'String', 'N']
        }
