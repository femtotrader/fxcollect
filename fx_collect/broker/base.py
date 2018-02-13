from abc import ABCMeta
from datetime import datetime, timedelta
import time

OLE_TIME_ZERO = datetime(1899, 12, 30)


class AbstractBroker(object):
    """
    The BrokerHandler object is designed to interact directly
    with FXCM using the python-forexconnect API.
    """
    
    __metaclass__ = ABCMeta

    def _session_status(self):
        if self._session.is_connected():
            return True
        else:
            return False

    def _login(self, broker, user, passwd, env, url):
        rest = 0
        while True:
            rest+=1
            try:
                self._session = broker(
                    user.encode(), passwd.encode(),
                    env.encode(), url.encode()
                )
                if self._session_status():
                    break
            except RuntimeError as e:
                print(e)
                time.sleep(rest)

    def _logout(self):
        self._session.logout()

    def _to_ole(self, pydate):
        if isinstance(pydate, datetime):
            delta = pydate - OLE_TIME_ZERO
            return float(delta.days) + (float(delta.seconds) / 86400)
        else:
            return pydate

    def _fm_ole(self, oletime):
        if isinstance(oletime, float):
            return OLE_TIME_ZERO + timedelta(days=float(oletime))
        else:
            return oletime