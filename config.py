from multiprocessing import cpu_count

DOWNLOAD_DIR = "/opt/work"
FUZZ_DIR = "/dev/shm/work"
DRILLER_WORKERS = 1
FUZZER_WORKERS = 1
FUZZER_FORCE_INTERVAL = 300
PROCESS_POOL = cpu_count()
