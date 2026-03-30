# Logging System 

# Problem Statement: 
# Log errors with timestamp to file (txt or Json). 

# Output Format: 

# 2026-01-01 10:00:00 ERROR Something failed 

# explain the above

from datetime import datetime
def logerror(message="ERROR something failed\n"):
    
    timestamp=datetime.now().strftime("%y-%m-%d %H:%M:%S")
    
    with open("log.txt",'a') as f:
        f.write(f"{timestamp} {message}")
    print(timestamp)
    

logerror()
logerror("Main system DOWN!\n")
logerror("Illegal Access\n")

