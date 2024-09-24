import random
import string


### PART1 ###
#generated rumber of dicts (random from 2 tp 10), can be replaced by user's input
dict_number = random.randint(2, 10)
print("\nThe number of generated dictionaries is", dict_number)

#list to store all dictionaries
all_dicts = []

#to iterate
i=1 #iterate every dictionary
g=0 #itarate every element in dictionary

while i <= dict_number:
    random_dict = {}
    #every dict would have diff number of pairs key+values from 5 to 15
    dict_size = random.randint(5, 15)

    #list to store all letters
    letters = list(string.ascii_lowercase)
    g = 0
    #to generate diff amount
    while g <= dict_size:
        #select random letter
        dict_key = random.sample(letters, 1)[0]

        #remove selected letter to avoid key's duplications
        letters.remove(dict_key)

        #random value
        dict_value = random.randint(0, 100)
        random_dict[dict_key] = dict_value
        g+=1
    ## add newly created dict to list of dicts
    all_dicts.append(random_dict)
    i+=1

print("\nGenerated dicts:")
for item in all_dicts:
    print(f'D_{all_dicts.index(item)} is {item}')

### PART2 ###
final_dict = {}

# Collect all unique keys from all dictionaries to set
all_keys = set()
for d in all_dicts:
    all_keys.update(d.keys())

# Iterate over each unique key
for key in all_keys:
    max_value = 0 # To store max_value
    max_index = 0 # To srote max index of dictionary
    count = 0  # To count occurrences of the key across dicts

    #Check every dictionary to find max value and index of dict
    for index, d in enumerate(all_dicts):
        if key in d:
            count += 1
            if d[key] >= max_value:
                max_value = d[key]
                max_index = index

    # Determine how to store the key based on its occurrences
    if count == 1:
        final_dict[f"{key}"] = max_value
    else:
        final_dict[f"{key}_{max_index}"] = max_value

# Result
print("\n\nFINAL DICT:\n", final_dict)
