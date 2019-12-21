import numpy as np
data = np.loadtxt("data.txt",delimiter=",",skiprows=1)

class K_Mean():

    def __init__(self,train,k_mean):
        self.train_X = train
        self.change_rates = [-1]
        self.centroid_centers = []
        self.cluster_map = { index:cluster for index,cluster in enumerate(np.random.randint(0,k_mean,
                                                                                              size = self.train_X.shape[0]))}
        self.train(k_mean)

    def train(self,k_mean):
        while True:
            for cluster_index in range(k_mean):
                cluster_instances = self.train_X[np.where(np.array(list(self.cluster_map.values())) == cluster_index)]
                self.centroid_centers.append(np.mean(cluster_instances,axis=0))
            t = np.array(list(self.cluster_map.values()))
            self.cluster_map = { index : cluster for index,cluster in enumerate(K_Mean.cluster_assignment(self.train_X,
                                                                                                        self.centroid_centers))}
            self.change_rates.append(np.mean(t == np.array(list(self.cluster_map.values()))) * 100)
            self.centroid_centers.clear()
            if self.change_rates[-1] == self.change_rates[-2]:
                break
            print(self.change_rates[-1])

    @staticmethod
    def cluster_assignment(train_set,centroid_centers):
        import pdb
        get_cluster = lambda observations: int(np.argmin(np.sum(np.square(observations - centroid_centers),axis=1)))
        cluster_indexes = [get_cluster(indv) for indv in train_set]
        return np.array(cluster_indexes)

s = K_Mean(data,5)