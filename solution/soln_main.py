class BusinessLead():

    def __init__(self, name, trainable, train):
        self.name = name
        self.trainable = trainable
        self.train = train

    def __lt__(self, other):
        return (self.train - self.trainable) < (other.train - other.trainable)

    def __repr__(self)
        return repr((self.name, self.trainable, self.train))

if __name__ == "__main__":
    leads = (BusinessLead("ABC", 15, 10), BusinessLead("DEF", 25, 25), BusinessLead("GHI", 35, 0), BusinessLead("JKL", 5, 3), BusinessLead("MNO", 10, 2))
    print(sorted(leads))
    

    
