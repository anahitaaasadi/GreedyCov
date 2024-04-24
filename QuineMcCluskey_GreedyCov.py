# A custom function for binary representation with specific length, so that it'll be easilly called and reused throughout the code:
def decimal_to_binary_fixed_width(decimal, width):
    # Convert decimal to binary using bin() and remove the '0b' prefix (cell 0 and 1 of the array)
    binary_representation = bin(decimal)[2:]
    
    # Ensure the binary representation has a fixed width. It's also beneficial when we have different lengths for binary numbers and want to
    # set them all as the maximum length (writing 5 as 0101 instead of 101 when we have 15, which is 1111)
    binary_representation = binary_representation.zfill(width)

    return binary_representation

# Get minterms and don't cares from the user
Min_or_Max = int(input("For minterms (will be represented by SOP) press 1. For maxterms (will be represented by POS) press 2."))

user_minterms = [int(num) for num in input("Enter the list of minterms separated by spaces: ").split()]
user_dontcares = [int(num) for num in input("Enter the list of don't cares separated by spaces: ").split()]

#Check for any common terms between minterm and don't care

if set(user_minterms).intersection(set(user_dontcares)):
    print("Stop Execution !!!! There is a don't care duplicated in minterms")
    # Stop execution or perform further actions here
else:
    print("Good to proceed")

input_minterms = sorted(user_minterms)
input_dontcares = sorted(user_dontcares)
min_dc = input_minterms + input_dontcares

# Determine the maximum width required based on the greatest input
max_width = len(bin(max(min_dc))) - 2

# Convert each input to binary with the determined width
binary_numbers = [decimal_to_binary_fixed_width(num, max_width) for num in min_dc]

# Display the binary representation of each number
print(f"Decimal | Binary")
print("----------------")
for i in range(len(min_dc)):
    print(f"{min_dc[i]} \t| {binary_numbers[i]}")
    #print(binary_numbers[i])

def count_ones(binary_string):
    # Count the number of ones in the binary string
    return binary_string.count('1')

# Categorize based on the number of ones
# To do this, a dictionary with cells like {number of ones: an array of corresponding binary numbers} is made:
total_pi = set()
categories = {}
for binary_number in binary_numbers:
    ones_count = count_ones(binary_number)
    if ones_count not in categories:
        categories[ones_count] = []
    categories[ones_count].append(binary_number)

# Sort categories based on the number of ones they have in ascending order
# Also, sort numbers within each category in ascending order
# Print the table in the end and divide each category
print(f"Decimal | Binary")
print("----------------")
for ones_count in sorted(categories.keys()):
    sorted_numbers = sorted(categories[ones_count])
    for binary_number in sorted_numbers:
        decimal_number = int(binary_number, 2)
        print(f"{decimal_number} \t| {binary_number}")
    print("----------------")

# Apply Combining theorem to two minterms if they differ excatly by 1 binary place
# If two numbers differed in one bit, returns the bit number by which they differ
# If two numbers were different in more than one bit, return the numbers themselves
def minterms_comparision(a, b): 
    diff = 0
    for j in range(len(a)):
        if a[j] != b[j]:
            diff_bit_index = j
            diff += 1
            if diff > 1:
                return (False, None)
    return(True, diff_bit_index)

# Dictionary to list conversion:
def dict_to_list(a):
    binary_mt_dc_list = []
    for i in a:
        binary_mt_dc_list.extend(a[i])
    return(binary_mt_dc_list)

# Determine the minterm based on the uncombined form or determine the minterms combined based on the combined form,
# When a is the binary PI and i is the bit number, initiallized as 0:
def determine_minterm(a, i = 0):
    temp = []
    if i == len(a):
        temp.append(a)
        return[str(int(temp[i], 2)) for i in range(len(temp))] # Binary to decimal conversion
# Write each - as 0 and 1 until we have ran out of -'s and increment the index:
    if a[i] == "-":
        a_0 = a[:i] + '0' + a[i+1:]
        temp.extend(determine_minterm(a_0, i+1))
        a_1 = a[:i] + '1' + a[i+1:]
        temp.extend(determine_minterm(a_1, i+1))
    else:
# Only increment the index in the absence of -:
        temp.extend(determine_minterm(a, i+1))
    return temp

# Remove don't cares themselves (empty rows in the chart) from the PI chart
# The minterm sequence giving error: [1 2 3 4], don't care sequence: [5 6 7 8]. has 1000 without any minterms
def remove_dc_PI_table(x):
    temp=x.copy()
    binary_equivalents_dc = [bin(decimal_digit)[2:] for decimal_digit in input_dontcares] 
    for i,j in x.items():
        if '-' not in i:
            if str(i) in binary_equivalents_dc:
                del temp[i]           
    return temp

