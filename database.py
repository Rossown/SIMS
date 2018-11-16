import os

def load(filename, password):
    itemList = []
    if not os.path.exists("csv/"+filename+".csv"):
        return False
    with open("csv/"+filename+".csv", "r") as file:
        next(file)
        for line in file:
            line2 = line.split(",")
            itemList.append({
                "name":line2[0],
                "price":line2[1],
                "weight":line2[2],
                "color":line2[3],
                "quantity":line2[4]
            })
    return itemList

def save(filename, list, password):
    if not os.path.exists("csv/"+filename+".csv"):
        os.makedirs("csv/"+filename+".csv")
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