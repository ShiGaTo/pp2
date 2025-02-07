import math, random


def convert_from_gram_to_ounce(from_x):
    return 28.3495231 * from_x


def convert_from_fahr_to_cent(temperature):
    return (5 / 9) * (temperature - 32)


def solve(numheads, numlegs):
    # chickens + rabbits = numheads
    # chickens * 2 + rabbits * 4 = numlegs
    # rabbits = (numlegs - 2 * numheads) / 2
    # chickens = numheads - rabbits
    return {
        "rabbits": (numlegs - 2 * numheads) >> 1,
        "chickens": numheads - ((numlegs - 2 * numheads) >> 1)
    }


def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def filter_prime(arr):
    return list(filter(is_prime, arr))


def print_all_permutations(s):
    cnt = dict()
    for ch in s:
        if cnt.get(ch) == None:
            cnt[ch] = 0
        cnt[ch] += 1

    def rec(cur=""):
        if len(cur) == len(s):
            print(cur)
            return

        for ch, chCnt in cnt.items():
            if chCnt:
                cnt[ch] -= 1
                rec(cur + ch)
                cnt[ch] += 1

    rec()


def reverse_sentence(sentence):
    return " ".join(reversed(sentence.split(" ")))


def has_33(nums):
    return ("".join(map(str, nums))).find("33") != -1


def spy_game(nums):
    cnt0 = 0
    for num in nums:
        if num == 0:
            cnt0 += 1
        elif num == 7 and cnt0 >= 2:
            return True
    return False


def calc_sphere_volume(radius):
    return (4 * radius ** 3 * math.pi) / 3


def uniq(arr1):
    arr = sorted(arr1)
    res = []
    for i in range(len(arr) - 1):
        if arr[i] != arr[i + 1]:
            res.append(arr[i])
    res.append(arr[-1])
    return res


def is_palindrome(s):
    s = "".join(s.split(" ")).lower()
    return s == s[::-1]


def histogram(nums):
    for num in nums:
        print("*" * num)


def game():
    start, end = 1, 20
    user_attempts = 0
    name = ""

    print("Hello! What is your name?")
    name = input()

    print()
    print(f"Well, {name}, I am thinking of a number between {start} and {end}.")
    guessed_num = random.randint(start, end)

    while 1:
        print("Take a guess.")
        user_num = int(input())
        user_attempts += 1

        print()
        if user_num < guessed_num:
            print("Your guess is too low.")
        elif user_num > guessed_num:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {user_attempts} guesses!")
            break


if __name__ == "__main__":
    print("Testing...")