# Removes the PI consisted upon don't cares only
# The minterm sequence giving error: [4, 5, 6, 8, 9, 10, 13], don't care sequence: [0, 7, 15].
def remove_dc_PI(x):
    result = {}
    for key, value_list in x.items():
        cleaned_list = [item for item in value_list if int(item) not in input_dontcares]
        result[key] = cleaned_list
    return result

def sum_of_ones_zeros(binary_string):
    return binary_string.count('0') + binary_string.count('1')


total_pi=[]
while True:
    temp_categories = categories.copy() # Creating a copy of previously grouped minterms based on the number of 1's
    categories, g = {}, 0 # A list of minterms
    tick = [] # A set of ticked grouped minterms, which will give us the final PI
    finish = True
    l = sorted(list(temp_categories.keys())) # Sorting the groups in the ascending order
    # Comparing minterms in each category with the minterms in the next one. Do that with every single minterm:
    for m in range(len(l)-1):
        for i in temp_categories[l[m]]: 
            for j in temp_categories[l[m+1]]:
                result = minterms_comparision(i, j)
                if result[0]: # If they differend in a single bit:
                    try: # If we already had a category for this number of ones, we can append it:
                        if j[:result[1]] + '-' + j[result[1]+1:] not in categories[g] :
                            categories[g].append(j[:result[1]] + '-' + j[result[1]+1:])
                            term = j[:result[1]] + '-' + j[result[1]+1:] 
                    except: # If we didn't have a category for this number of ones, we should create a new one:
                        categories[g] = [j[:result[1]] + '-' + j[result[1]+1:]]
                        term = j[:result[1]] + '-' + j[result[1]+1:]
                    finish = False
                    # Mark the combined minterms:
                    if i not in tick:
                        tick.append(i)
                    if j not in tick:
                        tick.append(j)
        g += 1
    #pi = list(set(dict_to_list(temp_categories)).difference(tick))
    pi=list(filter(lambda x: x not in tick, dict_to_list(temp_categories)))
    #pi=sorted(pi)
    #pi=sorted(pi, key=lambda x: x.count('0'), reverse=True)
    total_pi.extend(pi)
    if len(pi) == 0: 
        print("Unticked minterm for the above table:", None)
    else: 
        print("Unticked minterm for the above table:", ','.join(pi))
    if finish:
        if len(total_pi) == 0:
            print("Unticked minterm:", None)
        else:
            print("prime Implicants:", ','.join(total_pi))
        break
    print(f"min/Maxterms\t| PIs")
    print("-------------------------------")
    for i in sorted(categories.keys()):
        for j in categories[i]:
            print(f"{','.join(determine_minterm(j))}\t|{j}")
        print("-------------------------------")
total_pi= sorted(total_pi, key=sum_of_ones_zeros)
total_pi= sorted(total_pi, key=lambda x: x.count('0'))
pi_table = {i: determine_minterm(i) for i in total_pi}
print(pi_table)
pi_table=remove_dc_PI_table(pi_table)
pi_table=remove_dc_PI(pi_table)
print(pi_table)

# Draw PI Chart:
import copy
def remove_empty_PIs(original_table):
    table = copy.deepcopy(original_table)
    temp = [key for key, values in table.items() if not values]
    for key in temp:
        del table[key]
    return table
pi_table= remove_empty_PIs(pi_table)

def draw_chart(table):
    print("PI table so far:")
    minterms = sorted(set(int(value) for sublist in table.values() for value in sublist))
    minterms = [value for value in minterms if value not in input_dontcares]
    chart = {j: ['x' if str(i) in table[j] else '' for i in minterms] for j in table}
    print(max_width*" "+"|"+"\t" + "\t".join(map(str, minterms)))
    print("----------" * len(minterms) + "--------")
    for i, j in chart.items():
        print(i + "|" + "\t" + "\t".join(j))
    return

draw_chart(pi_table)

# Switch the dictionary (turn {PI: minterm} to {minterm: PI} and vice versa)
import copy
def switch_dict(original_dict):
    dict = copy.deepcopy(original_dict)
    switched_dict = {value: [str(key) for key, values in dict.items() if value in values] for values in dict.values() for value in values}
    return switched_dict

# Determine EPIs:
def determine_EPI(original_table):
    table = copy.deepcopy(original_table)
    x = switch_dict(table)
    result = []
    for i,j in x.items():
        if len(j) == 1:
            result.append(j[0]) if j[0] not in result else None
    return result

# Clean the PIs chosen and the corresponding minterms:
def clean_table(original_table, PI):
    table = copy.deepcopy(original_table)
    for key in PI:
        if key in table:
            values_to_remove = table[key]
            del table[key]
            for other_key, values in table.items():
                table[other_key] = [value for value in values if value not in values_to_remove]
    return table

# Remove the PIs with minterms already covered by chosen PIs:
def remove_empty_PIs(original_table):
    table = copy.deepcopy(original_table)
    temp = [key for key, values in table.items() if not values]
    for key in temp:
        del table[key]
    return table

