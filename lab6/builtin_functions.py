from functools import reduce
import time


def task1(arr):
  return reduce(lambda acc, val: acc * val, arr, 1)


def task2(str):
  return {
    "lower_cnt": reduce(lambda acc, ch: acc + (ch == ch.lower() and ch != ch.upper()), str, 0),
    "upper_cnt": reduce(lambda acc, ch: acc + (ch != ch.lower() and ch == ch.upper()), str, 0),
  }


def task3(str):
  return str == str[::-1]
  return "".join(reversed(str)) == str


def task4(num, ms = 0):
  time.sleep(ms / 1000)
  return num ** .5


def task5(tpl):
  return all(tpl)


print(task1([1, 2, 3, 4, 5]))

print(task2("The text with 3 UpperCase and 39 lower case characters."))

print(task3("abbssbba"))

num_for_sqrt, ms = 25100, 2123
print(f"Square root of {num_for_sqrt} after {ms} miliseconds is {task4(num_for_sqrt, ms)}")

print(task5((True, True, True)), task5((True, False, True)))