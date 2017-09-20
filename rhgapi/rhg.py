import time
import requests
from requests.auth import HTTPBasicAuth
from rhgmodel import *


class RHGClient:
    def __init__(self, username, password):
        self.http_auth = HTTPBasicAuth(username, password)
        self.sess = requests.session()
        self.sess.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"})
        self.statusTime = 0
        self.submitTime = 0

    def get_question_status(self):
        if time.time() - self.statusTime < 11:
            raise RHGException("api access too frequently")
        r = self.sess.get(const.RHG_STATUS_API, auth=self.http_auth)
        self.statusTime = time.time()
        if r.status_code != 200:
            raise RHGException(r.text)
        try:
            qs = QuestionStatus()
            j = r.json()
            if j.has_key("status"):
                raise RHGException(j["msg"])
            qs.from_dict(j)
            return qs
        except ValueError:
            raise RHGException(r.text)

    def submit_payload(self, payloadInfo):
        if not isinstance(payloadInfo, PayloadInfo):
            raise ValueError("Mistype of payloadInfo should be PayloadInfo")
        if time.time() - self.submitTime < 11:
            raise RHGException("api access too frequently")
        r = self.sess.post(const.RHG_SUBMIT_API, auth=self.http_auth, json=payloadInfo.to_map())
        self.submitTime = time.time()
        if r.status_code != 200:
            raise RHGException(r.text)

        try:
            j = r.json()
            if j["status"] is 1:
                return True
            return False
        except Exception:
            raise RHGException(r.text)
