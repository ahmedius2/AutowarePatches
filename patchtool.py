import os
import sys
import subprocess
import glob

def gen():
    # Define the file path
    file_path = "./autoware.repos"
    patches_dir = "./AutowarePatches"

    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i > 0 and (i - 1) % 4 == 0:
                path = os.path.join("./src", line.strip()[:-1])
                try:
                    result = subprocess.run(
                        ["git", "diff"],  # Command to run
                        cwd=path,  # Set the target directory
                        capture_output=True,  # Capture stdout and stderr
                        text=True,  # Get output as text instead of bytes
                        check=True  # Raise an exception if the command fails
                    )
                    if len(result.stdout) != 0:
                        #print(f"{path}\n", result.stdout)

                        path_as_fname = path[2:].replace("/", "-") + '.patch'
                        with open(os.path.join(patches_dir, path_as_fname), 'w') as out_file:
                            out_file.write(result.stdout)
                except subprocess.CalledProcessError as e:
                    print(f"Command failed with error: {e.stderr}")


def apply():
    # Define the file path
    os.chdir("./AutowarePatches")
    patch_files_list = glob.glob("*.patch")
    for patch_file in patch_files_list:
        patch_path = os.path.abspath(os.path.join('..', patch_file.replace('-', '/')[:-6]))
        patch_file = os.path.abspath(patch_file)
        result = subprocess.run(
            ["git", "checkout", "."],
            cwd=patch_path,  # Set the target directory
            capture_output=True,  # Capture stdout and stderr
            text=True,  # Get output as text instead of bytes
        )

        result = subprocess.run(
            ["git", "apply", patch_file],
            cwd=patch_path,  # Set the target directory
            capture_output=True,  # Capture stdout and stderr
            text=True,  # Get output as text instead of bytes
        )

def main():
    cmd = sys.argv[1]
    if cmd == 'gen':
        print('Generating patches')
        gen()
    elif cmd == 'apply':
        print('Applying patches')
        apply()
    else:
        print('Unknown command!')

if __name__ == "__main__":
    main()
