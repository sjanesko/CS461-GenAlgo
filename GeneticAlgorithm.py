#Reference https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6

coursesExpectedEnrollment = {"CS 101A": 40, "CS 101B": 25, "CS 201A": 30, "CS 201B": 30, "CS 191A": 60, "CS 191B": 20, "CS 291B": 40, "CS 291A": 20, "CS 303": 50, "CS 341": 40, "CS 449": 55, "CS 461": 40}

instructorClasses = {"Hare": ["CS 101", "CS 201", "CS 291", "CS 303", "CS 449", "CS 461"],
                    "Bingham": ["CS 101", "CS 201", "CS 191", "CS 291", "CS 449"],
                    "Kuhail": ["CS 303", "CS 341"],
                    "Mitchell": ["CS 191", "CS 291", "CS 303", "CS 341"],
                    "Rao": ["CS 291", "CS 303", "CS 341", "CS 461"]
                    }

roomCapacities = {"Haag 301": 70, "Haag 206": 30, "Royall 204": 70, "Katz 209": 50, "Flarsheim 310": 80, "Flarsheim 260": 25, "Bloch 0009": 30}

timeSlots = ["10A", "11A", "12P", "1P", "2P", "3P", "4P"]

print(roomCapacities["Haag 301"])