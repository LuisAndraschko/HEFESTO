import numpy as np
import copy

class KronReduction():
    instances = []

    def add_instance(self):
        KronReduction.instances.append(self)

    @classmethod
    def del_instances(cls):
        cls.instances = []

    def __init__(self, a_matrix, bar) -> None:
        self.a_matrix_org = copy.deepcopy(a_matrix)
        self.pivot = bar - 1
        self.a_matrix = None
        self.matrix_iter = None
        self.add_instance()

    def reduce(self):
        am = self.a_matrix_org
        aux_i = 0
        aux_j = 0

        n = self.a_matrix_org.shape[0]
        m = n - 1

        self.a_matrix = np.zeros((m, m), dtype=complex)
        self.matrix_iter = [i for i in range(m)]

        for i_line in self.matrix_iter:
            for j_line in self.matrix_iter:
                # If element position in line matrix exceeds or equal pivot position in both axis
                if i_line >= self.pivot and j_line >= self.pivot:
                    aux_i, aux_j = i_line + 1, j_line + 1
                    self.a_matrix[i_line][j_line] = am[aux_i][aux_j] - ((am[aux_i][self.pivot] * am[self.pivot][aux_j]) / am[self.pivot][self.pivot])
                # If element position in line matrix exceeds or equal pivot position in X axis
                elif i_line >= self.pivot:
                    aux_i = i_line + 1 
                    self.a_matrix[i_line][j_line] = am[aux_i][j_line] - ((am[aux_i][self.pivot] * am[self.pivot][j_line]) / am[self.pivot][self.pivot])
                # If element position in line matrix exceeds or equal pivot position in Y axis
                elif j_line >= self.pivot:
                    aux_j = j_line + 1
                    self.a_matrix[i_line][j_line] = am[i_line][aux_j] - ((am[i_line][self.pivot] * am[self.pivot][aux_j]) / am[self.pivot][self.pivot])
                # If element position in line matrix doesn't reach pivot position in any axis
                else:
                    self.a_matrix[i_line][j_line] = am[i_line][j_line] - ((am[i_line][self.pivot] * am[self.pivot][j_line]) / am[self.pivot][self.pivot])