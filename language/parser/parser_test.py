import os
base = "C:\\Users\\ofirg\\PycharmProjects\\AICourse\\venv\\Scripts\\python.exe C:\\Users\\ofirg\\PycharmProjects\\AICourse\\language\\parser\\parser.py sentences\\"
for sentence in range(1, 11):
    print(f"Running {str(sentence)}.txt")
    os.system(base + str(sentence) + ".txt")