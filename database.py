import os

#load function
def load(filename, password):
    #initialize item list
    itemList = []
    #make sure our csv folder exists
    if not os.path.exists("csv"):
        return False
    #attempt to open the corrosponding file
    with open("csv/"+filename+".csv", "r") as file:
        #skip password line
        next(file)
        #split each line by comma and add information to itemList as dict
        for line in file:
            line2 = line.split(",")
            itemList.append({
                "id":line2[0],
                "name":line2[1],
                "price":line2[2],
                "weight":line2[3],
                "color":line2[4],
                "quantity":line2[5]
            })
    return itemList

#save function
def save(filename, list, password):
    #verify csv exists
    if not os.path.exists("csv"):
        os.makedirs("csv")
    #open the corrosponding csv
    with open("csv/"+filename+".csv", "w+") as file:
        #write our password to csv
        file.write(password+"\n")
        #write each item to csv with commas separating info
        for item in list:
            file.write(format("%s,%s,%s,%s,%s,%s\n"%(
                item['id'],
                item["name"],
                item["price"],
                item["weight"],
                item["color"],
                item["quantity"]
            )))

#login verification
def checkLogin(filename, password):
    #if file does not exist, create a new file for the user with correct password
    if not os.path.exists("csv\\"+filename+".csv"):
        with open("csv\\"+filename+".csv", "w") as file:
            file.write(password)
        return True
    #if file exists, open it and verify password against first line
    with open("csv\\"+filename+".csv", "r") as file:
        return password.strip() == file.readline().strip()