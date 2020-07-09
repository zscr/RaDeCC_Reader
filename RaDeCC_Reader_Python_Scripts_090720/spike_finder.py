import numpy as np 

def spike_finder(counts_list, number_of_stds):
    results_list = []
    #print(np.average(counts_list)/np.median(counts_list))
    
    
    for i in range(len(counts_list)):
        copy_list = counts_list.copy()
        copy_list.pop(i)

        results_list.append(np.average(copy_list))
        #results_list.append(counts_list[i] > np.average(copy_list)+number_of_stds*np.std(copy_list))
    
    spike_dictionary = dict(zip(counts_list,results_list))
    return(results_list)

a_list = [1,3,1,2,3,100,1,2,3,1,3,2,5,2,4,2,3,0,1,2,3,5,3,2,1,2,4,3,2,0,1000]
b_list = [1,1,1,2,2,3,1,2,3,50,3,2,1,2,2,3,2,1,1]

# c_list.append()
# print (spike_finder(a_list,3))
# print (spike_finder(b_list,3))

# print (c_list) 
def spike_finder_2(counts_list, IQR_multiplier):
    index_list = []
    moving_window = 5
    for i in range(len(a_list)-moving_window+1):
        sample_window_list = counts_list[i:i+moving_window]
        q25,q50,q75 = np.quantile(sample_window_list, [.25,.50,.75])
        iqr = q75-q25
        # print (sample_window_list)
        #print (q50+IQR_multiplier*iqr)
        for j in range(len(sample_window_list)):
            if sample_window_list[j]> q50+IQR_multiplier*iqr:
                index_list.append(i+j)
    return(list(set(index_list)))

#a_list.append(1000)
# print (spike_finder_2(a_list, 3))

results = []
for i in range(100):
    c_list = np.random.rand(50)*10
    d_list = list(c_list)
    d_list[25] = 100.0

    results.append(spike_finder_2(d_list,20.0))


# print (results)
#print (d_list)
# print(np.quantile(a_list, [.25,.50,.75]))
# print(c_list)
