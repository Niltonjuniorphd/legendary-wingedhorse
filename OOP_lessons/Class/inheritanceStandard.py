from classWriteStandard import ClassName

class Inheritance(ClassName):

    '''
    This is a class description for the class Inheritance.
    This class is used to show how to write a Inheritance in python.
    Inheritance is the name of the class.

    '''
    def __init__(self, name_var1, name_var2, name_var3, name_var_new):
        ClassName.__init__(self, name_var1, name_var2, name_var3)
        self.var_new = name_var_new

    def FunctionActionPrint2(self):
        print("This is a function that print the value of the var1 from class Inheritance") #print some text to the screen
        print(self.var1) #print the value of the variable var1
        print(self.var_new) #print the value of the variable var_new
        
