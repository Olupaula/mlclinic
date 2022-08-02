import pickle

# femi = {"name": "femi", "age": 20, "class": "master\'s year two"}

class Person:
    def __init__(self):
        femi = "man"
        self.remark ="good man"

    def remark(self):
        return {"femi": self.remark}


femi = Person().remark
save_file = open("femi.pickle", "wb")
pickle.dump(femi, save_file)
save_file.close()

saved_file = open("femi.pickle", "rb")
femi1 = pickle.load(saved_file)
saved_file.close()

print(femi)

'''with open("femi2.pickle", "wb") as f:
    pickle.dump(femi, f)


with open("femi2.pickle", "rb") as f:
    femi2 = pickle.load(f)

print(femi2)'''


