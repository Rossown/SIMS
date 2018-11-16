import os

def load(filename, password):
    itemList = []
    if not os.path.exists("csv"):
        return False
    with open("csv/"+filename+".csv", "r") as file:
        next(file)
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

def save(filename, list, password):
    if not os.path.exists("csv"):
        os.makedirs("csv")
    with open("csv/"+filename+".csv", "w+") as file:
        file.write(password+"\n")
        for item in list:
            file.write(format("%s,%s,%s,%s,%s,%s\n"%(
                item['id'],
                item["name"],
                item["price"],
                item["weight"],
                item["color"],
                item["quantity"]
            )))

def checkLogin(filename, password):
    if not os.path.exists("csv/"+filename+".csv"):
        return True
    with open("csv/"+filename+".csv", "r") as file:
        return password.strip() == file.readline().strip()