from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

result = get_file_content("calculator", "main.py")
print(f"main.py length: {len(result)}")
print(f"main.py truncated: {'truncated' in result}")
print(result)

result = get_file_content("calculator", "pkg/calculator.py")
print(f"calculator.py length: {len(result)}")
print(f"calculator.py truncated: {'truncated' in result}")
print(result)

result = get_file_content("calculator", "/bin/cat")
print(f"cat length: {len(result)}")
print(f"cat truncated: {'truncated' in result}")
print(result)

result = get_file_content("calculator", "pkg/does_not_exist.py")
print(f"does_not_exist.py length: {len(result)}")
print(f"does_not_exist.py: {'truncated' in result}")
print(result)