EPI=determine_EPI(pi_table)
print("EPI List:")
print(EPI)
cleaned_table=clean_table(pi_table,EPI)
print(cleaned_table)

# Find the PI that has the most number of minterms:
def max_coverage(original_table):
    table = copy.deepcopy(original_table)
    final = []
    coverage = [len(value) for value in pi_table.values()]
    maximum_coverage = [i for i in range(len(coverage)) if coverage[i] == max(coverage)]
    final = [list(table.keys())[i] for i in maximum_coverage]
    return final

# Find the PI with the least number of literals (PIs w/ minimum cost):
def min_cost(original_table):
    table = copy.deepcopy(original_table)
    cost = []
    final = []
    for key in table:
        count = key.count('-')
        cost.append(max_width - count)
    min_index = [i for i in range(len(cost)) if cost[i] == min(cost)]
    final = [table[k] for k in min_index]
    return final

print(f"initial PI table: {pi_table}") 
Final_EPI = []
temp_pi_table = {}
while(len(pi_table)) > 0:
    EPI = determine_EPI(pi_table)
    print(f"EPIs:\n{EPI}")
    if len(EPI) > 0:
        Final_EPI += EPI
        print(f"PIs chosen so far: {Final_EPI}")
        pi_table = clean_table(pi_table, EPI)
        pi_table = remove_empty_PIs(pi_table)
        draw_chart(pi_table)
    else:
        print(f"No EPIs found")
    # Maximum Coverage:
        if (len(pi_table))>0:
            print("Looking for the PI w/ maximum coverage:")
            PI_max_coverage = max_coverage(pi_table)
            print(f"PIs w/ maximum coverage:\n{PI_max_coverage}")
            # If there was a single PI that had the most coverage, pick it. (Else) If there were multiple PIs w/ the maximum coverages, priorotize the one with the minimum cost:
            if len(PI_max_coverage) == 1:
                Final_EPI += PI_max_coverage
                print(f"PIs chosen so far: {Final_EPI}")
                pi_table = clean_table(pi_table, PI_max_coverage)
                pi_table = remove_empty_PIs(pi_table)
                draw_chart(pi_table)
                # Putting else not to execute all if statements; we don't want to repeat this for every PI and get stuck in a loop
            else:
                # Minimum Cost:
                # The key is to find the minimum cost among the PIs with the maximum coverage, not all PIs:
                PI_min_cost = min_cost(PI_max_coverage)
                print(f"PIs w/ minimum cost:\n{PI_min_cost}")
                # If there was a single PI that had the minimum cost, pick it. (Else) If there were multiple PIs w/ the minimum cost, pick the first one:
                if len(PI_min_cost) == 1:
                    Final_EPI += PI_min_cost
                    print(f"PIs chosen so far: {Final_EPI}")
                    temp_pi_table = clean_table(pi_table, PI_min_cost)
                    pi_table = remove_empty_PIs(temp_pi_table)
                    draw_chart(pi_table)
                    # Choosing the first PI that has both the maximum coverage and the minimum cost:
                else:
                    print("No single PI had the minimum cost. Choosing the first PI w/ the maximum coverage and minimum cost:")
                    Final_EPI+=[PI_min_cost[0]]
                    print(f"PIs chosen so far: {Final_EPI}")
                    temp_pi_table = clean_table(pi_table, [PI_min_cost[0]])
                    pi_table = remove_empty_PIs(temp_pi_table)
                draw_chart(pi_table)         
print(f"Final EPI list:")
print(Final_EPI)
draw_chart(pi_table)

def cost(lst):
    total_count = 0
    for string in lst:
        total_count += string.count('0') + string.count('1')
    return total_count

# Count zeros and ones
total_count = cost(Final_EPI)

# Output the result
print("Total cost:", total_count)

for index_j, j in enumerate(Final_EPI):
    if Min_or_Max == 1:
        result = ''
        alphabet_index = 0
        L = max_width
        for i in j:
            if i == '1':
                result += chr(ord('a') + alphabet_index)
                alphabet_index += 1
            elif i == '0':
                result += chr(ord('a') + alphabet_index) + "'"
                alphabet_index += 1
            else:
                alphabet_index += 1
        if index_j == len(Final_EPI) - 1:
            print(result, end=' ')
        else:
            print(result, end=' + ')
            
    elif Min_or_Max == 2:
        result = ''
        alphabet_index = 0
        L = max_width
        for i in j:
            if i == '1':
                result += chr(ord('A') + alphabet_index) + "'+"
                alphabet_index += 1
            elif i == '0':
                result += chr(ord('A') + alphabet_index) + "+"
                alphabet_index += 1
            else:
                alphabet_index += 1
        result = result[:-1]  # Remove the last '+' symbol
        if index_j == len(Final_EPI) - 1:
            print(result, end=' ')
        else:
            print(result, end=' . ')
