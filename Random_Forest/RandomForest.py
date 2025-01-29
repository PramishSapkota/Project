from DecisionTree import DecisionTree
import numpy as np
from collections import Counter
from joblib import Parallel, delayed
from sklearn.decomposition import PCA  # Import PCA

class RandomForest:
    def __init__(self, n_trees=10, max_depth=10, min_samples_split=2, max_features=None, n_jobs=-1, use_pca=True, n_components=100):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.n_jobs = n_jobs
        self.use_pca = use_pca
        self.n_components = n_components
        self.trees = []
        self.pca = None  # Will hold PCA model if used

    def fit(self, X, y):
        X = X.astype(np.float32)  # Reduce memory usage

        # Apply PCA for feature reduction if enabled
        if self.use_pca:
            self.pca = PCA(n_components=min(self.n_components, X.shape[1]))
            X = self.pca.fit_transform(X)

        if self.max_features is None:
            self.max_features = int(np.sqrt(X.shape[1]))

        self.trees = Parallel(n_jobs=min(self.n_jobs, 2))(  # Reduce parallel jobs
            delayed(self._train_tree)(X, y) for _ in range(self.n_trees)
        )

    def _train_tree(self, X, y):
        tree = DecisionTree(
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            n_features=self.max_features
        )
        X_sample, y_sample = self._bootstrap_samples(X, y)
        tree.fit(X_sample, y_sample)
        return tree

    def _bootstrap_samples(self, X, y):
        n_samples = X.shape[0]
        idxs = np.random.randint(0, n_samples, size=n_samples)
        return X[idxs], y[idxs]

    def predict(self, X):
        X = X.astype(np.float32)  # Convert to float32 for memory efficiency

        if self.use_pca:
            X = self.pca.transform(X)  # Apply PCA to test data

        predictions = np.array(
            Parallel(n_jobs=min(self.n_jobs, 2))(  # Reduce jobs
                delayed(tree.predict)(X) for tree in self.trees
            )
        )
        tree_preds = np.swapaxes(predictions, 0, 1)
        return np.array([self._most_common_label(pred) for pred in tree_preds])

    def _most_common_label(self, y):
        return Counter(y).most_common(1)[0][0]
