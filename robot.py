import os
import rhgapi
from threading import Timer
from multiprocessing.dummy import Pool
import config
import fuzz
import random
import logging
import time

challenges = {}
crashes_dict = {}
last_round = 0
pool = None


def resolv_work():
    questions = client.get_question_status()
    for challenge in questions.CurrentChallenge:
        if not challenges.has_key(challenge.ChallengeID):
            print("[*] Add Challenge %s, type %s." % (challenge.ChallengeID, ",".join(challenge.ChallengeType)))
            challenges[challenge.ChallengeID] = {"challenge":challenge}
            binary_name = os.path.join(config.DOWNLOAD_DIR, str(challenge.ChallengeID))
            challenge.download(os.path.abspath(binary_name))
            fuzzer = fuzz.Fuzz(binary=binary_name, time_limit=1200)
            challenges[challenge.ChallengeID]["fuzzer"] = fuzzer
            pool.apply_async(run_fuzzer, (fuzzer,))
        else:
            print("[*] Challenge exists: %s" % challenge.ChallengeID)
    Timer(60.0, resolv_work).start()

def check_crash():
    for id in challenges:
        fuzzer = challenges[id]["fuzzer"]
        print("[*] Check crash for %s" % id)
        cs = fuzzer.crashes()
        if len(cs) > 0:
            print("[*] Crash for %s found!" % id)
            if not crashes_dict.has_key(id):
                crashes_dict[id] = []
            crashes_dict[id].extend(cs)
    Timer(60.0, check_crash).start()

def submit_payload():
    info = rhgapi.PayloadInfo()
    crash_cnt = 0

    for id in challenges:
        p = rhgapi.Payload()
        if crashes_dict.has_key(id) and len(crashes_dict[id]) != 0:
            crash_cnt += 1
            p.set_crash(random.choice(crashes_dict[id]))
        else:
            pass
        info.add_payload(id, p)

    print("[*] Submit payloads, crash: %d" % crash_cnt)
    client.submit_payload(info)
    Timer(60.0, submit_payload).start()


def run_fuzzer(fuzzer):
    fuzzer.start()

if __name__ == "__main__":
    try:
        try:
            os.makedirs(config.DOWNLOAD_DIR, 0777)
        except OSError:
            pass
        pool = Pool(processes=config.PROCESS_POOL)
        username = os.environ.has_key("RHG_USER") and os.environ["RHG_USER"] or "team_11"
        password = os.environ.has_key("RHG_PASS") and os.environ["RHG_PASS"] or "wz2mrzmc"
        client = rhgapi.RHGClient(username, password)
        resolv_work()
        check_crash()
        submit_payload()
        print "[*] Finish init."
    except KeyboardInterrupt:
        pool.close()
        for challenge_id in challenges:
            challenges[challenge_id]["fuzzer"].stop()
        pool.join()



