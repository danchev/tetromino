# def pytest_addoption(parser):
#     parser.addoption("--all", action="store_true", help="run all combinations")


# def pytest_generate_tests(metafunc):
#     if "param1" in metafunc.fixturenames:
#         if metafunc.config.getoption("all"):
#             end = 5
#         else:
#             end = 2
#         metafunc.parametrize("param1", range(end))

# def pytest_generate_tests(metafunc):
#     idlist = []
#     argvalues = []
#     for scenario in metafunc.cls.scenarios:
#         idlist.append(scenario[0])
#         items = scenario[1].items()
#         argnames = [x[0] for x in items]
#         argvalues.append([x[1] for x in items])
#     metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


# scenario1 = ("basic", {"attribute": "value"})
# scenario2 = ("advanced", {"attribute": "value2"})


# class TestSampleWithScenarios:
#     scenarios = [scenario1, scenario2]

#     def test_demo1(self, attribute):
#         assert isinstance(attribute, str)

#     def test_demo2(self, attribute):
#         assert isinstance(attribute, str)



# This script generates a Tetris input file of random length and random moves.
# Usage: import and call generate_random_tetris_input(filename, num_lines)
# import random


# def generate_random_tetris_input(filename, num_lines):
#     piece_types = ["Q", "Z", "S", "T", "I", "L", "J"]
#     width = random.randint(5, 150)  # Random width between 5 and 15
#     with open(filename, "w") as f:
#         for _ in range(num_lines):
#             line = []
#             for _ in range(width):
#                 piece = random.choice(piece_types)
#                 col = random.randint(0, width - 1)
#                 line.append(f"{piece}{col}")
#             f.write(",".join(line) + "\n")


# # Example usage:
# # generate_random_tetris_input("tests/resources/random_input.txt", 500)

# if __name__ == "__main__":
#     generate_random_tetris_input("random_input.txt", 500)
