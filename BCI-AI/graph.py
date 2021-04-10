import matplotlib.pyplot as plt
import numpy as np
import time
# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')


import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from urllib.request import urlretrieve

def live_plotter(x_vec, y1_data, line1, identifier='', pause_time=0.000001):
    if line1 == []:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec, y1_data, '-o', alpha=0.8)
        # update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()

    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data) <= line1.axes.get_ylim()[0] or np.max(y1_data) >= line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line1


def make_fft(test):
    test_f = np.zeros(test.shape)
    for i in range(len(test_f)):
        length = test[i, 0]
        test_f[i, 0] = test[i, 0]
        test_f[i, -1] = test[i, -1]

        for j in range(1):
            test_f[i][int(1 + 1024 * j):int(1 + 1024 * j + length)] = np.abs(
                np.fft.fft(test[i][int(1 + 1024 * j):int(1 + 1024 * j + length)]))
    return test_f


import pickle
import numpy as np
# loading
with open('test.pickle', 'rb') as handle:
    test = pickle.load(handle)

# loading
with open('pca.pickle', 'rb') as handle:
    pca = pickle.load(handle)

# loading
with open('neigh.pickle', 'rb') as handle:
    neigh = pickle.load(handle)

time.sleep(3)
size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]

y_vec = np.zeros(x_vec.shape)
line1 = []
num=[15, 12, 11, 7, 13, 5, 10, 8, 18, 19, 6]
count=0
for i in num:
    count+=1
    start_time = time.time()
    print(" ")
    print(" ")
    print('set: '+str(count))
    #prediction=neigh.predict(pca.transform(make_fft(test[i:i+1])))[0]
    actual=test[i][-1]
    if actual!=-1:
        print("user is asked to think about: "+str(int(actual)))
    else:
        print("user is asked to think anything other then a number")
    temp=[]
    for j in test[i][:-1]:
        rand_val = j
        y_vec[-1] = rand_val
        line1 = live_plotter(x_vec, y_vec, line1)
        y_vec = np.append(y_vec[1:], 0.0)
        temp.append(j)
        #time.sleep(0.000000000001)
    #predict=len(temp)
    temp+=[actual]
    predict=neigh.predict(pca.transform(make_fft(np.array([temp]))))
    end_time = time.time()
    if predict != -1:
        print("Our BCI-AI predicts user is thinking about: "+str(int(predict)))
    else:
        print("Our BCI-AI predicts thinking about something other then a number")

    print("total time taken in the current instance: ", end_time - start_time)




'''size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
print(x_vec)
y_vec = np.random.randn(len(x_vec))
print(y_vec)
line1 = []
while True:
    rand_val = np.random.randn(1)
    y_vec[-1] = rand_val
    line1 = live_plotter(x_vec,y_vec,line1)
    y_vec = np.append(y_vec[1:],0.0)
    time.sleep(0.5)'''