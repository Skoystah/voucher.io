from collections import namedtuple

TestUser = namedtuple("TestUser", ["name", "password", "is_admin"])

TEST_USERS = {
    1: TestUser("Jos", "SafePassword1", True),
    2: TestUser("Francine", "SafePassword2", False),
    3: TestUser("Marie", "SafePassword3", True),
    4: TestUser("Fritz", "SafePassword4", False),
}
