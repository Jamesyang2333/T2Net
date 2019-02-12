import os
indir =
in_dir = os.path.join(os.getcwd(), args.indir)
    out_dir = os.path.join(os.getcwd(), args.outdir)

    if not os.access(out_dir, os.F_OK):
        os.mkdir(out_dir)

    pathList = []
    dirList = []
    with open(in_dir, 'r') as input:
        for line in input:
            if line.strip():
                dirList.append(os.path.join(os.getcwd(), line.strip()))

    for dir in dirList:
        fileList = os.listdir(dir)
        for current in fileList:
            completePath = os.path.join(dir, current)
            if is_image(completePath):
                pathList.append(completePath)

    random.shuffle(pathList)
    testSize = int(len(pathList) * float(args.ratio))
    testList = pathList[0: testSize]
    trainList = pathList[testSize:]
    with open(os.path.join(out_dir, args.nameOfDataset + ".txt"), 'w') as allFile:
        for path in pathList:
            allFile.write(path + "\n")
        allFile.close()

    with open(os.path.join(out_dir, args.nameOfDataset + "_train.txt"), 'w') as trainFile:
        for path in trainList:
            trainFile.write(path + "\n")
        trainFile.close()

    with open(os.path.join(out_dir, args.nameOfDataset + "_test.txt"), 'w') as testFile:
        for path in trainList:
            testFile.write(path + "\n")
        testFile.close()
    print("The dataset has been splited into " + str(len(pathList) - testSize) + " training images and " + str(testSize) + " test images")

