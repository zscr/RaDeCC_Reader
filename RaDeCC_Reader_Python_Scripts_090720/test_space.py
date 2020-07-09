import numpy as np 


list_a = [1,1,1,1,2,2,2,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,4,4,1400,3,5,3,2,2,2,2,1,1,1]

list_b = [1,1,1,1,2,2,2,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,4,4,8,3,5,3,2,2,2,2,1,1,1]

n = 6
pair = [1,2]
lista = []
for i in range(n):
    lista.append(pair)

print(lista)

lista[0][1] = 5
print(lista)

def test_function():
    var_a = 'yes'
    var_b = 'no'
    return(var_a, var_b)

test_results = test_function()
print (test_results[1])










# def spike_detection(counts_list, number_of_stds):
#     results_list = []
#     q75, q25 = np.percentile(counts_list, [75 ,25])
#     iqr = q75-q25
#     print(np.average(counts_list)/np.median(counts_list))
#     for i in range(len(list_a)):
#         results_list.append(counts_list[i] > np.average(counts_list)+number_of_stds*np.std(counts_list))
#     return(str(results_list).count('True'))


# print (spike_detection(list_a, 3))
# print (spike_detection(list_b, 3))

# diff_list = []
# for i in range(len(list_b)):
#     for j in range(len(list_b)):
#         diff_list.append(list_b[i]-list_b[j])

# print(diff_list, np.average(diff_list))

