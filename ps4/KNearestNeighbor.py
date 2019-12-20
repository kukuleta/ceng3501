import numpy as np

class KNearestNeighbor():
    def __init__(self,train_set):
        self.train_X,self.train_Y = train_set[...,:-1],train_set[...,-1]

    def predict(self,test_set,k_nearest):
        import pdb
        predictions = []
        for i in test_set:
            predictions.append(KNearestNeighbor.get_class(self,i,k_nearest))
        return predictions

    def get_class(self,test_instance,k):
        distances = np.sqrt(np.sum(np.square(test_instance[:-1] - self.train_X),axis=1))
        temp = self.train_Y[np.unique(np.argsort(distances)[:k])]
        unique_categories,counts = np.unique(temp,return_counts=True)
        ranges_with_max_score = np.count_nonzero(counts == np.max(counts))
        if ranges_with_max_score == 1:
            return int(unique_categories[np.where(counts == np.max(counts))])
        else:
            category_indices = unique_categories[np.where(counts == np.max(counts))]
            return int(np.random.choice(category_indices))


if __name__ == "__main__":
    train = np.loadtxt("train.txt",delimiter=",",skiprows=1)
    test = np.loadtxt("test.txt",delimiter=",",skiprows=1)
    model = KNearestNeighbor(train)
    print("Accuracy for k=5 is {acc}".format(acc = np.mean(test[...,-1] == model.predict(test,5))*100))



