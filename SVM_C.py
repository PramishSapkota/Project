from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix
import numpy as np

class SVM_Classifier:
    def __init__(self, learning_rate=0.01, no_of_iterations=1000, lambda_parameter=0.01, batch_size=None, kernel='linear', gamma=0.1):
        self.learning_rate = learning_rate
        self.no_of_iterations = no_of_iterations
        self.lambda_parameter = lambda_parameter
        self.batch_size = batch_size
        self.kernel = kernel
        self.gamma = gamma
        self.w = None
        self.b = None
        self.scaler = None
        self.X = None
        self.Y = None
        self.alpha = None

    def fit(self, X, Y):
        # Convert X to a sparse matrix if it's not already
        if not isinstance(X, csr_matrix):
            X = csr_matrix(X)

        # Normalize features
        self.scaler = StandardScaler(with_mean=False)  # with_mean=False for sparse matrices
        X = self.scaler.fit_transform(X)

        self.m, self.n = X.shape
        self.w = np.random.randn(self.n) * 0.01
        self.b = 0
        self.alpha = np.zeros(self.m)
        self.X = X
        self.Y = np.where(Y <= 0, -1, 1)

        for i in range(self.no_of_iterations):
            if self.batch_size:
                indices = np.random.choice(self.m, self.batch_size, replace=False)
                X_batch = X[indices]
                y_batch = self.Y[indices]
                self._update_weights(X_batch, y_batch, indices)
            else:
                self._update_weights(X, self.Y, np.arange(self.m))

    def _kernel_function(self, X1, X2):
        if self.kernel == 'linear':
            return X1.dot(X2.T).toarray()
        elif self.kernel == 'rbf':
            sq_dist = np.sum(X1.power(2), axis=1) + np.sum(X2.power(2), axis=1).T - 2 * X1.dot(X2.T).toarray()
            return np.exp(-self.gamma * sq_dist)
        else:
            raise ValueError("Unsupported kernel. Choose 'linear' or 'rbf'.")

    def _update_weights(self, X, y_label, indices):
        if self.kernel == 'linear':
            linear_output = X.dot(self.w) - self.b
        else:
            K = self._kernel_function(X, self.X)
            linear_output = K.dot(self.alpha * self.Y) - self.b

        condition = y_label * linear_output >= 1
        dw = (2 * self.lambda_parameter * self.w) - X[~condition].T.dot(y_label[~condition])
        db = -np.sum(y_label[~condition])

        self.w -= self.learning_rate * dw
        self.b -= self.learning_rate * db

        if self.kernel != 'linear':
            self.alpha[indices[~condition]] += self.learning_rate * y_label[~condition]

    def predict(self, X):
        if self.scaler is None:
            raise ValueError("Model must be fitted before prediction.")

        # Convert X to a sparse matrix if it's not already
        if not isinstance(X, csr_matrix):
            X = csr_matrix(X)

        # Use the same scaler that was used during training
        X = self.scaler.transform(X)

        if self.kernel == 'linear':
            output = X.dot(self.w) - self.b
        else:
            K = self._kernel_function(X, self.X)
            output = K.dot(self.alpha * self.Y) - self.b

        predicted_labels = np.sign(output)
        return np.where(predicted_labels <= -1, 0, 1)