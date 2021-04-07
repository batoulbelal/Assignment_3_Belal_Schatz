# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy
import csv
import random
import string


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hello, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def readFromCSVfile():
#comment: from https://www.youtube.com/watch?v=efSjcrp87OY
# --------------------------------------------------
#comment: this function reads the data from the CSV file

#return: it returns a list; which contains the data from the CSV file in ghe following format
#e.g. ['0.348265448', '0.269011835']
#--------------------------------------------------

    with open('input.csv') as file:
        bufferedList = []
#comment: the delimeter tells me which symbol separates the lines
        reader = csv.reader(file, delimiter=';')
        count =0;
        for row in reader:
            #print(row)
            bufferedText = str(row.copy());
#comment: the next code line does convert the ',' into a '.' -> always after a 0
#comment: not all , can be replaced by a . because -> ['0.348265448'->,<- '0.269011835'] the comme in between would also be changed
#comment: this can be changed to like '1,' to '1.' and this for all numbers from 0 to 9
#comment: converting ',' to '.' is necessary to allow parsing into float
            textCommaConvertToDot = bufferedText.replace("0,", "0.")

            #print(textCommaConvertToDot)

            bufferedList.append(textCommaConvertToDot)
            if count > 100:
                break
            count +=1;

    return bufferedList;

def splitInputFromCSVFile(numberOfRow):
# split strings taken from https://www.w3schools.com/python/ref_string_split.asp
#----------------------------------------------------
#comment: function splits the input from the CSV file according to the split symbol " ' "
#return: return the stringList of the split strings
#----------------------------------------------------

    splitCSVInput = []

    buffText = str(dataFromCSVFile[numberOfRow]);
    splitText = buffText.split("'");
    splitCSVInput.append((str(splitText)));

    return splitText;

def createArrayOfInputValues(numberOfColumnsFromInputData, numberOfRowsFromInputData):
#-----------------------------------------------------------
#this function creates an array of the input data points (excluding the first lines with the information)
#return: it returns an array that contains the read data points from the CSV file
#-----------------------------------------------------------

#comment: creates an initial array filled with zeroes in the dimension an rows according to the chosen values
    bufferedArray = numpy.zeros((numberOfRowsFromInputData, numberOfColumnsFromInputData), dtype='float');

#comment: i think this code line is obsolete
    bufferedList = splitInputFromCSVFile(3);


    for currentRow in range (0,numberOfRowsFromInputData):
#comment: the location for output 1 helps with splitting the string because
#comment: the number is only at odd indexes e.g. 1,3,5,7 (at the other indexes, there are symbols such as '[' or ','
        locationForOutput = 1;
#comment: the 2 in the next line comes from the fact that the line where the data set in the CSV starts is the third one (index 2)
        bufferedText = splitInputFromCSVFile(2+currentRow);
        for currentColumn in range (0,numberOfColumnsFromInputData):
            bufferedArray[currentRow][currentColumn] = bufferedText[locationForOutput]
#comment: the next line makes the location for output = 1,3,5,7, etc.
            locationForOutput += 2;

    return bufferedArray;

def manhattanDistance(A, B):
#comment: from https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cityblock.html
#comment: taken from https://www.geeksforgeeks.org/python-calculate-city-block-distance/
#comment: the function calculated the manhattan distance

#----------------------------------------------------
#comment: the function calculates the manhattan distance of 2 data points A and B; A and B in the form of
#return: it returns the distance as an integer / float
#----------------------------------------------------

    result = numpy.sum([abs(a - b) for (a, b) in zip(A, B)])
    return result

def kMeansClusteringProcess(numberOfClusters, numberOfRowsFromInputData, numberOfColumnsFromInputData, arrayDataPointsFromCSVFile):
# ----------------------------------------------------
#comment: the function performs the whole clustering process including: allocation of 3 random centroids withih the range of (xmin,xmax; ymin,ymax; zmin,zmax)
#comment: further it performs the calculation of the manhattan distance (included in array vectorManhattanDistance)
#comment: also, it stores which item of the CSV data array belongs to which cluster (stored in matrixDataBelongsToWhichCLuster)
#comment: the matrixClusterInformation contains the cluster number and the centroid locations (x,y,z)

#return: void (nothing so far)

# ----------------------------------------------------
    matrixPositionOfClusterCentroids = numpy.zeros((int(numberOfClusters), int(numberOfColumnsFromInputData)), dtype='float') # man muss hier nur entsprechend eine matrix ersteleln, die mir x/y coordinaten der cluster speichert

#comment: the array is copied to avoid changes
    copiedArrayContainingDotsDataFromFile = arrayDataPointsFromCSVFile.copy();

