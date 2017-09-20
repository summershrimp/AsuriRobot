import requests
import os


class Challenge:
    def __init__(self):
        self.ChallengeID = 0
        self.ChallengeType = []
        self.Difficulty = 1
        self.EIP = ""
        self.MemoryReadPath = ""
        self.MemoryWritePath = ""
        self.MemoryWriteContent = ""
        self.BinaryUrl = ""

    def download(self, dest):
        r = requests.get(self.BinaryUrl, stream=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"})
        p = os.path.realpath(dest)
        with open(p, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 512):
                if chunk:
                    f.write(chunk)
        f.close()
        os.chmod(p, 0755)
        return p

    def from_dict(self, m):
        for k in m:
            if k == "ChallengeType":
                self.ChallengeType.extend(m[k].split(","))
                continue
            if hasattr(self, k):
                setattr(self, k, m[k])


class Detail:
    def __init__(self):
        self.pwned_times = 0
        self.defensed_times = 0
        self.score = 0

    def from_list(self, l):
        if len(l) != 3:
            raise ValueError("Len of list l should be 3.")
        self.pwned_times = l[0]
        self.pwned_times = l[1]
        self.pwned_times = l[2]


class DefenceDetail:
    def __init__(self):
        self.Crash = Detail()
        self.EIP = Detail()
        self.MemoryRead = Detail()
        self.MemoryWrite = Detail()

    def from_dict(self, m):
        if not isinstance(m, dict):
            raise ValueError("Mistype of m, should be dict. ")
        for k in m:
            if hasattr(self, k):
                getattr(self, k).from_list(m[k])


class LastDetail:
    def __init__(self):
        self.ChallengeID = 0
        self.AtkScore = 0
        self.DefScore = 0
        self.CheckScore = 0
        self.DefDetail = DefenceDetail()

    def from_dict(self, m):
        if not isinstance(m, dict):
            raise ValueError("Mistype of m, should be dict. ")
        for k in m:
            if k == "DefDetail":
                self.DefDetail.from_dict(m[k])
                continue
            if hasattr(self, k):
                setattr(self, k, m[k])


class PointsInfo:
    def __init__(self):
        self.total_score = 0
        self.score_earn = 0
        self.score_lost = 0

    def from_dict(self, m):
        self.total_score = m["Points"]
        self.score_earn = m["Score"]
        self.score_lost = m["Deduction"]


class QuestionStatus:
    def __init__(self):
        self.CurrentRound = 0
        self.CurrentChallenge = []
        self.LastDetail = []
        self.FlowPacket = ""
        self.PointsInfo = PointsInfo()

    def from_dict(self, m):
        self.CurrentRound = m["CurrentRound"]
        self.FlowPacket = m["FlowPacket"]
        for i in m["CurrentChallenge"]:
            cc = Challenge()
            cc.from_dict(i)
            self.CurrentChallenge.append(cc)
        for i in m["LastDetail"]:
            ld = LastDetail()
            ld.from_dict(i)
            self.LastDetail.append(ld)
        self.PointsInfo.from_dict(m["PointsInfo"][0])
