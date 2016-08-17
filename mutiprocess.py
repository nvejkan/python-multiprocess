import math
import time
from multiprocessing import Pool

def test_func(i):
    '''
    This function consumes a lot CPU power.
    It returns the sum of the arctan values of the list, i.
    '''
    j = 0
    for x in i:
        j += math.atan2(x, x)
    return j

def plot(x,y):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    index = x
    bar_width = 0.85

    rects1 = plt.bar(index, y, bar_width,
                    align='center',
                    color='g',
                    label='time')

    plt.xlabel('no. of pool')
    plt.ylabel('Time')
    plt.title('Time / no. of pool')
    plt.xticks(x, x) #show all x-ticks
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    #generate a big list
    data = [ i for i in range(0,20000000)]

    #number of pools for each test
    l = range(1,17)
    n_time = []
    for i in l:
        time_list = [] # a list to keep each loop's time
        step = math.ceil(len(data)/i) # calculate a step size to split the data into chucks

        #Will run each test for 5 times and then find the average running time
        for j in range(0,5):
            slices = (data[i:i + step] for i in range(0, len(data), step)) #split the data into chucks 
            pool = Pool(processes=i) # set no. of pools
            start_time = time.time() # start the timer
            
            ret1 = pool.map_async(test_func, slices) #Call the test_func. Map each chuck to pools one-by-one.
            answer = sum(ret1.get()) #This is how to get the return from each pool
            #print(answer) #print the result

            #close the process pool
            pool.close()
            pool.terminate()
            pool.join()
            
            elapsed_time = time.time() - start_time # stop the timer
            time_list.append(elapsed_time) # append to the list
        #print(time_list)
        avg_time = sum(time_list)/len(time_list)
        print_str = "{0} processes time: {1}\n"
        print(print_str.format(i,avg_time)) #show the resulted running time of each N pool.
        n_time.append(avg_time)

    plot(l,n_time) #plot the graph
