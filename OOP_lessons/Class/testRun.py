from classWriteStandard import ClassName
from inheritanceStandard import Inheritance

#using the class ClassName

#instantiate the the class
my_object = ClassName('water', 'C', 10)
my_inheritance = Inheritance('water_I', 'C_I', 10, 'juice')

#print values of the variables/atributes of the class
print(my_object.var1) #print the value of the variable var1
print(my_object.var2) #print the value of the variable var2
print(my_object.var3) #print the value of the variable var3

#call the functions of the class
my_object.FuntionChangeValue('cofee') #call the function FuntionChangeValue with the value of the parameter new_value changed from water to cofee
print(my_object.var1) #print the changed value of the variable var1

my_object.FunctionActionPrint() #call the function FunctionActionPrint
my_inheritance.FunctionActionPrint2() #call the function FunctionActionPrint

print(my_object.FunctionActionReturn(0.1)) #print the result of the function FunctionActionReturn with the value of the parameter name_param1

#instantiating several objects of the class ClassName
my_object_2 = ClassName('juice', 'C', 18)
my_object_3 = ClassName('tea', 'H', 12)
my_object_4 = ClassName('sprinkle_water', 'C', 15)

#creating alist of the objects of the class ClassName
my_list = []
my_list.append(my_object)
my_list.append(my_object_2)
my_list.append(my_object_3)
my_list.append(my_object_4)

for i in my_list:
    print(i.var1) #print the value of the variable var1 of each object of the list
    print(i.var2) #print the value of the variable var2 of each object of the list
    print(i.var3) #print the value of the variable var3 of each object of the list
    print('\n') #print a new blank line