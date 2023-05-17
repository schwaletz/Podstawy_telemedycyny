import random
import matplotlib.pyplot as plt
import pandas as pd

Generated_signals = pd.Series()
mean_signal = pd.Series()
# deklaracja zmiennych listy
Normal = []
Supraventicular_ectopic = []
Fusion = []
Ventricular_entropic = []
Unknow = []
column_names = []
Sets = [Normal, Supraventicular_ectopic, Fusion, Ventricular_entropic, Unknow]
start = 1
end = 187
"data - https://www.physionet.org/content/mitdb/1.0.0/"
"data - https://www.kaggle.com/datasets/shayanfazeli/heartbeat/code?select=mitbih_test.csv"
data = pd.read_csv('mitbih_train.csv', index_col=0)

print(data.shape)
# print(data.info)
"Five classes of ECG beat (0) normal (N), (1) supraventricular ectopic (S), (2) fusion (F), (3) ventricular ectopic (V), and (4) unknown (Q)."

# dzielenie cvs wg sygnału (normalny, z zaburzeniami)
for i in range(len(Sets)):
    for row in range(data.shape[0]):
        if data.iloc[row, -1] == i:
            str(Sets[i].append(data.iloc[row, :]))

# lista z nazwami kolumn, dobrze było by zmienic te nazwy na np.numer próbkowania lub jednostke czasu
for column in data.columns:
    column_names.append(str(column))
column_names = column_names[:-1]

# ------------OPCJE-----

# wybor rodzaju sygnalu i tego jak bardzo sygnal ma byc podobny do wzrocowego
option = int((input(
    f" 1 - Normal beat \n 2 - supraventricular ectopic beat \n 3 - Fushion beat \n 4 - Ventricular ectopic beat ")))
input_num = float(input("\n podaj korelacje względem sygnału wzorcowego "))
input_num = 0.9
# wygladzanie sygnału, 20 to takie optimum
smooth = int(input('\n podaj wartosc wygladzenia sygnalu '))

if option == 1:
    # usuwanie z zbioru granicznych wartosci max i min w celu "oczyszczenia" danych
    Normal = pd.DataFrame(Normal, columns=column_names)
    Normal = Normal.iloc[:, :-1]
    print(f' shape before max/min drop: {Normal.shape}')
    for i in range(Normal.shape[1]):
        if Normal.shape[0] > 40:
            if 184 > i > 5:
                max_value = (Normal[column_names[i]]).max()
                min_value = (Normal[column_names[i]]).min()
                max_value_indexes = Normal.index[Normal[column_names[i]] == max_value].tolist()
                Normal.drop(max_value_indexes, inplace=True)
                min_value_indexes = Normal.index[Normal[column_names[i]] == min_value].tolist()
                Normal.drop(min_value_indexes, inplace=True)
    print(f'shape after max/min drop: {Normal.shape}')

    # rzeczy do plotowania
    minimal = Normal.min()
    maximal = Normal.max()
    for n in range(1, 5):
        mean = Normal.mean()
        Generated_signal = mean
        index = Generated_signal.index
        for i in range(186):
            if i < 2:
                Generated_signal = Generated_signal.replace(float(Generated_signal[i]), -0.7)
            elif 184 > i >= 2:
                minimal_num = float(minimal[i])
                maximal_num = float(maximal[i])
                mean_num = float(mean[i])
                minimal_num = minimal_num + ((mean_num - minimal_num) * input_num)
                maximal_num = maximal_num - ((maximal_num - mean_num) * input_num)
                Generated_signal_number = ((mean_num + random.uniform(minimal_num, maximal_num)) / 2)
                Generated_signal = Generated_signal.replace(Generated_signal[index[i]], Generated_signal_number)
            else:
                Generated_signal = Generated_signal.replace(Generated_signal[index[i]], 2.2)

        Generated_signal = Generated_signal.set_axis(list(range(start, end)))
        mean = mean.set_axis(list(range(start, end)))
        start = start + 186
        end = start + 186
        Generated_signals = Generated_signals._append(Generated_signal)
        mean_signal = mean_signal._append(mean)
    for x in range(smooth):
        for i in range(3, (186 * n)):
            Generated_signals[i] = (Generated_signals[i] + Generated_signals[i + 1]) / 2

    # ocena
    dif = 0
    for i in range(1, Generated_signals.shape[0]):
        dif = dif + (abs(Generated_signals[i] - mean_signal[i])) / mean_signal[i]
    ocena = (dif / Generated_signals.shape[0]) * 100
    print(
        f'-------------\n procentowa różnica pomiędzy wygenerowanym sygnałem \n a sygnałem referencyjnym wynosi: {ocena}\n --------------------------')
    #wykres wygenerowany sygnał / sygnał wzorcowy
    plt.figure()
    Generated_signals[4:730].plot(color='blue')
    mean_signal[4:730].plot(color='red', linestyle='dashed')
    plt.show()
    Generated_signals.to_csv('generated_signal.csv')
