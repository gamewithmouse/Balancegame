class BalanceCore:
    def __init__(self, choice_list):
        self.choice_list = choice_list
        self.winned_list = []

    def choose(self, idx):
        self.winned_list.append(self.choice_list[idx])
        del self.choice_list[0:2]

    def get_choice(self):

        print(self.choice_list, self.winned_list)
        if len(self.winned_list) == 1 and len(self.choice_list) == 0:
            return {"result": self.winned_list, "stats": "won"}
        if len(self.choice_list) == 1:
            self.winned_list.append(self.choice_list[0])
            del self.choice_list[0]

        if len(self.choice_list) < 2:
            print("add")
            self.choice_list += self.winned_list
            self.winned_list = []

        return {"result" : self.choice_list[0:2], "stats" : "normal"}

# 마크 로
#
#
#
#


if __name__ == "__main__":
    core = BalanceCore(["마크", "로블", "브롤", "카러플", "무계"])
    while True:
        choice = core.get_choice()
        if choice["stats"] == "normal":
            print(", ".join(choice["result"]))
        else:
            print(choice["result"][0], "승")
        core.choose(int(input("선택지")))
