from collections import deque
import random

class NQueensCSP:
    """
    Class to represent the N-Queens problem using Constraint Satisfaction Problem (CSP) techniques.
    """
    def __init__(self):
        #initializing domains and constraints variables
        self.domains = {}
        self.constraints = []
            
    def read_input(self, file_path):
        """
        function to read input from a file or generate a random board, and initialize the domain and constraint variables.
        """
        if file_path:
            #reading queen columns from the file
            with open(file_path, 'r') as file:
                queen_cols = [int(line.strip()) for line in file]
                n = len(queen_cols)
        else:
            #generating a random board with one queen in each column
            n = int(input("Enter the board size (10 <= n <= 1000): "))
            queen_cols = [random.randint(0, n - 1) for _ in range(n)]

        #initializing domains with all possible row values for each column
        self.domains = {i: list(range(n)) for i in range(n)}
        #generating all possible constraints between pairs of variables
        self.constraints = [(i, j) for i in range(n) for j in range(n) if i != j]
        return queen_cols

    def is_consistent(self, variable, value, assignment):
        """
        function to check if assigning a value to a variable maintains consistency with the current assignment.
        """
        #checking if the value conflicts with any existing assignments
        for var, val in assignment.items():
            if val == value or abs(val - value) == abs(var - variable):
                return False
        return True

    def select_unassigned_variable(self, assignment):
        """
        function to select an unassigned variable based on the MRV heuristic.
        """
        #selecting the variable with the fewest remaining values in its domain
        unassigned_vars = [var for var in range(len(self.domains)) if var not in assignment]
        return min(unassigned_vars, key=lambda var: (len(self.domains[var]), -var))

    def order_domain_values(self, variable, assignment):
        """
        function to order the domain values for a variable based on the LCV heuristic.
        """
        def lcv_score(value):
            #calculating the LCV score for each value in the domain
            count = 0
            for neighbor_var in range(len(self.domains)):
                if neighbor_var != variable and neighbor_var not in assignment:
                    for neighbor_val in self.domains[neighbor_var]:
                        if self.is_consistent(neighbor_var, neighbor_val, {**assignment, variable: value}):
                            count += 1
            return count
        #sorting domain values based on LCV score
        return sorted(self.domains[variable], key=lcv_score, reverse=True)

    def revise(self, var_i, var_j):
        """
        function to revise the domains of two variables to enforce arc consistency.
        """
        revised = False
        for val_i in self.domains[var_i][:]:
            #checking if there is any value in var_i's domain that satisfies the constraints with var_j
            if all(not any(val_i == val_j for val_j in self.domains[var_j]) for val_j in self.domains[var_j]):
                #if no such value found, removing val_i from var_i's domain
                self.domains[var_i].remove(val_i)
                revised = True
        return revised

    def AC3(self):
        """
        function that use the AC3 algorithm to enforce arc consistency.
        """
        #initializing a queue with all constraints
        queue = deque(self.constraints)
        while queue:
            #pop a constraint from the queue
            var_i, var_j = queue.popleft()
            #revise the domains of var_i and var_j
            if self.revise(var_i, var_j):
                #if var_i's domain becomes empty, return False (no solution)
                if not self.domains[var_i]:
                    return False
                #adding new constraints to the queue based on var_i's revisions
                for var_k, _ in self.constraints:
                    if var_k != var_j:
                        queue.append((var_k, var_i))
        return True

    def backtracking_search(self):
        """
        function to perform backtracking search to find a solution to the N-Queens problem.
        """
        return self._backtrack({})

    def _backtrack(self, assignment):
        """
        recursive helper function for backtracking search.
        """
        if len(assignment) == len(self.domains):
            return assignment
        #selecting an unassigned variable
        variable = self.select_unassigned_variable(assignment)
        #ordering domain values for the selected variable
        ordered_values = self.order_domain_values(variable, assignment)
        
        for value in ordered_values:
            #checking if the value is consistent with the current assignment
            if self.is_consistent(variable, value, assignment):
                #assigning the value to the variable
                assignment[variable] = value
                #recursively call _backtrack with the updated assignment
                result = self._backtrack(assignment)
                #if a solution is found, return it
                if result is not None:
                    return result
                #if no solution found, remove the assignment and continue searching
                del assignment[variable]
        
        #if no solution found, return None
        return None

    def solve_nqueens(self, file_path):
        """
        function to solve the N-Queens problem using CSP techniques.
        """
        #reading input from file and initializing domains and constraints
        queen_cols = self.read_input(file_path)
        #enforcing arc consistency using AC3
        if self.AC3():
            #perform backtracking search to find a solution
            assignment = self.backtracking_search()
            #printing solution if found
            if assignment is None:
                print("No solution found")
            else:
                print("Solution found")
                for i in range(len(queen_cols)):
                    print((i+1, assignment[i]+1))
        else:
            print("No solution found.")


csp_solver = NQueensCSP()
csp_solver.solve_nqueens("D:/G48698217/nqueens.txt")  #solving N-Queens problem using input from file
#if the file path is not mentioned the board will be initialized randomly by prompting to give n value during run time.