#comment: initial 'global' variables in the function
    minimumValueX=0;
    maximumValueX=0;
    minimumValueY=0;
    maximumValueY=0;
    minimumValueZ=0;
    maximumValueZ=0;

#comment: this loop fills goes through every columns of the dataset array and determines the minimum and maximum value
#comment: of the dimensions (depending if there is 1,2 or 3 dimensions)

    for currentColumn in range (0,int(numberOfColumnsFromInputData)):
        minimumValueColumn = min(copiedArrayContainingDotsDataFromFile[:,currentColumn])
        maximumValueColumn = max(copiedArrayContainingDotsDataFromFile[:,currentColumn])
        # mit dem unten stehenden code sind alle fälle abgedeckt
        if currentColumn == 0:
            minimumValueX = minimumValueColumn;
            maximumValueX = maximumValueColumn;

        if currentColumn == 1:
            minimumValueY = minimumValueColumn;
            maximumValueY = maximumValueColumn;

        if currentColumn == 2:
            minimumValueZ = minimumValueColumn;
            maximumValueZ = maximumValueColumn;



#comment: matrix cluster information has the following appearance
#comment: there are x columns (depending on number of dimensions)
#comment: and x rows (depending on the number of clusters)
#comment: appearance (see line below)
#comment: [clusterNumber] [centroidXCoordinat] [centroidYCoordinate] [centroidZCoordinate]
    matrixClusterInformation = numpy.zeros((int(numberOfClusters),(1+int(numberOfColumnsFromInputData))), dtype='float') # the first dimension is for the cluster number; die erste +1 ist für die linkeste spalte, weil cluster nummer; d

#comment: the loop below fills out the [clusterNumber] column with the numbers from 1 to 3 automatically
    for actualRow in range (0,int(numberOfClusters)):
        matrixClusterInformation[actualRow,0]=1+actualRow;

    #print(numberOfColumnsFromInputData)


#comment: the next if blocks do the following:
#comment: depending on how many columns/dimensions there are; random starting location in between the x/y/z limits are created and inserted
#comment: into the matrixClusterInformation-Array
    if int(numberOfColumnsFromInputData)==1:
        for row in range (0,int(numberOfClusters)):
            matrixClusterInformation[row,1]= random.uniform(minimumValueX,maximumValueX)

    if int(numberOfColumnsFromInputData) == 2:
        print("hüpft er rein?")
        for row in range (0,int(numberOfClusters)):
            matrixClusterInformation[row,1]= random.uniform(minimumValueX,maximumValueX)
        for row in range (0,int(numberOfClusters)):
            matrixClusterInformation[row,2]= random.uniform(minimumValueY,maximumValueY)

    if int(numberOfColumnsFromInputData) ==3:
        for row in range (0,int(numberOfClusters)):
            matrixClusterInformation[row,1]= random.uniform(minimumValueX,maximumValueX)
        for row in range (0,int(numberOfClusters)):
            matrixClusterInformation[row,2]= random.uniform(minimumValueY,maximumValueY)
        for row in range(0, int(numberOfClusters)):
            matrixClusterInformation[row, 3] = random.uniform(minimumValueZ, maximumValueZ)

    #print(matrixClusterInformation)

#comment: the vectorManhattanDistance array contains 1/2/3 (depending on dimensions) columns where the distance from each
#comment: data point / line from CSV file (=row) is calculated for every cluster centroid (=column)
#comment: appearance see below:
# [element1DistanceToCentroidCluster1] [element1DistanceToCentroidCluster2] [element1DistanceToCentroidCluster3]
# [element2DistanceToCentroidCluster1] [element2DistanceToCentroidCluster2] [element2DistanceToCentroidCluster3]
# and so on
    vectorManhattanDistance = numpy.zeros((int(numberOfRowsFromInputData),int(numberOfClusters)), dtype='float')

#comments: the following loops calculate the distance with the manhattanDistance-Function
    for counterVariable in range (0,int(numberOfRowsFromInputData)):

#comment: the [counterVariable, 0] equals the column 0 (the leftmost) and so on for the other loops
#comment: matrixClusterInformation[0, 1:3] -> this takes the centroid x/y/z from the matrixClusterInformation-Array
#comment: arrayDataPointsFromCSVFile[counterVariable] gets the [x,y,z] from the read in CSV file

        vectorManhattanDistance[counterVariable,0]=manhattanDistance(arrayDataPointsFromCSVFile[counterVariable], matrixClusterInformation[0, 1:3])

