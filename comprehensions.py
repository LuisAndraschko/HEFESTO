import numpy as np


#################################### LIST COMPREHENSION #####################################
nums = np.arange(11)
# ########################################################### I want 'n' for each 'n' in nums
# # Non comprehensively
# my_list = []
# for n in nums:
#     my_list.append(n)
# print(my_list)
# # Comprehensively
# my_list = [n for n in nums]
# print(my_list)

########################################################### I want 'n*n' for each 'n' in nums
# # Non comprehensively
# my_list = []
# for n in nums:
#     my_list.append(n*n)
# print(my_list)
# # Comprehensively
# my_list = [n*n for n in nums]
# print(my_list)
# Using Map + lambda
# Map runs everything on a given list through a a certain function
# lambda is a anonymous function
# my_list = map(lambda n: n*n, nums)
# print(list(my_list))

################################################ I want 'n' for each 'n' in nums if n is even
# # Non comprehensively
# my_list = []
# for n in nums:
#     if n % 2 == 0:
#         my_list.append(n)
# print(my_list)
# # Comprehensively
# my_list = [n for n in nums if n % 2 == 0]
# print(my_list)
# # Using filter + lambda
# # filter runs everything on a given list through a certain function and returns a list
# # lambda is a anonymous function
# my_list = filter(lambda n: n % 2 == 0, nums)
# print(list(my_list))

############# I want a (letter, num) pair for each letter in 'abcd' and each number in '0123'
# # Non comprehensively
# my_list = []
# for letter in 'abcd':
#     for num in '0123':
#         my_list.append((letter, num))
# print(my_list)
# # Comprehensively 
# my_list = [(letter, num) for letter in 'abcd' for num in '0123']
# print(my_list)

#################################### DICT COMPREHENSION #####################################
names = ['Bruce', 'Clark', 'Peter', 'Logan', 'Wade']
heroes = ['Batman', 'Superman', 'Spiderman', 'Wolverine', 'Deadpool']
# print(dict(zip(names, heroes)))
############# I want a dict{'name': 'hero'} for each name, hero in zip(names, heroes)
# Non comprehensively
my_dict = {}
for name, hero in zip(names, heroes):
    my_dict[name] = hero
print(my_dict)
# Comprehensively 
my_dict = {name: hero for name, hero in zip(names, heroes)}
print(my_dict)

############# I want a dict{'name': 'hero'} for each name, hero in zip(names, heroes) if name not equal to Peter
# Non comprehensively
my_dict = {}
for name, hero in zip(names, heroes):
    if name != 'Peter':
        my_dict[name] = hero
print(my_dict)
# Comprehensively 
my_dict = {name: hero for name, hero in zip(names, heroes) if name!= 'Peter'}
print(my_dict)