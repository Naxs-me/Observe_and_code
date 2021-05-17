from sys import settrace
import inspect
import pickle
import nbformat as nbf
import copy
import linecache

nb = nbf.read("./astIPYNB.ipynb", 4)
stack = []
with open("dump.txt", "rb") as fp:
    lineNo = pickle.load(fp)
with open("visited.txt", "rb") as fp:
    visited = pickle.load(fp)

searchLinoNo = list(zip(*lineNo[::-1]))
searchLinoNo = [list(searchLinoNo[0]),list(searchLinoNo[1])]
searchLinoNo[0].reverse()
searchLinoNo[1].reverse()
print(searchLinoNo)
execTrace = []
# print(nb['cells'][0])

# stack.append(stack[-1])
currline = 0
history = []
current_variables = {}


def my_tracer(frame, event, arg=None):
    global currline
    global current_variables
    global stack
    global execTrace
    global visited
    whitespace = "&nbsp;"*4
    code = frame.f_code
    func_name = code.co_name
    currInd = 0
    cellNo = 0
    if func_name == 'encode' or func_name == 'main' or func_name[0] == "<":
        return
    line_no = frame.f_lineno-124
    if line_no in searchLinoNo[0]:
        currInd = searchLinoNo[0].index(line_no)
        # print(currInd)
        line = linecache.getline("combine.py", line_no+124)
        # print("line %d: %s" % (line_no, line))
        execTrace.append(currInd)
        # currInd = searchLinoNo[0].index(line_no)
        # print("currind ",currInd)
    else:
        return
    

    if event == 'call':
        # print(currInd)
        # print("call lineno",line_no)
        call_entry = "Enter a function " + func_name + " with arguments"
        for j, k in frame.f_locals.items():
            call_entry += " " + str(j) + " -> " + str(k)
        cellNo = (currInd)*2
        # print(cellNo)
        # print(nb['cells'][cellNo]['source'])
        nb['cells'][cellNo]['source'] += call_entry + "\n\n"

    if event == 'line':
        new_variables = inspect.stack()[1][0].f_locals
        for var in new_variables:
            if var not in current_variables:
                text = "Introduce a variable :- " + \
                    var + " = " + str(new_variables[var])
                # if currLine == len(output):
                #     output.append([line_no, text])
                # else:
                #     output[currLine][1] = output[currLine][1] + \
                #         " -> " + str(new_variables[var])
                # print(currLine,output)
                cellNo = (execTrace[-2])*2
                # print("cellNo " ,cellNo)
                # if cellNo not in visited:
                nb['cells'][cellNo]['source'] += whitespace*lineNo[execTrace[-2]][1] + text + "\n\n"
                    # visited.append(cellNo)


                # nb['cells'].append(nbf.v4.new_markdown_cell(text))
                # nb['cells'].append(nbf.v4.new_code_cell())
                # currLine += 1
                # print("<div style=\"display:inline-block;width:50px;\"></div>", "<div style=\"display:inline-block;\">%s</div>" % (var + " = " + str(new_variables[var]) + " is introduced."),"<br>")

            else:
                if new_variables[var] != current_variables[var]:
                    # print("var ", var)
                    text = var + " = " + \
                        str(current_variables[var]) + \
                        " -> " + str(new_variables[var])
                    cellNo = (execTrace[-2])*2
                    # print("hello else", currInd)
                    # print("cellNo " ,cellNo)
                    # if cellNo not in visited:
                    nb['cells'][cellNo]['source'] += whitespace*lineNo[execTrace[-2]][1] + text + "\n\n"
                        # visited.append(cellNo)
                    # if currLine == len(output):
                    #     output.append([line_no, text])
                    # else:
                    #     output[currLine][1] = output[currLine][1] + \
                    #         " -> " + str(new_variables[var])
                    # nb['cells'].append(nbf.v4.new_markdown_cell(text))
                    # nb['cells'].append(nbf.v4.new_code_cell())
                    # currLine += 1
                    # print("<div style=\"display:inline-block;width:50px;\"></div>", "<div style=\"display:inline-block;\">%s</div>" % (var + " = " + str(current_variables[var]) + " -> " + str(new_variables[var])),"<br>")

        # curr_indent = 0
        # for c in curr_code:
        #     if c == " ":
        #         curr_indent += 1
        #     else:
        #         break

        current_variables = copy.deepcopy(new_variables)
        stack.append({copy.deepcopy((execTrace[-2])*2):copy.deepcopy(current_variables)})

    return my_tracer

settrace(my_tracer)
# <__code__insertion__>

settrace(None)
# print(history)
nbf.write(nb, 'result.ipynb')
with open("stack.txt", "wb") as fp:
    print("dump")
    pickle.dump(stack, fp)
    print("dumped")
with open("visited.txt", "wb") as fp:
    print("visited 1",visited)
    pickle.dump(visited, fp)