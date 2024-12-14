import subprocess

def run_parallel():
    process1=subprocess.Popen(['python','key.py'])
    process2=subprocess.Popen(['python','window2.py'])
    process1.wait()
    process2.wait()
  
if __name__ == "__main__":
    run_parallel()  



                                                      