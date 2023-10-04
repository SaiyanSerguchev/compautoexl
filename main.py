import psutil
import platform
import GPUtil
import xlsxwriter

workbook = xlsxwriter.Workbook("Audit.xlsx")
worksheet = workbook.add_worksheet()
worksheet.set_column("A:A", 30)

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
worksheet.write("A1", f"Node Name: {uname.node}")
worksheet.write("A2", f"Processor: {uname.machine}")
gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    worksheet.write("A3", f"GPU: {gpu.name}")

svmem = psutil.virtual_memory()
worksheet.write("A4", f"Memory: {get_size(svmem.total)}")

print()
worksheet.write("A5", f"Physical cores:{psutil.cpu_count(logical=False)}")
print()
worksheet.write("A6", f"Total cores:{psutil.cpu_count(logical=True)}")

partitions = psutil.disk_partitions()
for partition in partitions:
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    worksheet.write("A7",f"  Total Size of disk: {get_size(partition_usage.total)}")
    worksheet.write("A8",f"  Used: {get_size(partition_usage.used)}")

workbook.close()