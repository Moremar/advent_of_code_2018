RECIPES = [3, 7]
ELVES = [0, 1]


def next_recipe():
    sum_recipe = RECIPES[ELVES[0]] + RECIPES[ELVES[1]]
    if sum_recipe >= 10:
        RECIPES.append(1)
        sum_recipe -= 10
    RECIPES.append(sum_recipe)
    for elf_id in range(len(ELVES)):
        next_id = (ELVES[elf_id] + 1 + RECIPES[ELVES[elf_id]]) % len(RECIPES)
        ELVES[elf_id] = next_id


def compute(steps):
    while len(RECIPES) < steps + 10:
        next_recipe()
    return ''.join([str(i) for i in RECIPES[steps:steps+10]])


if __name__ == '__main__':
    print("Scores of the 10 next recipes  = ", compute(540561))
