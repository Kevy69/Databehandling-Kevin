# import sympy 
from sympy import * 
  
M = Matrix([[2, 1, -9],
            [1, 1, -7],
            [-1, 1, -3]])
print("Matrix : {} ".format(M))
   
# Use sympy.rref() method 
M_rref = M.rref()
      
print("The Row echelon form of matrix M and the pivot columns : {}".format(M_rref)) 