elif option == 2:
    Supraventicular_ectopic = pd.DataFrame(Supraventicular_ectopic, columns=column_names)
    Supraventicular_ectopic = Supraventicular_ectopic.iloc[:, :-1]
    print(f' shape before max/min drop: {Supraventicular_ectopic.shape}')
    for i in range(Supraventicular_ectopic.shape[1]):
        if Supraventicular_ectopic.shape[0] > 40:
            if 183 > i > 5:
                max_value = (Supraventicular_ectopic[column_names[i]]).max()
                min_value = (Supraventicular_ectopic[column_names[i]]).min()
                max_value_indexes = Supraventicular_ectopic.index[
                    Supraventicular_ectopic[column_names[i]] == max_value].tolist()
                Supraventicular_ectopic.drop(max_value_indexes, inplace=True)
                min_value_indexes = Supraventicular_ectopic.index[
                    Supraventicular_ectopic[column_names[i]] == min_value].tolist()
                Supraventicular_ectopic.drop(min_value_indexes, inplace=True)
    print(f'shape after max/min drop: {Supraventicular_ectopic.shape}')

    minimal = Supraventicular_ectopic.min()
    maximal = Supraventicular_ectopic.max()
    for n in range(1, 5):
        mean = Supraventicular_ectopic.mean()
        Generated_signal = mean
        index = Generated_signal.index
        for i in range(186):
            if i < 2:
                Generated_signal = Generated_signal.replace(float(Generated_signal[i]), -0.5)
            elif 184 > i >= 2:
                minimal_num = float(minimal[i])
                maximal_num = float(maximal[i])
                mean_num = float(mean[i])
                minimal_num = minimal_num + ((mean_num - minimal_num) * input_num)
                maximal_num = maximal_num - ((maximal_num - mean_num) * input_num)
                Generated_signal_number = ((mean_num + random.uniform(minimal_num, maximal_num)) / 2)
                Generated_signal = Generated_signal.replace(Generated_signal[index[i]], Generated_signal_number)
            else:
                Generated_signal = Generated_signal.replace(Generated_signal[index[i]], 1.8)

        Generated_signal = Generated_signal.set_axis(list(range(start, end)))
        mean = mean.set_axis(list(range(start, end)))
        start = start + 186
        end = start + 186
        Generated_signals = Generated_signals._append(Generated_signal)
        mean_signal = mean_signal._append(mean)
    for x in range(smooth):
        for i in range(3, (186 * n)):
            Generated_signals[i] = (Generated_signals[i] + Generated_signals[i + 1]) / 2

    # ocena
    dif = 0
    for i in range(1, Generated_signals.shape[0]):
        dif = dif + (abs(Generated_signals[i] - mean_signal[i])) / mean_signal[i]
    ocena = (dif / Generated_signals.shape[0]) * 100
    print(
        f'-------------\n procentowa różnica pomiędzy wygenerowanym sygnałem \n a sygnałem referencyjnym wynosi: {ocena}\n --------------------------')
    # na wykresach: wartosc max, min, srednia, mediana i wygenerowany sygnal
    plt.figure()
    Generated_signals[4:730].plot(color='blue')
    mean_signal[4:730].plot(color='red', linestyle='dashed')
    plt.show()
    Generated_signals.to_csv('generated_signal.csv')
