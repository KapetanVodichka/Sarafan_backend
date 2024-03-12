def generate_sequence(n):
    string = ""
    num = 1

    for i in range(1, n + 1):
        string += str(num) * num
        num += 1

    return string


n = int(input("Введите количество элементов последовательности: "))
string = generate_sequence(n)
print(string)