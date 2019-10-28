from ortools.sat.python import cp_model

def Futoshiki_Solver(constraints):
    Cp_Model = cp_model.CpModel()
    Cp_Solver = cp_model.CpSolver()

    tableDomainConstraints = [[],[],[],[]]
    column_letters = ["A","B","C","D"]
    for row in tableDomainConstraints:
        index = 0
        for letter in column_letters:
            row.append(Cp_Model.NewIntVar(1,4,"{letter}{index}".format(letter=letter,index=index)))
            index = index + 1

    columns_straightforward = [tableDomainConstraints[column][row] for column in range(4) for row in range(4)]
    columns = [[columns_straightforward[0:4]],[columns_straightforward[4:8]],
               columns_straightforward[8:12],columns_straightforward[12:16]]

    for column_group in columns:
        Cp_Model.AddAllDifferent(column_group)
    for row_group in tableDomainConstraints:
        Cp_Model.AddAllDifferent(row_group)

    for x in constraints:
        if (int(x[1]) > 0):
            Cp_Model.Add(eval(x[0]) == eval(x[1]))
        else:
            Cp_Model.Add(eval(x[0]) > eval(x[1]))

    status = Cp_Solver.Solve(Cp_Model)

    if status == cp_model.FEASIBLE:
        futoshikiOutput = open("futoshiki_output.txt", 'w')
        for row_group in tableDomainConstraints:
            futoshikiOutput.writelines(str(Cp_Solver.Value(row_group[0])) + "," +
                                       str(Cp_Solver.Value(row_group[1])) + "," +
                                       str(Cp_Solver.Value(row_group[2])) + "," +
                                       str(Cp_Solver.Value(row_group[3])) + "\n")


futoshikiInput = open("fitoshiki_input.txt", 'r')
lines = futoshikiInput.readlines()
linesplit = []
for i in lines:
    linesplit.append(i.strip().split(","))
futoshikiInput.close()

Futoshiki_Solver(constraints=linesplit)