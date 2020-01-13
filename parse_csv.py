import csv

cropTypeMapping = {
    "inter" : "1",
    "main" : "2"
}

cropHarvestMapping = {
    "single" : "1",
    "multiple" : "2"
}

def parseProduct(row):
    productCode = row[0]
    # dropdown
    cropType = cropTypeMapping[row[1].strip().lower()]
    cropVariety = row[2]
    cropArea = row[3]
    cropSeason = row[4]
    cropHarvest = cropHarvestMapping[row[5].strip().lower()]
    # dropdown
    expectedYield = row[6]

    return {
        "productCode" : productCode,
        "cropType" : cropType,
        "cropVariety" : cropVariety,
        "cropArea" : cropArea,
        "cropSeason" : cropSeason,
        "cropHarvest" : cropHarvest,
        "expectedYield" : expectedYield
    }

def parseData():

    with open('data.csv') as csvfile:
        reader = csv.reader(csvfile)
        # skip the header
        next(reader, None)
        # parse each row 
        data = {}
        for row in reader:
            registrationNum = row[1]
            products = []
            for index in range(3,60,8):
                product = parseProduct(row[index : index + 7])
                products.append(product)
            
            data[registrationNum] = products

    
    return data
        
