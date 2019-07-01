import sys

costs = []
demands = []
drafts = []

def parse_file(fileName):
    with open(fileName, "r") as f:
        num_line = 1
        global n
        global costs
        global demands
        global drafts
        n = fileName.split("_")[0]
        n = n.replace("pcb", "")
        n = n.replace("bayg", "")
        n = n.replace("gr", "")
        n = n.replace("KroA", "")
        n = n.replace("ulysses", "")
        n = int(n)
        demands = []
        drafts = []

        lines = f.readlines()
        if fileName[:3] == "pcb" or fileName[:4] == 'KroA':
            costs = [[0] * int(n) for i in range(int(n))]
            for line in lines:
                if num_line >= 2 and num_line <= 1 + (int(n)):
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        costs[num_line-2][i] = (int(numeros[i]))
                if num_line == int(n) + 2:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 2):
                        demands.append(int(numeros[i]))
                if num_line == int(n) + 3:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        drafts.append(int(numeros[i]))
                num_line += 1
        else:
            costs = [[0] * int(n) for i in range(int(n))]
            for line in lines:
                if num_line >= 16 and num_line <= 16 + (int(n)-1):
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(int(n)):
                        costs[num_line-16][i] = (int(numeros[i]))
                if num_line == 16 + (int(n)-1) + 9:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        demands.append(int(numeros[i]))
                if num_line == 16 + (int(n)-1) + 12:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        drafts.append(int(numeros[i]))
                num_line += 1
    
    filename = fileName.split(".")[0]
    filename += "glpk.dat"
    with open(filename, "w") as f:
        f.write("data;\n")
        line = "set V:= "
        for i in range(1, n+1):
            line += str(i) + " "
        line += ";"
        f.write(line)
        f.write("\n")
        line = "param c:= \n"
        f.write(line)
        
        for i in range(0, n):
            for j in range(0, n):
                line = str(i+1) + " " + str(j+1) + " " + str(costs[i][j]) + "\n"
                f.write(line)
        f.write(";")
        f.write("\n")

        line = "param d := \n"
        f.write(line)
        for i in range(0,n):
            line = str(i+1) + " " + str(demands[i])
            f.write(line)
        f.write(";")

        f.write("\n")

        line = "param l := \n"
        f.write(line)
        for i in range(0,n):
            line = str(i+1) + " " + str(drafts[i])
            f.write(line)
        f.write(";")
        
        f.write("\n")
        f.write("end;")

if __name__ == '__main__':
    fileName = str(sys.argv[1])
