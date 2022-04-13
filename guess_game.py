from random import randint

def guess_game():
    n = randint(1, 1000)
    i = 1
    print("Загадано число от 1-1000. У вас 10 попыток. Отгадайте его.")
    while i <= 10:
        u = int(input(f'{str(i)}-я попытка: '))
        if u > n:
            print("Много")
        elif u < n:
            print("Мало")
        else:
            print(f'Вы угадали число с {i}-й попытки. Поздравляем!')
            break
        i += 1
    else:
        print("Вы исчерпали 10 попыток. Было загадано", n)

guess_game()