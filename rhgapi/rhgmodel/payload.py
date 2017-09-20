import base64

class Payload:
    def __init__(self):
        self.Crash = ""
        self.Eip = ""
        self.Memwrite = ""
        self.Memread = ""
        self.defense = ""

    def set_crash(self, binary):
        self.Crash = base64.encodestring(binary)

    def set_eip(self, binary):
        self.Eip = base64.encodestring(binary)

    def set_mem_write(self, binary):
        self.Memwrite = base64.encodestring(binary)

    def set_mem_read(self, binary):
        self.Memread = base64.encodestring(binary)

    def set_defense(self, binary):
        self.defense = base64.encodestring(binary)

    def to_map(self):
        ret = []
        for i in dir(self):
            if not i.startswith("_"):
                inst = getattr(self, i)
                if isinstance(inst, str):
                    ret.append({i:inst})
        return ret


class PayloadInfo:
    def __init__(self):
        self.Payloads = {}

    def add_payload(self, challengeId, payload):
        if not isinstance(payload, Payload):
            raise ValueError("Mistype of payload, should be Payload.")
        self.Payloads[challengeId] = payload

    def del_payload(self, challengeId):
        del self.Payloads[id]

    def to_map(self):
        ret = []
        for k in self.Payloads:
            ret.append({
                "ChallengeID": k,
                "Payload": self.Payloads[k].to_map()
            })
        return {
            "payloadInfo": ret
        }