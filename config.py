from multiprocessing import cpu_count
import os

DOWNLOAD_DIR = os.environ.has_key("DOWNLOAD_DIR") and os.environ["DOWNLOAD_DIR"] or "/dev/shm/rhg_bin"
FUZZ_DIR = os.environ.has_key("FUZZ_DIR") and os.environ["FUZZ_DIR"] or "/dev/shm/work"
FUZZER_WORKERS = os.environ.has_key("FUZZER_WORKERS") and int(os.environ["FUZZER_WORKERS"]) or 1
DRILLER_WORKERS = os.environ.has_key("DRILLER_WORKERS") and int(os.environ["DRILLER_WORKERS"]) or 1
FUZZER_FORCE_INTERVAL = os.environ.has_key("FUZZER_FORCE_INTERVAL") and int(os.environ["FUZZER_FORCE_INTERVAL"]) or 300
PROCESS_POOL = os.environ.has_key("PROCESS_POOL") and int(os.environ["PROCESS_POOL"]) or cpu_count()
