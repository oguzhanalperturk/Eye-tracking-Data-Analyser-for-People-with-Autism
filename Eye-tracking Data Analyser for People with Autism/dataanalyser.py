import string
import copy
import matplotlib.pyplot as plt
import sys

# We used this function for reading the data from file
def readFile(filename):
    try:
        file = open(filename, "r")
    except:
        print("Error happened in opening the file")
        exit(1)

    records = file.readlines()
    file.close()
    return records


# We used this function for creating grid according to the given image and grid size.
def createGrid(sizeOfImage, gridSegmentation):
    sizeOfImage = sizeOfImage.split("x")
    gridSegmentation = gridSegmentation.split("x")
    gridList = []
    increaseAmount_x = int(sizeOfImage[0]) / int(gridSegmentation[1])
    increaseAmount_y = int(sizeOfImage[1]) / int(gridSegmentation[0])
    increaseAmount_x = int(increaseAmount_x)
    increaseAmount_y = int(increaseAmount_y)
    x = -increaseAmount_x
    y = -increaseAmount_y
    for i in range(int(gridSegmentation[1]) + 1):
        templist = []
        x += increaseAmount_x
        y = -increaseAmount_y
        for j in range(int(gridSegmentation[0]) + 1):
            y += increaseAmount_y
            position = [x, y]
            templist.append(position)
        gridList.append(templist)

    templist = []
    newlist = []
    letters = list(string.ascii_uppercase)
    letter_count = 0
    x = 0
    y = 0
    count = 0
    loop_count = 0
    while (loop_count < int(gridSegmentation[0]) * int(gridSegmentation[1])):
        if (y == int(gridSegmentation[1])):
            y = 0
        if (count % int(gridSegmentation[1]) == 0 and count != 0):
            x += 1
        templist = [gridList[y][x], gridList[y][x + 1], gridList[y + 1][x], gridList[y + 1][x + 1]]
        newlist.append(templist)
        count += 1
        y += 1
        loop_count += 1
        templist.append(letters[letter_count])
        letter_count += 1

    return newlist


# We used this function for reading data from file and place the data of each people in a list.
def getPeopleInfoList(filename):
    filecontent = readFile(filename)
    filecontent.pop(0)
    peopleList = []
    count = 0
    people = []
    for i in filecontent:
        count += 1
        temp = i.split(",")
        temp[3] = temp[3].replace("\n", "")
        temp_insert = [temp[1], temp[2], temp[3]]
        if (temp[0] == "0"):
            people = []
            peopleList.append(people)
        people.append(temp_insert)

    return peopleList


# We used this function for detecting the grid letter of given position
def detectGrid(grid, position):
    position = position.split("x")
    position[0] = int(position[0])
    position[1] = int(position[1])
    for i in grid:
        if (position[1] >= i[0][1] and position[1] <= i[1][1]):
            if (position[0] >= i[0][0] and position[0] <= i[2][0]):
                return i[4]


# We used this function for creating an empty dictionary in needed format
def createDictionary(grid):
    letters = list(string.ascii_uppercase)
    last_letter = grid[-1][4]
    grid_letters = []
    for i in letters:
        if (i == last_letter):
            grid_letters.append(i)
            break
        grid_letters.append(i)
    info_dict = {"Total number of people": 0, "Total time viewed": 0, "Total number of fixations": 0}
    grid_letters = {i: {"ASD": copy.deepcopy(info_dict), "CONTROL": copy.deepcopy(info_dict)} for i in grid_letters}

    return grid_letters


# We used this function for placing all data into the empty dictionary
def createStatistics(data_dict, position_list,grid,people_info):
    people_grid_letters = []
    for i in position_list:
        temp = []
        for j in i:
            position_str = j[0] + "x" + j[1]
            letter = detectGrid(grid,position_str)
            temp.append([letter,j[2]])
        people_grid_letters.append(temp)

    letters = list(string.ascii_uppercase)
    last_letter = grid[-1][4]
    grid_letters = []
    for i in letters:
        if (i == last_letter):
            grid_letters.append(i)
            break
        grid_letters.append(i)

    for i in people_grid_letters:
        letter_flag_dict = {i: 0 for i in grid_letters}
        for j in i:
            data_dict[j[0]][people_info]['Total number of fixations'] += 1
            data_dict[j[0]][people_info]['Total time viewed'] += int(j[1])
            if(letter_flag_dict[j[0]] == 0):
                data_dict[j[0]][people_info]['Total number of people'] += 1
                letter_flag_dict[j[0]] += 1




# Create grid
grid = createGrid(sys.argv[3], sys.argv[4])

# Get autism positions list
autism_positions = getPeopleInfoList(sys.argv[1])
# Get control positions list
control_positions = getPeopleInfoList(sys.argv[2])

# empty dictionary in needed format
data_dict = createDictionary(grid)

# Fill the dictionary with data from asd.txt file
createStatistics(data_dict, autism_positions,grid, "ASD")
# Fill the dictionary with data from control.txt file
createStatistics(data_dict, control_positions,grid, "CONTROL")


while True:
    print("")
    print("1. Compare the total number of people,the total time viewed, and the total number of fixations for people with and without autism for a particular element on an image ")
    print("2. Compare the total number of people, the total time viewed, and the total number of fixations for people with and without autism on an image")
    print("3. Exit")
    command = input("Enter the command: ")
    print("")

    if(command == '1'):
        print("1. Total number of people")
        print("2. Total time viewed")
        print("3. Total number of fixations")
        metric = input("Choose a metric: ")

        if(metric == '1'):
            metric = "Total number of people"

        elif(metric == '2'):
            metric = "Total time viewed"

        elif (metric == '3'):
            metric = "Total number of fixations"


        for i in data_dict:
            print(i)

        print("")

        # While loop for checking improper letter inputs
        while True:
            element = input("Select an element from above: ")
            if (element in data_dict):
                break
            print("Please select an element from above!")


        groups = ["People with Autism", "People Without Autism"]
        values = [data_dict[element]['ASD'][metric], data_dict[element]['CONTROL'][metric]]
        plt.bar(groups, values)
        plt.xlabel('Groups')
        plt.ylabel(metric)
        plt.title('Comparison Between People With & Without Autism for Element '+element)
        plt.show()


    elif command == '2':
        print("1. Total number of people")
        print("2. Total time viewed")
        print("3. Total number of fixations")
        metric = input("Choose a metric: ")

        if (metric == '1'):
            metric = "Total number of people"

        elif (metric == '2'):
            metric = "Total time viewed"

        elif (metric == '3'):
            metric = "Total number of fixations"


        # Sum of the entered metric
        autism_sum = 0
        control_sum = 0
        for i in data_dict:
            autism_sum += data_dict[i]['ASD'][metric]
            control_sum += data_dict[i]['CONTROL'][metric]

        groups = ["People with Autism", "People Without Autism"]
        values = [autism_sum, control_sum]
        plt.bar(groups, values)
        plt.xlabel('Groups')
        plt.ylabel(metric)
        plt.title('Comparison Between People With & Without Autism for an image')
        plt.show()


    elif command == '3':
        break

    else:
        print("Please enter proper command!")