from classWriteStandard import ClassName
from inheritanceStandard import Inheritance

#using the class ClassName and class Inheritance

#instantiating several objects of the class ClassName and one for Inheritance
my_object = ClassName('water', 'C', 10)
my_object_2 = ClassName('juice', 'C', 18)
my_object_3 = ClassName('tea', 'H', 12)
my_object_4 = ClassName('sprinkle_water', 'C', 15)
my_inheritance = Inheritance('water_I', 'C_I', 10, 'juice_I')

#print values of the variables/atributes of the class
print('print values of the variables/atributes of the object my_object:')
print('-----------')
print(my_object.var1) #print the value of the variable var1
print(my_object.var2) #print the value of the variable var2
print(my_object.var3) #print the value of the variable var3
print('-----------\n')

#call the functions of the class
print('change the value of the variable var1 from water to cofee:')
print('-----------')
my_object.FuntionChangeValue('cofee') #call the function FuntionChangeValue with the value of the parameter new_value changed from water to cofee
print(my_object.var1) #print the changed value of the variable var1
print('-----------\n')

print('call the functions of the class ClassName and Inheritance:')
print('-----------')
my_object.FunctionActionPrint() #call the function FunctionActionPrint
my_inheritance.FunctionActionPrint2() #call the function FunctionActionPrint
print('-----------\n')

print('call the function FunctionActionReturn:')
print('-----------')
print(my_object.FunctionActionReturn(0.1)) #print the result of the function FunctionActionReturn with the value of the parameter name_param1
print('-----------\n')



#creating alist of the objects of the class ClassName
my_list = []
my_list.append(my_object)
my_list.append(my_object_2)
my_list.append(my_object_3)
my_list.append(my_object_4)
my_list.append(my_inheritance)

for i in my_list:
    print(i.var1) #print the value of the variable var1 of each object of the list
    print(i.var2) #print the value of the variable var2 of each object of the list
    print(i.var3) #print the value of the variable var3 of each object of the list
    print('\n') #print a new blank line