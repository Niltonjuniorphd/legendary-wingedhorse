class ClassName:
    '''
    This is a class description for the class.
    This class is used to show how to write a class in python.
    ClassName is the name of the class.

    '''

    #The __init__ function define the constructor of the class attributes
    #the param self is a dictionary of the atributes/variables of the class
    def __init__(self, name_var1, name_var2, name_var3):
        self.var1 = name_var1 #define the variables or atributes of the class
        self.var2 = name_var2
        self.var3 = name_var3

    #The next sequence of def define the functions of the class
    def FunctionActionPrint(self):
        print("This is a function that print the value of the var1") #print some text to the screen
        print(self.var1) #print the value of the variable var1

    def FuntionChangeValue(self, new_value):
        self.var1 = new_value #change the value of the variable var1
        
    def FunctionActionReturn(self, name_param1):
        return self.var3*(1-name_param1) #return the result of a action function