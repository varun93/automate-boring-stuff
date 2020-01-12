import csv

def parseProduct(row):
    productCode = row[0]
    # dropdown
    cropType = row[1]
    cropVariety = row[2]
    cropArea = row[3]
    cropSeason = row[4]
    cropHarvest = row[5]
    # dropdown
    expectedYield = row[6]

    return {
        "productCode" : productCode,
        "cropType" : cropType,
        "cropVariety" : cropVariety,
        "cropArea" : cropArea,
        "cropSeason" : cropSeason,
        "cropHarvest" : cropHarvest
    }

with open('data.csv') as csvfile:
    reader = csv.reader(csvfile)
    # skip the header
    next(reader, None)
    # parse each row 
    for row in reader:
        registrationNum = row[1]
        for index in range(3,60,8):
            product = parseProduct(row[index : index + 7])
            print(product)

        # print(row[3:10])
        # print(row[11:18])
        # print(row[19:26])
        # print(row[27:34])
        # print(row[35:42])
        # print(row[43:50])
        # print(row[51:58])
        # print(row[59:66])