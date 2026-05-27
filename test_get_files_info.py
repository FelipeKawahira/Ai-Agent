from functions.get_files_info import get_files_info

print(f"{get_files_info("calculator", ".")}")
print(f"{get_files_info("calculator", "/bin")}")
print(f"{get_files_info("calculator", "../")}")
print(f"{get_files_info("calculator", "main.py")}")