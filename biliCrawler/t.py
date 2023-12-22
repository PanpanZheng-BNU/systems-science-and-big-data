import pathlib
import os
import time

parent_foldername = pathlib.Path(__file__).parent.resolve()
child_foldername = time.strftime("%Y-%m-%d-%H", time.localtime())
if not os.path.exists(os.path.join(parent_foldername, child_foldername)):
    os.mkdir(os.path.join(parent_foldername, child_foldername))

print(os.path.join(parent_foldername, child_foldername))
