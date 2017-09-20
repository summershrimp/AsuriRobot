import os
import rhgapi
from threading import Timer
from multiprocessing import Pool
import config
import fuzz

challenges = {}
last_round = 0
pool = None


def resolv_work():
    questions = client.get_question_status()
    for challenge in questions.CurrentChallenge:
        if not challenges.has_key(challenge.ChallengeID):
            print "[*] Add Challenge %s, type %s." % (challenge.ChallengeID, ",".join(challenge.ChallengeType))
            challenges[challenge.ChallengeID] = {"challenge":challenge}
            binary_name = os.path.join(config.DOWNLOAD_DIR, str(challenge.ChallengeID))
            challenge.download(os.path.abspath(binary_name))
            fuzzer = fuzz.Fuzz(binary=binary_name, time_limit=1200)
            challenges[challenge.ChallengeID]["fuzzer"] = fuzzer
            pool.apply_async(run_fuzzer, (fuzzer,))


def check_crash():
    for challengeId in challenges:
        fuzzer = challenges[challengeId]["fuzzer"]
        if fuzzer.found_crash() :
            pass


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
        resolver = Timer(60, resolv_work())
        resolver.start()
        crasher = Timer(60, check_crash())
        crasher.start()
    except KeyboardInterrupt:
        pool.close()
        pool.join()



