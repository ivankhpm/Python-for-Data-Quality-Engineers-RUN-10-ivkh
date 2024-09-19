import random as r

#1 create list of 100 random numbers from 0 to 1000
randomlist = r.sample(range(0, 1000), 100)


#2 sort list from min to max (without using sort())
### empty list to store results
new_list = []

###while loop to find min value
while randomlist:
    minimum = randomlist[0]
    for x in randomlist:
        if x < minimum:
            minimum = x
    new_list.append(minimum)
    randomlist.remove(minimum)
##print(new_list)

#3 calculate average for even and odd numbers
### empty list to store values
ev_li = []
od_li = []

### for loop to check even or odd
for i in new_list:
    if (i % 2 == 0):
        ev_li.append(i)
    else:
        od_li.append(i)
### calc averages
avg_ev = sum(ev_li) / len(ev_li)
avg_od = sum(od_li) / len(od_li)

## print averages
print("Even lists average: ", avg_ev)
print("Odd lists average: ", avg_od)