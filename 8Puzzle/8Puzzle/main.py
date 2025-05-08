from eightpuzzle import createRandomEightPuzzle, EightPuzzleSearchProblem
from search import rand, bfs, dfs, astar, ucs

if __name__ == '__main__':
    puzzle = createRandomEightPuzzle(50)
    print('A random puzzle:')
    print(puzzle)

    problem = EightPuzzleSearchProblem(puzzle)
    search_algorithms = [rand, bfs, dfs, astar, ucs]
    for alg in search_algorithms:
        path = alg(problem)
        print(f'{alg.__name__} found a path of {len(path)} moves: {str(path)}')

        curr = puzzle
        for i, p in enumerate(path, 1):
            curr = curr.result(p)
            print(f'After {i} move{("", "s")[i > 1]}: {p}')
            print(curr)
