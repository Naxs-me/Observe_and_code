import ast
import nbformat as nbf
import pickle

class MyVisitor(ast.NodeVisitor):
    def __init__(self, nb, lineNo):
        self.nb = nbf.v4.new_notebook()
        self.nb['cells'] = []
        self.lineNo = []
        
    def updateNode(self, node, depth, attributes=None):
        Type = ""
        whitespace = "&nbsp;"*4*(depth-2)
        if isinstance(node, ast.Call):
            Type = "Function called"
            text = whitespace + Type + ": "
            self.nb['cells'][-2]['source'] += text
        elif isinstance(node, ast.Name):
            if node.id == 'int':
                return
            if attributes == 'forTarget':
                self.nb['cells'][-2]['source'] += "with target variable: " + node.id + ' over: '
            elif attributes == 'forIter':
                self.nb['cells'][-2]['source'] += node.id
            elif attributes == 'arg_only':
                self.nb['cells'][-2]['source'] += node.id + '\n\n'
            else:
                self.nb['cells'][-2]['source'] += node.id + " with arguments "
                print("arguments added")
        elif isinstance(node, ast.Str):
            self.nb['cells'][-2]['source'] += "\"" + node.s + "\"" + " "
        else:
            Type = str(type(node))
            text = whitespace + Type + ": \n\n"
            self.nb['cells'][-2]['source'] += text

    def addNode(self,node, depth, attributes=None):
        Type = ""
        whitespace = "&nbsp;"*4*depth
        if isinstance(node, ast.FunctionDef):
            Type = 'Function Definition'
            text = whitespace + str(node.lineno) + " :" + Type + ": \n\n"
            self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            self.nb['cells'].append(nbf.v4.new_code_cell())
        elif isinstance(node, ast.Assign):
            if attributes == "Else":
                text = "&nbsp;"*4*(depth-1) + str(node.lineno-1) + " :" + "Else" + ": \n\n"
                text += whitespace + str(node.lineno) + " :" + "Assignment" + ": \n\n"
                self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            elif attributes == None:
                Type = 'Assignment'
                text = whitespace + str(node.lineno) + " :" + Type + ": \n\n"
                self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            self.nb['cells'].append(nbf.v4.new_code_cell())
        elif isinstance(node, ast.Expr):
            if attributes == "Else":
                Type = 'Else'
            elif attributes == None:
                Type = 'Expression'
            text = whitespace + str(node.lineno) + " :" + Type + ": \n\n"
            self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            self.nb['cells'].append(nbf.v4.new_code_cell())
        elif isinstance(node, ast.If):
            if attributes == "Elif":
                Type = 'Elif'
            elif attributes == None:
                Type = 'If'
            text = whitespace + str(node.lineno) + " :" + Type + ": \n\n"
            self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            self.nb['cells'].append(nbf.v4.new_code_cell())
        elif isinstance(node, ast.While):
            Type = 'While'
            text = whitespace + str(node.lineno) + " :" + Type + ": \n\n"
            self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            self.nb['cells'].append(nbf.v4.new_code_cell())
        elif isinstance(node, ast.For):
            Type = 'For'
            text = whitespace + str(node.lineno) + " :" + Type + ": "
            self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            self.nb['cells'].append(nbf.v4.new_code_cell())
        elif isinstance(node, ast.AugAssign):
            Type = 'AugAssign'
            text = whitespace + str(node.lineno) + " :" + Type + ": \n\n"
            self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            self.nb['cells'].append(nbf.v4.new_code_cell())
        elif isinstance(node, ast.Return):
            Type = 'Return'
            text = whitespace + str(node.lineno) + " :" + Type + ": \n\n"
            self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            self.nb['cells'].append(nbf.v4.new_code_cell())
        else:
            Type = str(type(node))
            text = whitespace + str(node.lineno) + " :" + Type + ": \n\n"
            self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
            self.nb['cells'].append(nbf.v4.new_code_cell())
        self.lineNo.append([node.lineno,depth])

    def visit_Str(self, node, depth, attr=None):
        depth += 1
        for text in node:
            if isinstance(text, ast.Call):
                self.visit_Call(text, depth)
                print("str call")
            elif isinstance(text, ast.Num):
                self.visit_Num(text, depth)
                print("str num")
            elif isinstance(text, ast.Str):
                if attr == 'arg' or attr == 'arg_only':
                    self.updateNode(text,depth)
                    print("arg1")
                print('Found String: "' + text.s + '"')
            elif isinstance(text, ast.Name):
                if attr == 'arg':
                    self.updateNode(text,depth)
                    print('arg2')
                if attr == 'arg_only':
                    self.updateNode(text,depth,attributes=attr)

    def visit_Name(self, node, depth, attr=None):
        depth += 1
        if attr == 'call':
            self.updateNode(node,depth)
        elif attr == 'forIter':
            print("visited name")
            self.updateNode(node,depth,attributes=attr)
        elif attr == 'forTarget':
            self.updateNode(node,depth,attributes=attr)

        if isinstance(node, list):
            for name in node:
                print("hello ", len(node))
                # print('Name: ' + name.id, name.ctx)

        elif isinstance(node, ast.Add):
            print('Add: ' + str(node))
        else:
            # print('Name: ' + node.id, node.ctx)
            pass
        pass

    def visit_FunctionDef(self, node):
        depth = 0
        print('Function Definition: ' + str(node.name))
        self.addNode(node, depth)
        depth = 1
        self.visit_arguments(node.args, depth)
        for node in node.body:
            print("in function " ,node)
            self.addNode(node, depth)
            if isinstance(node, ast.Str):
                self.visit_Str(node, depth)
                # self.visit_Constant(node, depth)
                pass
            elif isinstance(node, ast.FunctionDef):
                self.visit_FunctionDef(node)
            elif isinstance(node, ast.Expr):
                self.visit_Expr(node, depth)
            elif isinstance(node, ast.Assign):
                print("assign")
                self.visit_Assign(node, depth)
            elif isinstance(node, ast.While):
                self.visit_While(node, depth)
            elif isinstance(node, ast.For):
                self.visit_For(node, depth)
            elif isinstance(node, ast.If):
                self.visit_If(node,depth)
            elif isinstance(node, ast.Return):
                self.visit_Return(node, depth)
            else:
                print("reached1")
                print(node)
        print("end")
        pass

    def visit_Expr(self, node=None, depth=None):
        if depth is None:
            self.general_visit_Expr(node)
        else:
            # print("hello")
            self.depth_visit_Expr(node ,depth)
        pass

    def general_visit_Expr(self, node):
        print("general")
        if isinstance(node, list):
            for nod in node:
                print('Expression: ' + str(nod.value))
                self.visit_Call(nod.value, 0, 'expr')
        else:
            print('Expression: ' + str(node.value))
            self.visit_Call(node.value, 0, 'expr')
        pass

    def depth_visit_Expr(self, node, depth):
        depth += 1
        if isinstance(node, list):
            for nod in node:
                print('Expression: ' + str(nod.value))
                self.visit_Call(nod.value, depth, 'expr')
        else:
            print('Expression: ' + str(node.value))
            self.visit_Call(node.value, depth, 'expr')
        pass

    def visit_Call(self, node, depth, attr=None):
        depth += 1
        # print("reached")
        print('Call: ' + str(node.func))
        if attr == 'expr':
            self.updateNode(node,depth)
            print("in call expr")
        self.visit_Name(node.func , depth, 'call')
        print("call end")
        self.visit_Str(node.args, depth, 'arg_only')
        pass

    def visit_Assign(self, node, depth=0):
        depth += 1
        # print("Test " + str(node.value))
        if isinstance(node, list):
            for nod in node:
                if isinstance(nod, ast.If):
                    self.visit_If(nod, depth)
                else:
                    self.visit_Name(nod.targets, depth)
                    print('Assign: ' + str(nod.value))
                    self.visit_Call(nod.value, depth)
        else:
            # print("hello" + str(node))
            self.visit_Name(node.targets, depth)
            print('Assign: ' + str(node.value))
            if isinstance(node.value, ast.Num):
                self.visit_Num(node.value, depth)
            elif isinstance(node.value, ast.ListComp):
                self.visit_ListComp(node.value, depth)
        pass

    def visit_ListComp(self, node, depth):
        print("List: " + str(node.elt))
        self.visit_Call(node.elt, depth)
        pass

    def visit_Num(self, node, depth):
        depth += 1
        # print("hello " + str(ast.dump(node)))
        if isinstance(node, list):
            for nod in node:
                # print('Num: ' + str(nod.n))
                pass
        else:
            # print('Num: ' + str(node.n))
            pass
        pass

    def visit_While(self, node, depth):
        depth += 1
        print('While: ' + str(node.test))
        self.visit_Compare(node.test, depth)
        self.visit_Try(node.body, depth)
        pass

    def visit_For(self, node, depth):
        depth += 1
        print("visited for")
        print('For: ')
        # self.addNode(node,depth)
        self.visit_Name(node.target, depth, 'forTarget')
        print("visited for")
        if isinstance(node.iter, ast.Name):
            self.visit_Name(node.iter, depth, 'forIter')
            print("for iter")
        elif isinstance(node.iter, ast.Call):
            self.visit_Call(node.iter, depth, 'expr')
            print("for expr")
        self.visit_Try(node.body, depth)
        pass

    def visit_Try(self, nodes, depth):
        depth += 1
        for node in nodes:
            self.addNode(node,depth)
            print("in while ", node)
            if isinstance(node, ast.Expr):
                self.visit_Expr(node, depth)
            elif isinstance(node, ast.Assign):
                self.visit_Assign(node, depth)
            elif isinstance(node, ast.AugAssign):
                self.visit_AugAssign(node, depth)
            elif isinstance(node, ast.While):
                self.visit_While(node, depth)
            elif isinstance(node, ast.For):
                self.visit_For(node, depth)
            elif isinstance(node, ast.Try):
                print('Try: ')
                self.visit_Assign(node.body, depth)
                # self.visit_ExceptHandler(node.handlers, depth)
        pass

    def visit_AugAssign(self, node, depth):
        depth+=1
        print('AugAssign')
        self.visit_Name(node.target,depth)
        # self.visit_Name(node.op,depth)
        print(node.op)
        self.visit_Num(node.value,depth)
        pass

    def visit_arguments(self, node, depth):
        depth += 1
        # print("arg")
        print('Arguments: ' + str(node.args))
        pass

    def visit_Compare(self, node, depth):
        depth += 1
        print('Comparision')
        if not isinstance(node, ast.BoolOp):
            self.visit_Name(node.left, depth)
            # self.visit_Name(node.ops, depth)
            print(node.ops)
            self.visit_Num(node.comparators, depth)
        pass

    def visit_If(self, node, depth):
        print("If")
        print(node.lineno)
        depth += 1
        self.visit_Compare(node.test, depth)
        for body_part in node.body:
            self.addNode(body_part,depth)
            print("if de",depth)
            if isinstance(body_part, ast.Expr):
                self.visit_Expr(body_part, depth)
                
        for or_else_part in node.orelse:
            # print("else" + str(type(or_else_part)))
            if isinstance(or_else_part, ast.If):
                depth -= 1
                print('ElIf')
                self.addNode(or_else_part,depth,attributes = "Elif")
                self.visit_If(or_else_part, depth)
            else:
                print('Else')
                print(or_else_part)
                self.addNode(or_else_part,depth,attributes = "Else")
                if isinstance(or_else_part, ast.Expr):
                    self.visit_Expr(or_else_part, depth)
                elif isinstance(or_else_part, ast.Assign):
                    self.visit_Assign(or_else_part, depth)
        pass

    def visit_Return(self, node, depth):
        depth += 1
        if isinstance(node.value, ast.BinOp):
            self.visit_BinOp(node.value, depth)
        else:
            print(str(node.value))
        pass

    def visit_BinOp(self, node, depth):
        depth += 1
        print('BinOp')
        self.visit_Name(node.left, depth)
        self.visit_Name(node.op, depth)
        self.visit_Name(node.right, depth)
        pass

    def get_Notebook(self):
        file = nbf.write(self.nb, 'astIPYNB.ipynb')
        with open("dump.txt", "wb") as fp:
            pickle.dump(self.lineNo, fp)
        return file


# code_file = open('example.py').read()
# code = ast.parse(code_file)
# # for k in code.body:
# #     print(k)

# # print("end")
# visitor = MyVisitor(nb = [], lineNo = [])
# visitor.visit(code)
# print()
# visitor.get_Notebook()