elif option == 3:

    Fusion = pd.DataFrame(Fusion, columns=column_names)
    Fusion = Fusion.iloc[:, :-1]
    print(f' shape before max/min drop: {Fusion.shape}')
    for i in range(Fusion.shape[1]):
        if Fusion.shape[0] > 40:
            if 183 > i > 5:
                max_value = (Fusion[column_names[i]]).max()
                min_value = (Fusion[column_names[i]]).min()
                max_value_indexes = Fusion.index[Fusion[column_names[i]] == max_value].tolist()
                Fusion.drop(max_value_indexes, inplace=True)
                min_value_indexes = Fusion.index[Fusion[column_names[i]] == min_value].tolist()
                Fusion.drop(min_value_indexes, inplace=True)
    print(f'shape after max/min drop: {Fusion.shape}')

    minimal = Fusion.min()
    maximal = Fusion.max()

    for n in range(1, 5):
        mean = Fusion.mean()
        Generated_signal = mean
        index = Generated_signal.index
        for i in range(2, 184):
            minimal_num = float(minimal[i])
            maximal_num = float(maximal[i])
            mean_num = float(mean[i])
            minimal_num = minimal_num + ((mean_num - minimal_num) * input_num)
            maximal_num = maximal_num - ((maximal_num - mean_num) * input_num)
            Generated_signal_number = ((mean_num + random.uniform(minimal_num, maximal_num)) / 2)
            Generated_signal = Generated_signal.replace(Generated_signal[index[i]], Generated_signal_number)

        Generated_signal = Generated_signal.set_axis(list(range(start, end)))
        mean = mean.set_axis(list(range(start, end)))
        start = start + 186
        end = start + 186
        Generated_signals = Generated_signals._append(Generated_signal)
        mean_signal = mean_signal._append(mean)
    for x in range(smooth):
        for i in range(3, (186 * n)):
            Generated_signals[i] = (Generated_signals[i] + Generated_signals[i + 1]) / 2

    # ocena
    dif = 0
    for i in range(1, Generated_signals.shape[0]):
        dif = dif + (abs(Generated_signals[i] - mean_signal[i])) / mean_signal[i]
    ocena = (dif / Generated_signals.shape[0]) * 100
    print(
        f'-------------\n procentowa różnica pomiędzy wygenerowanym sygnałem \n a sygnałem referencyjnym wynosi: {ocena}\n --------------------------')
    # na wykresach: wartosc max, min, srednia, mediana i wygenerowany sygnal
    plt.figure()
    Generated_signals[4:730].plot(color='blue')
    mean_signal[4:730].plot(color='red', linestyle='dashed')
    plt.show()
    Generated_signals.to_csv('generated_signal.csv')
elif option == 4:

    Ventricular_entropic = pd.DataFrame(Ventricular_entropic, columns=column_names)
    Ventricular_entropic = Ventricular_entropic.iloc[:, :-1]
    print(f' shape before max/min drop: {Ventricular_entropic.shape}')
    for i in range(Ventricular_entropic.shape[1]):
        if Ventricular_entropic.shape[0] > 40:
            if 183 > i > 5:
                max_value = (Ventricular_entropic[column_names[i]]).max()
                min_value = (Ventricular_entropic[column_names[i]]).min()
                max_value_indexes = Ventricular_entropic.index[
                    Ventricular_entropic[column_names[i]] == max_value].tolist()
                Ventricular_entropic.drop(max_value_indexes, inplace=True)
                min_value_indexes = Ventricular_entropic.index[
                    Ventricular_entropic[column_names[i]] == min_value].tolist()
                Ventricular_entropic.drop(min_value_indexes, inplace=True)
    print(f' after max/min drop: {Ventricular_entropic.shape}')

    minimal = Ventricular_entropic.min()
    maximal = Ventricular_entropic.max()

    for n in range(1, 5):
        mean = Ventricular_entropic.mean()
        Generated_signal = mean
        index = Generated_signal.index
        for i in range(2, 184):
            minimal_num = float(minimal[i])
            maximal_num = float(maximal[i])
            mean_num = float(mean[i])
            minimal_num = minimal_num + ((mean_num - minimal_num) * input_num)
            maximal_num = maximal_num - ((maximal_num - mean_num) * input_num)
            Generated_signal_number = ((mean_num + random.uniform(minimal_num, maximal_num)) / 2)
            Generated_signal = Generated_signal.replace(Generated_signal[index[i]], Generated_signal_number)

        Generated_signal = Generated_signal.set_axis(list(range(start, end)))
        mean = mean.set_axis(list(range(start, end)))
        start = start + 186
        end = start + 186
        Generated_signals = Generated_signals._append(Generated_signal)
        mean_signal = mean_signal._append(mean)
    for x in range(smooth):
        for i in range(3, (186 * n)):
            Generated_signals[i] = (Generated_signals[i] + Generated_signals[i + 1]) / 2

    # ocena
    dif = 0
    for i in range(1, Generated_signals.shape[0]):
        dif = dif + (abs(Generated_signals[i] - mean_signal[i])) / mean_signal[i]
    ocena = (dif / Generated_signals.shape[0]) * 100
    print(
        f'-------------\n procentowa różnica pomiędzy wygenerowanym sygnałem \n a sygnałem referencyjnym wynosi: {ocena}\n --------------------------')
    # na wykresach: wartosc max, min, srednia, mediana i wygenerowany sygnal
    plt.figure()
    Generated_signals[4:730].plot(color='blue')
    mean_signal[4:730].plot(color='red', linestyle='dashed')
    plt.show()
    Generated_signals.to_csv('generated_signal.csv')

