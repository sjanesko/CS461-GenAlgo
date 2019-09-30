class Schedule:
    def __init__(self, CS101A, CS101B, CS201A, CS201B, CS191A, CS191B, CS291B, CS291A, CS303, CS341, CS449, CS461):
        self.courseArray = [CS101A, CS101B, CS201A, CS201B, CS191A, CS191B, CS291B, CS291A, CS303, CS341, CS449, CS461]
    
    def print(self):
        print("Schedule:")
        for course in self.courseArray:            
            course.print()
        print("------------")