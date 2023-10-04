import psutil
import platform
import GPUtil

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

uname = platform.uname()
print(f"Node Name: {uname.node}")
print(f"Processor: {uname.machine}")
gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    print(f"GPU: {gpu.name}")

svmem = psutil.virtual_memory()
print(f"Memory: {get_size(svmem.total)}")

print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))

partitions = psutil.disk_partitions()
for partition in partitions:
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size of disk: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")