elif option == 5:
    median = Unknow.median()
    mean = Unknow.mean()
    minimal = Unknow.min()
    maximal = Unknow.max()

    Unknow = pd.DataFrame(Unknow, columns=column_names)
    Unknow = Unknow.iloc[:, :-1]
    print(f' shape before max/min drop: {Unknow.shape}')
    for i in range(Unknow.shape[1]):
        if Unknow.shape[0] > 40:
            if 183 > i > 5:
                max_value = (Unknow[column_names[i]]).max()
                min_value = (Unknow[column_names[i]]).min()
                max_value_indexes = Unknow.index[Unknow[column_names[i]] == max_value].tolist()
                Unknow.drop(max_value_indexes, inplace=True)
                min_value_indexes = Unknow.index[Unknow[column_names[i]] == min_value].tolist()
                Unknow.drop(min_value_indexes, inplace=True)
    print(f' after max/min drop: {Unknow.shape}')

    minimal = Unknow.min()
    maximal = Unknow.max()

    for n in range(1, 5):
        mean = Unknow.mean()
        Generated_signal = mean
        index = Generated_signal.index
        for i in range(186):
            if i < 2:
                Generated_signal = Generated_signal.replace(float(Generated_signal[i]), 2.2)
            elif 184 > i >= 2:
                minimal_num = float(minimal[i])
                maximal_num = float(maximal[i])
                mean_num = float(mean[i])
                minimal_num = minimal_num + ((mean_num - minimal_num) * input_num)
                maximal_num = maximal_num - ((maximal_num - mean_num) * input_num)
                Generated_signal_number = ((mean_num + random.uniform(minimal_num, maximal_num)) / 2)
                Generated_signal = Generated_signal.replace(Generated_signal[index[i]], Generated_signal_number)
            else:
                Generated_signal = Generated_signal.replace(Generated_signal[index[i]], -0.7)

        Generated_signal = Generated_signal.set_axis(list(range(start, end)))
        mean = mean.set_axis(list(range(start, end)))
        start = start + 186
        end = start + 186
        Generated_signals = Generated_signals._append(Generated_signal)
        mean_signal = mean_signal._append(mean)
    for x in range(smooth):
        for i in range(3, (186 * n)):
            Generated_signals[i] = (Generated_signals[i] + Generated_signals[i + 1]) / 2

    # ocena
    dif = 0
    for i in range(1, Generated_signals.shape[0]):
        dif = dif + (abs(Generated_signals[i] - mean_signal[i])) / mean_signal[i]
    ocena = (dif / Generated_signals.shape[0]) * 100
    print(
        f'-------------\n procentowa różnica pomiędzy wygenerowanym sygnałem \n a sygnałem referencyjnym wynosi: {ocena}\n --------------------------')
    # na wykresach: wartosc max, min, srednia, mediana i wygenerowany sygnal
    plt.figure()
    Generated_signals[4:730].plot(color='blue')
    mean_signal.plot(color='red', linestyle='dashed')
    plt.show()
    Generated_signals.to_csv('generated_signal.csv')
else:
    print('invalid option value')
