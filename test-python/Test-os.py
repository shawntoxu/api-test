import os 

host=os.popen('hostname')
print host.read().strip()
    