class ClassName:
    '''
    This is a class description for the class.
    This class is used to show how to write a class in python.

    '''

    #Define the constructor of the class attributes
    #self is a dictionary of the atributes/variables of the class
    def __init__(self, name_var1, name_var2, name_var3):
        self.var1 = name_var1 #define the variables or atributes of the class
        self.var2 = name_var2
        self.var3 = name_var3

    #Define the functions of the class
    def FunctionAction(self, name_param1, name_param2, name_param3):
        print("This is a function") #print some text to the screen
        return self.var1*(1-self.name_param1) #return the result of a action function
        