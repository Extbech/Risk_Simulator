import random
from tqdm import tqdm


class Attacker:
    def __init__(self, name, solider):
        self.name = name
        self.soliders = solider
        self.highest = 0
        self.second_highest = 0
        self.rolls = []
        self.lost = False
        self.single = 0

    def roll(self):
        self.rolls = []
        self.highest = 0
        self.second_highest = 0
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)
        dice_3 = random.randint(1, 6)
        self.rolls = [dice_1, dice_2, dice_3]
        self.rolls.sort(reverse=True)
        self.highest = self.rolls[0]
        self.second_highest = self.rolls[1]
        return

    def roll_2(self):
        self.highest = 0
        self.second_highest = 0
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)
        if dice_1 >= dice_2:
            self.highest = dice_1
            self.second_highest = dice_2

            return
        self.highest = dice_2
        self.second_highest = dice_1
        return

    def single_roll(self):
        self.single = 0
        self.single = random.randint(1, 6)
        return

    def loser(self):
        self.soliders = self.soliders - 1
        if self.soliders < 1:
            self.lost = True
        return


class Defender:
    def __init__(self, name, solider):
        self.name = name
        self.soliders = solider
        self.highest = 0
        self.second_highest = 0
        self.lost = False
        self.single = 0

    def roll(self):
        self.highest = 0
        self.second_highest = 0
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)
        if dice_1 >= dice_2:
            self.highest = dice_1
            self.second_highest = dice_2
            return

        self.highest = dice_2
        self.second_highest = dice_1
        return

    def single_roll(self):
        self.single = 0
        self.single = random.randint(1, 6)
        return

    def loser(self):
        self.soliders = self.soliders - 1
        if self.soliders < 1:
            self.lost = True
        return


class Game:
    def __init__(self, attacker: Attacker, defender: Defender):
        self.attacker = attacker
        self.defender = defender
        self.winner = None

    def play(self):
        while self.attacker.soliders > 0 and self.defender.soliders > 0:
            if self.attacker.soliders >= 3 and self.defender.soliders >= 2:
                self.attacker.roll()
                self.defender.roll()
                self.check_highest_roll()
                self.check_second_highest_roll()
                if self.defender.lost:
                    self.winner = self.attacker

            if self.attacker.soliders == 2 and self.defender.soliders >= 2:
                self.attacker.roll_2()
                self.defender.roll()
                self.check_highest_roll()
                self.check_second_highest_roll()
                if self.attacker.lost:
                    self.winner = self.defender
                if self.defender.lost:
                    self.winner = self.attacker

            if self.attacker.soliders == 2 and self.defender.soliders < 2:
                self.attacker.roll_2()
                self.defender.single_roll()
                lost = self.check_single_against_multiple(self.defender)
                if lost:
                    self.winner = self.attacker

            if self.attacker.soliders == 1 and self.defender.soliders >= 2:
                self.attacker.single_roll()
                self.defender.roll()
                lost = self.check_single_against_multiple(self.attacker)
                if lost:
                    self.winner = self.defender

            if self.attacker.soliders >= 3 and self.defender.soliders == 1:
                self.defender.single_roll()
                self.attacker.roll()
                lost = self.check_single_against_multiple(self.defender)
                if lost:
                    self.winner = self.attacker

            if self.attacker.soliders == 1 and self.defender.soliders == 1:
                self.attacker.single_roll()
                self.defender.single_roll()
                self.winner = self.check_single_vs_single()

        return self.winner

    def check_single_against_multiple(self, who):
        if who == self.attacker:
            if self.defender.highest >= self.attacker.single:
                self.attacker.loser()
                return self.attacker.lost
            else:
                self.defender.loser()
                return self.defender.lost
        else:
            if self.defender.single >= self.attacker.highest:
                self.attacker.loser()
                return self.attacker.lost
            else:
                self.defender.loser()
                return self.defender.lost

    def check_single_vs_single(self):
        if self.defender.single >= self.attacker.single:
            self.attacker.loser()
            return self.defender
        else:
            self.defender.loser()
            return self.attacker

    def check_highest_roll(self):
        if self.defender.highest >= self.attacker.highest:
            self.attacker.loser()
        else:
            self.defender.loser()
        return

    def check_second_highest_roll(self):
        if self.defender.second_highest >= self.attacker.second_highest:
            self.attacker.loser()
        else:
            self.defender.loser()


def write_results(stats):
    with open("results.txt", "w") as f:
        for stat in stats:
            f.write(
                f"Soliders each: {stat['soliders']} || Attacker Win %: {stat['attackerwin']} || Defender Win %: {stat['defenderwin']} || Games Played: {stat['games']}"
            )
            f.write("\n")


if __name__ == "__main__":

    stats = []
    for i in tqdm(range(100)):
        i = i + 1
        attacker_soliders = i
        defender_soliders = i
        defender_wins = 0
        attacker_wins = 0
        for k in range(1000):
            attacker = Attacker("Benji", attacker_soliders)
            defender = Defender("Harald", defender_soliders)
            risk = Game(attacker, defender)
            risk.play()
            if risk.winner.name == "Harald":
                defender_wins += 1
            else:
                attacker_wins += 1
        total_games = attacker_wins + defender_wins
        stats.append(
            {
                "soliders": i,
                "attackerwin": round((attacker_wins / total_games) * 100, 2),
                "defenderwin": round((defender_wins / total_games) * 100, 2),
                "games": total_games,
            }
        )
    for stat in stats:
        print(stat["soliders"])
    write_results(stats)
