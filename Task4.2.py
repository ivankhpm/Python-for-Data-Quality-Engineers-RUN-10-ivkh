import random
import string

### FUNCTIONS

#func 1
#generated rumber of dicts (random from 2 tp 10), can be replaced by user's input
def dictionary_generator(dict_number):
    print("\nThe number of generated dictionaries is", dict_number)
    #list to store all dictionaries
    all_dicts = [{random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in range(random.randint(5, 15))} for _ in range(dict_number)]
    return all_dicts


#func 2
def max_dict_values(all_dicts):
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
    return final_dict




### USAGE of funcs
test = dictionary_generator(7)

print("\nGenerated dicts:")
for x, y in enumerate(test):
    print(f'D_{x} is {y}')


# Result
print("\n\nFINAL DICT:\n", max_dict_values(test))