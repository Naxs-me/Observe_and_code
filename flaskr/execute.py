import nbformat as nbf
import copy
import linecache

nb = nbf.read("./result.ipynb", 4)

history = []
lineCount = []
stackCounter = 0

code = '''from sys import settrace
import inspect
import pickle
with open("stack.txt", "rb") as fp:
    stack = pickle.load(fp)

# stack.append(stack[-1])
# for k in stack:
#     print(k)
currline = 0
history = [None]*len(lineCount)

def my_tracer(frame, event, arg=None):
    global currline
    global lineCount
    global stackCounter
    code = frame.f_code
    func_name = code.co_name
    if func_name == 'encode' or func_name == 'main' or func_name[0] == "<":
        return
    line_no = frame.f_lineno
    
    if event == 'line':
        print(lineCount)
        print("currline", currline)
        if line_no in lineCount:
            # lineCount = lineCount[1:]
            # print("entered",line_no,lineCount)
            currline = lineCount.index(line_no)
            print(line_no, currline)
        else:
            print("exited")
            return
        new_variables = inspect.stack()[1][0].f_locals
        if(list(stack[stackCounter].values())[0] == new_variables):
            # print(stack[currline])
            # print(new_variables)
            # print("match")

            history[currline] = "match"
        else:
            # print(stack[currline])
            # print(new_variables)
            # print("not match")
            history[currline] = str(list(stack[stackCounter].values())[0]) + " != " + str(new_variables) + str(line_no)
            # print(list(stack[currline].items))
            print("line no", line_no)
        stackCounter +=1

    return my_tracer

settrace(my_tracer)

def fun():
'''
for cell in nb["cells"]:
    if cell['cell_type'] == 'code':
        temp = cell['source'].split('\n')
        for l in temp:
            if l != '':
                code += " "*4 + l + "\n"
        lineCount.append(code.count("\n"))
        # print("temp")
        # print(temp,lineCount)
# print("line count",lineCount)
lineCount = lineCount[1:]

code += "\nfun()\nsettrace(None)\n"
print(code)
exec(code)

k = 0
for i in range(len(nb["cells"])-1):
    if nb["cells"][i]['cell_type'] == 'code':
        print(i)
        nb["cells"].insert(i+1, nbf.v4.new_markdown_cell(history[k]))
        k += 1
# print("break")
# for k in history:
#     print(k)

nbf.write(nb, 'output.ipynb')
