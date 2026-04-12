data = [6, 12, 18, 24, 30, 35, 39] #use data created by task 1
def infection_wave(data):
    #calculate the infection wave based on the data
    diff = [0]*(len(data)-1)
    for i in range(1, len(data)):
        diff[i-1] = data[i] - data[i-1]
    return diff

def find_peak(data):
    #find the peak of the infection wave
    result = []
    for i in range(1, len(data)-1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            result.append([i, data[i]])
    if len(result) == 0:
        return [len(data)+1, data[-1]]
    elif len(result) == 1:
        return result[0]
    else:
        result.sort(key=lambda x: x[1], reverse=True)
        return result[0]

infection_wave_data = infection_wave(data)
peak = find_peak(infection_wave_data)
print("The peak of the infection wave is at day", peak[0])