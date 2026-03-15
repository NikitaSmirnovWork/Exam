diapazon_int = list(map(int, input().split()))
otvet = [0, 1]
for i in range(2, 25):
    otvet.append(otvet[i - 2] + otvet[i - 1])
start_index = 0
for m in otvet:
    if m > diapazon_int[0]:
        start_index = otvet.index(m)
        break
end_index = 0
for v in otvet:
    if v > diapazon_int[1]:
        end_index = otvet.index(v)
        break
if end_index == 0:
    end_index = len(otvet)
itog = " ".join(map(str, otvet[start_index:end_index]))
if (itog) == "" or (itog) == " ":
    print("В заданном диапазоне нет чисел Фибоначчи")
else:
    print(itog)
