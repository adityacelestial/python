from datetime import datetime
import multiprocessing

processes=[]
values = [10_000_000, 25_000_000, 15_000_000, 20_000_000] 

def compute_squares(value):
    sum=0
    for v in range(value):
        sum+=v**2

if __name__=="__main__":
    
    start=datetime.now()

    for value in values:
        compute_squares(value)
    print(f"Single pocess seq {datetime.now()-start}")
    start=datetime.now()
    for value in values:
        p=multiprocessing.Process(target=compute_squares,args=(value,))
        p.start()
        processes.append(p)
    for process in processes:
        process.join()
    print(f"Multi processing {datetime.now()-start}")