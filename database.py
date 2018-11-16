def load(filename, password):
    itemList = []
    with open("csv/"+filename+".csv", "r") as file:
        if password == file.readline():
            for line in file:
                line2 = line.split(",")
                itemList.append({
                    "name":line2[0],
                    "price":line2[1],
                    "weight":line2[2],
                    "color":line2[3],
                    "quantity":line2[4]
                })

def save(filename, list, password):
    with open("csv/"+filename+".csv", "w+") as file:
        file.write(password+"\n")
        for item in list:
            file.write(format("%s,%s,%s,%s,%s\n"%(
                item["name"],
                item["price"],
                item["weight"],
                item["color"],
                item["quantity"]
            )))