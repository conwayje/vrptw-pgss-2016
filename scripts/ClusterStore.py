from ClusterSolution import ClusterSolution
from Path import Path

class ClusterStore():

  clusters = []
  clustered_customer_ids = []

  @staticmethod
  def cluster(index):
    return clusters[index]

  @staticmethod
  def find_cluster_containing_customer( customer_id ):
    for cluster in ClusterStore.clusters:
      for customer in cluster.customers:
        if customer.number == customer_id:
          return cluster

  @staticmethod
  def store_clusters(filename, customers):

    if filename == "C201":
       c1 = ClusterSolution(1, [customers[i - 1] for i in [39, 36, 34, 38, 37, 33, 32, 35, 31]], Path([customers[i-1] for i in [34, 36, 39, 38, 37, 35, 31, 33, 32]]), 200.0, 7.25547898547, (-34.666666666666664, -9.444444444444445), False)
       c2 = ClusterSolution(2, [customers[i - 1] for i in [16, 14, 12, 19, 15, 18, 17, 13]],     Path([customers[i-1] for i in [12, 14, 16, 15, 19, 18, 17, 13]]),     190.0, 7.34102343001, (-20.375, 30.0),                           False)
       c3 = ClusterSolution(3, [customers[i - 1] for i in [30, 29, 27, 24, 22, 20, 21]],         Path([customers[i-1] for i in [20, 22, 24, 27, 29, 30, 21]]),         90.0,  6.20236952745, (-14.857142857142858, 2.142857142857143),  False)
       c4 = ClusterSolution(4, [customers[i - 1] for i in [52, 47, 43, 50, 42, 41, 51, 45]],     Path([customers[i-1] for i in [47, 52, 50, 51, 45, 42, 41, 43]]),     90.0,  5.41121520548, (-10.375, -17.375),                        False)
       c5 = ClusterSolution(5, [customers[i - 1] for i in [57, 55, 59, 54, 60, 58, 56, 53]],     Path([customers[i-1] for i in [57, 59, 60, 58, 56, 53, 54, 55]]),     200.0, 6.68603956016, (-0.375, -41.25),                          False)
       c6 = ClusterSolution(6, [customers[i - 1] for i in [67, 63, 69, 66, 62, 74, 64, 61, 72]], Path([customers[i-1] for i in [69, 66, 64, 61, 72, 74, 62, 63, 67]]), 180.0, 5.98351645237, (9.222222222222221, -15.555555555555555),  False)
       c7 = ClusterSolution(7, [customers[i - 1] for i in [91, 90, 88, 86, 84, 83, 82]],         Path([customers[i-1] for i in [91, 88, 84, 82, 83, 86, 90]]),         110.0, 8.35195198985, (26.857142857142858, 6.857142857142857),   False)
       c8 = ClusterSolution(8, [customers[i - 1] for i in [81, 76, 71, 79, 73, 70, 80]],         Path([customers[i-1] for i in [81, 76, 71, 70, 73, 79, 80]]),         120.0, 8.05719351554, (49.857142857142854, -18.571428571428573), False)
       ClusterStore.clusters = [c1, c2, c3, c4, c5, c6, c7, c8]
       ClusterStore.clustered_customer_ids = [39, 36, 34, 38, 37, 33, 32,
          35, 31, 16, 14, 12, 19, 15, 18, 17, 13, 30, 29, 27,
          24, 22, 20, 21, 52, 47, 43, 50, 42, 41, 51, 45, 57,
          55, 59, 54, 60, 58, 56, 53, 67, 63, 69, 66, 62, 74,
          64, 61, 72, 91, 90, 88, 86, 84, 83, 82, 81, 76, 71,
          79, 73, 70, 80]

    if filename == "C202":
       c1 = ClusterSolution(1, [customers[i - 1] for i in [39, 36, 34, 38, 37, 33, 32, 35, 31]], Path([customers[i-1] for i in [34, 36, 39, 38, 37, 35, 31, 33, 32]]), 200.0, 7.25547898547, (-34.666666666666664, -9.444444444444445), False)
       c2 = ClusterSolution(2, [customers[i - 1] for i in [16, 14, 12, 19, 15, 18, 17, 13]],     Path([customers[i-1] for i in [12, 14, 16, 15, 19, 18, 17, 13]]),     190.0, 7.34102343001, (-20.375, 30.0),                           False)
       c3 = ClusterSolution(3, [customers[i - 1] for i in [30, 29, 27, 24, 22, 20, 21]],         Path([customers[i-1] for i in [20, 22, 24, 27, 29, 30, 21]]),         90.0,  6.20236952745, (-14.857142857142858, 2.142857142857143),  False)
       c4 = ClusterSolution(4, [customers[i - 1] for i in [52, 47, 43, 50, 42, 41, 51, 45]],     Path([customers[i-1] for i in [47, 52, 50, 51, 45, 42, 41, 43]]),     90.0,  5.41121520548, (-10.375, -17.375),                        False)
       c5 = ClusterSolution(5, [customers[i - 1] for i in [57, 55, 59, 54, 60, 58, 56, 53]],     Path([customers[i-1] for i in [57, 59, 60, 58, 56, 53, 54, 55]]),     200.0, 6.68603956016, (-0.375, -41.25),                          False)
       c6 = ClusterSolution(6, [customers[i - 1] for i in [67, 63, 69, 66, 62, 74, 64, 61, 72]], Path([customers[i-1] for i in [69, 66, 64, 61, 72, 74, 62, 63, 67]]), 180.0, 5.98351645237, (9.222222222222221, -15.555555555555555),  False)
       c7 = ClusterSolution(7, [customers[i - 1] for i in [91, 90, 88, 86, 84, 83, 82]],         Path([customers[i-1] for i in [91, 88, 84, 82, 83, 86, 90]]),         110.0, 8.35195198985, (26.857142857142858, 6.857142857142857),   False)
       c8 = ClusterSolution(8, [customers[i - 1] for i in [81, 76, 71, 79, 73, 70, 80]],         Path([customers[i-1] for i in [81, 76, 71, 70, 73, 79, 80]]),         120.0, 8.05719351554, (49.857142857142854, -18.571428571428573), False)
       ClusterStore.clusters = [c1, c2, c3, c4, c5, c6, c7, c8]
       ClusterStore.clustered_customer_ids = [39, 36, 34, 38, 37, 33, 32,
          35, 31, 16, 14, 12, 19, 15, 18, 17, 13, 30, 29, 27,
          24, 22, 20, 21, 52, 47, 43, 50, 42, 41, 51, 45, 57,
          55, 59, 54, 60, 58, 56, 53, 67, 63, 69, 66, 62, 74,
          64, 61, 72, 91, 90, 88, 86, 84, 83, 82, 81, 76, 71,
          79, 73, 70, 80]

    elif filename == "RC208":
       rc1 = ClusterSolution(1, [customers[i - 1] for i in [17, 47, 14, 12, 16, 15, 11, 10, 13, 9]],  Path([customers[i-1] for i in [12, 14, 47, 17, 16, 15, 13, 9, 11, 10]]),   200.0, 7.81024967591, (-35.0, -9.0),                            False)
       rc2 = ClusterSolution(2, [customers[i - 1] for i in [5, 3, 1, 45, 8, 46, 4, 7, 6, 2]],         Path([customers[i-1] for i in [1, 3, 5, 45, 4, 46, 8, 7, 6, 2]]),          190.0, 7.30000000000, (-20.5, 30.2),                            False)
       rc3 = ClusterSolution(3, [customers[i - 1] for i in [43, 44, 42, 40, 39, 38, 41, 36, 35, 37]], Path([customers[i-1] for i in [42, 44, 43, 40, 36, 35, 37, 38, 39, 41]]),  200.0, 7.47328575661, (20.2, 31.9),                             False)
       rc4 = ClusterSolution(4, [customers[i - 1] for i in [34, 31, 29, 27, 32, 30, 28, 26, 33]],     Path([customers[i-1] for i in [34, 31, 29, 27, 26, 28, 30, 32, 33]]),      150.0, 8.01233616770, (49.44444444444444, -18.333333333333332), False)
       rc5 = ClusterSolution(5, [customers[i - 1] for i in [24, 22, 20, 49, 19, 25, 23, 21, 48, 18]], Path([customers[i-1] for i in [24, 25, 23, 21, 48, 18, 19, 49, 20, 22]]),  200.0, 6.76239602508, (0.3, -40.8),                             False)
       ClusterStore.clusters = [rc1, rc2, rc3, rc4, rc5]
       ClusterStore.clustered_customer_ids = [17, 47, 14, 12, 16, 15, 11, 10, 13, 9,
        5, 3, 1, 45, 8, 46, 4, 7, 6, 2,
        43, 44, 42, 40, 39, 38, 41, 36, 35, 37,
        34, 31, 29, 27, 32, 30, 28, 26, 33,
        24, 22, 20, 49, 19, 25, 23, 21, 48, 18]

    elif filename == "C203":
        c1 = ClusterSolution(1, [customers[i - 1] for i in [57, 55, 54, 59, 60, 58, 56, 53]],        Path([customers[i - 1] for i in [57, 55, 54, 59, 60, 58, 56, 53]]), 200.0, 7.81024967591, (-35.0, -9.0),          True)
        c2 = ClusterSolution(2, [customers[i - 1] for i in [81, 76, 71, 70, 73, 79, 80]],            Path([customers[i - 1] for i in [81, 76, 71, 70, 73, 79, 80]]), 200.0, 7.81024967591, (-35.0, -9.0),              True)
        c3 = ClusterSolution(3, [customers[i - 1] for i in [18, 17, 13, 15, 19, 16, 41, 2]],         Path([customers[i - 1] for i in [18, 17, 13, 15, 19, 16, 41, 2]]), 200.0, 7.81024967591, (-35.0, -9.0),           True)
        c4 = ClusterSolution(4, [customers[i - 1] for i in [39, 38, 37, 35, 31, 32, 33, 34, 36]],    Path([customers[i - 1] for i in [39, 38, 37, 35, 31, 32, 33, 34, 36]]), 200.0, 7.81024967591, (-35.0, -9.0),      True)
        c5 = ClusterSolution(5, [customers[i - 1] for i in [100, 99, 97, 98, 95, 94, 92, 1]],        Path([customers[i - 1] for i in [100, 99, 97, 98, 95, 94, 92, 1]]), 200.0, 7.81024967591, (-35.0, -9.0),          True)
        c6 = ClusterSolution(6, [customers[i - 1] for i in [67, 63, 69, 66, 27, 4, 64, 61, 72, 68]], Path([customers[i - 1] for i in [67, 63, 69, 66, 27, 4, 64, 61, 72, 68]]), 200.0, 7.81024967591, (-35.0, -9.0),   True)
        c7 = ClusterSolution(7, [customers[i - 1] for i in [52, 47, 43, 50, 51, 45, 42, 41]],        Path([customers[i - 1] for i in [52, 47, 43, 50, 51, 45, 42, 41]]), 200.0, 7.81024967591, (-35.0, -9.0),          True)
        c8 = ClusterSolution(7, [customers[i - 1] for i in [30, 29, 27, 24, 22, 20, 21]],            Path([customers[i - 1] for i in [30, 29, 27, 24, 22, 20, 21]]), 200.0, 7.81024967591, (-35.0, -9.0),              True)
        ClusterStore.clusters = [c1, c2, c3, c4, c5, c6, c7, c8]
        ClusterStore.clustered_customer_ids = [57, 55, 54, 59, 60, 58, 56, 53,       
                                              81, 76, 71, 70, 73, 79, 80,
                                              18, 17, 13, 15, 19, 16, 41, 2,
                                              39, 38, 37, 35, 31, 32, 33, 34, 36,
                                              100, 99, 97, 98, 95, 94, 92, 1,
                                              67, 63, 69, 66, 27, 4, 64, 61, 72, 68,
                                              52, 47, 43, 50, 51, 45, 42, 41,
                                              30, 29, 27, 24, 22, 20, 21]
