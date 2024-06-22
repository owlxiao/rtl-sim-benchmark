import subprocess


def kernel_version():
    version = subprocess.run(
        ['uname', '-r'], stdout=subprocess.PIPE, text=True).stdout.strip()
    return f"Arch Linux (Kernel {version})"


def gcc_version():
    output = subprocess.run(['gcc', '--version'],
                            stdout=subprocess.PIPE, text=True).stdout
    version = next((line for line in output.split() if '.' in line), 'unknown')
    return f"gcc {version}"


def llvm_version():
    output = subprocess.run(['clang', '--version'],
                            stdout=subprocess.PIPE, text=True).stdout
    version = next((line for line in output.split() if '.' in line), 'unknown')
    return f"Clang {version}"


def verilator_version():
    output = subprocess.run(['verilator', '--version'],
                            stdout=subprocess.PIPE, text=True).stdout
    version = output.split()[1]
    return f"Verilator {version}"


def firtool_version():
    output = subprocess.run(['firtool', '--version'],
                            stdout=subprocess.PIPE, text=True).stdout
    version = output.split()[1]
    return f"Firtool {version}"


print("field, value")
print(f"OS,{kernel_version()}")
print(f"Compiler,{gcc_version()} {llvm_version()}")
print(f"Verilator,{verilator_version()}")
print(f"Firtool,{firtool_version()}")
