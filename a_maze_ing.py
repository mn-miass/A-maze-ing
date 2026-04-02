from  parsing import FileHandler


#the first part must include reading arguments



file = FileHandler("config.txt")

functions = [file.FileCheck(),
             file.IsEmpty(),
            file.GetData(),
            file.CheckData(),
            file.DataIsValid()]

for function in functions:
    if file.valid == True:
        function

print(file.valid)