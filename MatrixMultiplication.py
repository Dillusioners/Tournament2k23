# function to input a matrix
def input_matrix():
	# asking user for the row and coloums in the matrix
    row = int(input('Enter the row for the matrix: '))
    col = int(input('Enter the coloumn for the matrix: '))
    matrix = []

    print()
	
	# iterating through the matrix
    for i in range(row):
		# initializing a new row
        matrix.append([])
        for j in range(col):
			# appending an element to specified location
            matrix[i].append(int(input(f'Enter the element for [{i + 1}, {j + 1}]: ')))

    return matrix

# function to multiply two matrices using row-coloumn method
def multiply_matrices(A, B):
	# if the coloumn of first matrix doesnt match the row of second matrix
	# i.e. unable to multiply
    if len(A[0]) != len(B):
        print ("Matrix multiplication not possible. Number of columns in the first matrix must be equal to the number of rows in the second matrix.")
		return None
	
    result = []

	# iterating through the first matrix
    for i in range(len(A)):
        row = []

		# iterating through the row of second matrix
        for j in range(len(B[0])):
            element = 0

			# iterating through the coloumns of the second matrix
            for k in range(len(B)):
				# multiplying the matrix based on the row-coloum method
                element += A[i][k] * B[k][j]

			# appening the new element to row
            row.append(element)

		# appending the new row to the result
        result.append(row)
		
    return result

# function to print a matrix
def print_matrix(matrix):
	# iteating through the matrix and printing all the members
	for row in matrix:
		for elem in row:
			print(elem, end=' ')

		print() # printing newline

# main method
def main():
	# inputting the two matrices
	A = input_matrix()
	print('\n')
	B = input_matrix()
	
	# the multiplication being calculated
	result_matrix = multiply_matrices(A, B)

	# if successfuly multiplication is done
	if result_matrix != None:
		# printing the result
		print('\nThe resulting matrix is: ')
		print_matrix(result_matrix)

# running the program
if __name__ == '__main__':
	main()
