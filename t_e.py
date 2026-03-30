# Python script for technical excersize 1 
import csv
import warnings
import logging

# import numpy as np
import pandas as pd

# Global parameter for currently acknowleged origins, to be updated in the future
errArr = {"C": [0], 
          "T": [0], 
          "D": [0], 
          "N": [0]}
errDf = pd.DataFrame(data=errArr)

def main():
    # As we dont have a standard path, require manual input to file name 
    # fName = input("Please prove full input path to the desired csv file: ")
    fName = "samples.txt"

    # Boolean for saving dataframe to csv
    isSure = input('Do you want to save percentage of failed samples as csv? (y/n): ').lower().startswith('y')

    # Open csv file using csv reader
    with open(fName, mode="r") as inF:
        csv_reader = csv.reader(inF)
         # Read in header row separately
        header = next(csv_reader, None)
        # Iterate over each row in the CSV file

        rCount = 0 
        for row in csv_reader: 
            row = list(row)
            # Get Sample name
            sName = row[0]
            sOri = list(sName)
            sOri = sOri[1]
            # Get Percentage of the bases in the consensus
            # percN = row[1]
            # Get Percentage of the bases of the reference genome covered 
            percCov = row[2]
            # Get longest sequence in consensus
            # maxRun = row[3]
            # Get number of read aligned to reference genome
            # noAln = row[4]
            # Get boolean if seuence passes quality filter
            qualBool = row[5]

            rCount+=1
            # If coverage belov 95%, or quality boolean is set as false, add to counter 
            if float(percCov) < 95.00 or qualBool == "FALSE": 
                # If we do not have the origin in our error dataframe, 
                # print origin name, add new column to dataframe
                if not sOri in errDf.columns.values.tolist():
                    print("Error: Origin:", sOri, "not currently covered in script, adding it to output dataframe")
                    errDf.insert(1, sOri, [0])
                errDf[sOri]+=1
    
    # Check if any of the origins have more then 10% failed samples (i.e. if more then 10% of rows )
    percDf = errDf/rCount

    # Raise warnings for each origin that has over 10% failed samples
    for ori in percDf.columns.values.tolist():
        if percDf[ori][0] > 10:
            warnings.warn("Origin:", ori, "has over 10 percent failed samples!")

    if(isSure):
        # Save percentage dataframe for each failed origin as a csv
        percDf.to_csv("Failed_Origins.csv", 
                  encoding="utf-8", 
                  index=False)

if __name__ == "__main__":
    main()