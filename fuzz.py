import driller
import fuzzer

import config


class Fuzz:
    def __init__(self, binary, time_limit):
        self.binary = binary
        self.time_limit = time_limit
        self.fuzzer = None

    def start(self):
        print "[*] Enable driller..."
        self.drill_extension = driller.LocalCallback(num_workers=config.DRILLER_WORKERS)
        print "[*] Initialize fuzzer..."
        self.fuzzer = fuzzer.Fuzzer(
            self.binary, config.FUZZ_DIR, afl_count=config.FUZZER_WORKERS, force_interval=config.FUZZER_FORCE_INTERVAL,
            create_dictionary=True, stuck_callback=self.drill_extension, time_limit=self.time_limit
        )
        print "[*] Starting fuzzer..."
        self.fuzzer.start()

    def kill(self):
        self.fuzzer.kill()
        self.drill_extension.kill()

    def found_crash(self):
        if not self.fuzzer:
            return False
        return self.fuzzer.found_crash()