#comment: loop for cluster 2
    for counterVariable in range(0, int(numberOfRowsFromInputData)):
        vectorManhattanDistance[counterVariable, 1] = manhattanDistance(arrayDataPointsFromCSVFile[counterVariable], matrixClusterInformation[1, 1:3])

#comment: loop for cluster 3
    for counterVariable in range(0, int(numberOfRowsFromInputData)):
        vectorManhattanDistance[counterVariable, 2] = manhattanDistance(arrayDataPointsFromCSVFile[counterVariable], matrixClusterInformation[2, 1:3])


#comment: matrixDataItemBelongsToWhichCluster contains the information which item / line of CSV belongs to which cluster
#appearance
# [ClusterElement1] = e.g. 1
#[ClusterElement2] = 2
#[ClusterElement3] =1
# and so on
    matrixDataItemBelongsToWhichCluster= numpy.zeros((int(numberOfRowsFromInputData),1),dtype='float')

    for rowCounter in range (0,int(numberOfRowsFromInputData)):
        #print(vectorManhattanDistance[rowCounter, 0])
        #print(vectorManhattanDistance[rowCounter, 1])
        #print(vectorManhattanDistance[rowCounter, 2])
        #print("-------")

#comment: error handling should be implemented; if 3 dimension, it should be until [rowCounter, 4]
#comment: the if statements check e.g.
#comment: if [manhDistanceCluster 1 < manhDistanceCluster 2] & [manhDistanceCluster 1 < manhDistanceCluster 3] then it belongs to cluster 1
#comment: the element belongs to the cluster where the manhattan distance is the smallest value

        if (vectorManhattanDistance[rowCounter,0] < vectorManhattanDistance[rowCounter,1]) & (vectorManhattanDistance [rowCounter,0] < vectorManhattanDistance[rowCounter,2]):
            matrixDataItemBelongsToWhichCluster[rowCounter,0] = 1;

        if (vectorManhattanDistance[rowCounter,1] < vectorManhattanDistance[rowCounter,0]) & (vectorManhattanDistance[rowCounter,1]<vectorManhattanDistance[rowCounter,2]):
            matrixDataItemBelongsToWhichCluster[rowCounter,0] = 2;

        if (vectorManhattanDistance[rowCounter,2] < vectorManhattanDistance[rowCounter,0]) & (vectorManhattanDistance[rowCounter,2]<vectorManhattanDistance[rowCounter,1]):
            matrixDataItemBelongsToWhichCluster[rowCounter,0] = 3;

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    print("- From the DATA-Set -")
    dataFromCSVFile = readFromCSVfile();

    print("- Split first line -")
    # comment: this code line splits the first read in line to extract the number of clusters
    bufferedSplitText = splitInputFromCSVFile(0);  # von row index 0
    print(bufferedSplitText)

    # comment: this line occurs to be '['[', 'ï»¿3', ', ', '', ']']' -> to get rid of the symbols
    # comment: therefore the 4th element (index 3) of the whole secodn element (index 1) of the list is chosen (=workaround)
    numberOfClusters = bufferedSplitText[1][3]
    # print("CLUSTERS")
    # print(numberOfClusters)

    # comment: the next block takes the second line of the CSV file and extracts the number of rows from the second line (index 1)
    bufferedSplitText = splitInputFromCSVFile(1);
    # comment: the bufferedSplitText[1] has the index 1 because the element [0] equals '['
    numberOfRows = bufferedSplitText[1]
    print("- Number of ROWS -")
    print(numberOfRows)

    # comment: the next block extracts the number of Columns / dimensions from the second line of the CSV file (index 1)
    bufferedSplitText = splitInputFromCSVFile(1);
    # comment: the index must be 3 because [0]='[', [1]='(rows)', [2]=',' [3]='(columns)'
    numberOfDimensions = bufferedSplitText[3];
    # print(numberOfDimensions)

    # comment: the array matrixContainingDataFromCSVFile includes ONLY the data points from the CSV file
    # comment: the first 2 lines of the CSV file which contain inf. about cluster / rows / etc are not part of this array
    # comment: parsing to int is necessary because it reads in a string and since dimensions and rows can just be whole numbers, int is feasible to be used
    matrixContainingDataFromCSVFile = createArrayOfInputValues(int(numberOfDimensions), int(numberOfRows)).copy();
    # comment: copying the array with .copy() is necessary because otherwise it does not work and the array is left with zeros

    print('- DATA FROM THE CSV FILE -')
    print(matrixContainingDataFromCSVFile)

    kMeansClusteringProcess(numberOfClusters, numberOfRows, numberOfDimensions, matrixContainingDataFromCSVFile);

# replace function from https://www.w3schools.com/python/ref_string_replace.asp

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
