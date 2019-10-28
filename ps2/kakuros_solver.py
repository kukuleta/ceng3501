from ortools.sat.python import cp_model

def Kakuros_Solver(sum_constraints):
    Cp_Model = cp_model.CpModel()
    Cp_Solver = cp_model.CpSolver()

    tableDomainConstraints = [[],[],[]]
    for row in tableDomainConstraints:
        for column in range(3):
            row.append(Cp_Model.NewIntVar(1,9,"Cell-{column}-{row}".format(column=column,row=row)))

    for row_group in tableDomainConstraints:
        total_row_value = 0
        row_index = 0
        for row_item in row_group:
            total_row_value+=row_item
        Cp_Model.AddAllDifferent(row_group)
        Cp_Model.Add(total_row_value = sum_constraits[row_index + 3])
        row_index = row_index + 1

    columns_straightforward = [tableDomainConstraints[column][row] for column in range(2) for row in range(2)]
    columns = [[columns_straightforward[0:3]],[columns_straightforward[3:6]],columns_straightforward[6:9]]

    for column_group in columns:
        total_column_value = 0
        column_index = 0
        for column_item in column_group:
            total_column_value += column_item
        Cp_Model.AddAllDifferent(column_group)
        Cp_Model.Add(total_row_value=sum_constraits[column_index])
        column_index = column_index + 1

    status = Cp_Solver.Solve(Cp_Model)
    if status == cp_model.FEASIBLE:
        kakurosOutputFile = open("kakuro_output.txt", 'w')
        kakurosOutputFile.writelines("x" + "," + str(sum_constraints[0]) + "," +
                                     str(sum_constraints[1]) + "," + str(sum_constraints[2]) + "\n")
        for row_group in tableDomainConstraints:
            row_constraint_index = 0
            kakurosOutputFile.writelines(str(sum_constraints[row_constraint_index + 3]) + "," +
                                         str(Cp_Solver.Value(row_group[0])) + "," + str(Cp_Solver.Value(row_group[1])) + "," + str(
                    Cp_Solver.Value(row_group[2])) + "\n")


kakurosInput = open("kakuros_input.txt", 'r')
lines = kakurosInput.readlines()
sum_constraits = []
for i in lines:
    linesSplitted = i.strip().split(",")
    for x in linesSplitted:
        sum.append(x)
kakurosInput.close()

kakurosOutputFile = open("kakuro_output.txt", 'w')
Kakuros_Solver(sum)