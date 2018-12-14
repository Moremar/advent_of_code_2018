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


def compute(seq_str):
    seq = [int(c) for c in seq_str]
    seq_size = len(seq)
    next_recipe()
    next_recipe()
    while True:
        next_recipe()
        if seq == RECIPES[-seq_size:]:
            return len(RECIPES) - seq_size
        elif seq == RECIPES[-seq_size - 1: -1]:
            return len(RECIPES) - seq_size - 1


if __name__ == '__main__':
    print("Recipes before this score  = ", compute('540561'))
