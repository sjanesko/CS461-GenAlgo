# Reference https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6
import Course
import Schedule
import random as r
import operator

def fitnessCalculation(schedule):
    fitnessScore = 0

    # creates an array of tuples for the rooms/times and creates list of duplicates
    courseRoomTime = [(course.room, course.time)
                      for course in schedule.courseArray]
    courseRoomsDupes = list(
        set([x for x in courseRoomTime if courseRoomTime.count(x) > 1]))

    # creates array of tuples for teacher/time and creatse list of duplicates
    instructorTimes = [(course.instructor, course.time)
                       for course in schedule.courseArray]
    InstructorTimesDupes = list(
        set([x for x in instructorTimes if instructorTimes.count(x) > 1]))

    for course in schedule.courseArray:
        # For each course that is taught by an instructor who can teach it: +3
        if (course.name in instructorClasses[course.instructor]):
            fitnessScore += 3

        # For each course that is the only course scheduled in that room at that time: +5
        if (course.room, course.time) not in courseRoomsDupes:
            fitnessScore += 5

        # For each course that is in a room large enough to accommodate it: +5
        if coursesExpectedEnrollment[course.name] < roomCapacities[course.room]:
            fitnessScore += 5
            # Room capacity is no more than twice the expected enrollment: +2
            if not coursesExpectedEnrollment[course.name] * 2 < roomCapacities[course.room]:
                fitnessScore += 2

        # For each course that does not have the same instructor teaching another course at the same time: +5
        if (course.instructor, course.time) not in InstructorTimesDupes:
            fitnessScore += 5

    # For each schedule that has the same instructor teaching more than 4 courses: -5 per course over 4
    # creates count of how many instructors are teaching a class
    instructorNameOccurences = [
        course.instructor for course in schedule.courseArray]
    instructorDict = {key: value for (key, value) in (
        (x, instructorNameOccurences.count(x)) for x in set(instructorNameOccurences))}

    for x in (instructorDict.keys()):
        if instructorDict[x] > 4:
            fitnessScore -= (instructorDict[x] - 4) * -5

    # For each schedule that has Rao or Mitchell (graduate faculty) teaching more courses than Hare or Bingham: -5% to total fitness score.
    if ("Rao" in instructorDict and "Hare" in instructorDict and "Bingham" in instructorDict):
        if (instructorDict["Rao"] > instructorDict["Hare"] or instructorDict["Rao"] > instructorDict["Bingham"]):
            fitnessScore -= fitnessScore * 0.05

    elif ("Mitchell" in instructorDict and "Hare" in instructorDict and "Bingham" in instructorDict):
        if (instructorDict["Mitchell"] > instructorDict["Hare"] or instructorDict["Mitchell"] > instructorDict["Bingham"]):
            fitnessScore -= fitnessScore * 0.05
    elif ("Hare" not in instructorDict or "Bingham" not in instructorDict):
        # Hare or Bingham not teaching any classes to lower by 5%
        fitnessScore -= fitnessScore * 0.05

    courseTime = {key: value for (key, value) in [(
        course.name, course.time) for course in schedule.courseArray]}
    courseRoom = {key: value for (key, value) in [(
        course.name, course.room) for course in schedule.courseArray]}

    # CS 101 and CS 191 are usually taken the same semester
    # Courses are scheduled for same time: -10% to score
    if (courseTime["CS 101A"] == courseTime["CS 191A"] or courseTime["CS 101A"] == courseTime["CS 191B"]):
        fitnessScore -= fitnessScore * .1

    # Courses are scheduled for same time: -10% to score
    elif (courseTime["CS 101B"] == courseTime["CS 191A"] or courseTime["CS 101B"] == courseTime["CS 191B"]):
        fitnessScore -= fitnessScore * .1

    adjacentTime = False
    # Courses are scheduled for adjacent times: +5% to score
    if (courseTime["CS 101A"] == (courseTime["CS 191A"] - 100) or courseTime["CS 101A"] == (courseTime["CS 191A"] + 100)):
        fitnessScore += fitnessScore * .05
        adjacentTime = True
    elif (courseTime["CS 101A"] == (courseTime["CS 191B"] - 100) or courseTime["CS 101A"] == (courseTime["CS 191B"] + 100)):
        fitnessScore += fitnessScore * .05
        adjacentTime = True
    elif (courseTime["CS 101B"] == (courseTime["CS 191A"] - 100) or courseTime["CS 101B"] == (courseTime["CS 191A"] + 100)):
        fitnessScore += fitnessScore * .05
        adjacentTime = True
    elif (courseTime["CS 101B"] == (courseTime["CS 191B"] - 100) or courseTime["CS 101B"] == (courseTime["CS 191B"] + 100)):
        fitnessScore += fitnessScore * .05
        adjacentTime = True

    if adjacentTime == True:
        # one in katz other is not
        if ((courseRoom["CS 101A"][:4] or courseRoom["CS 101B"][:4]) == "Katz" and (courseRoom["CS 191A"][:4] or courseRoom["CS 191B"][:4]) != "Katz" or (courseRoom["CS 191A"][:4] or courseRoom["CS 191B"][:4]) == "Katz" and (courseRoom["CS 101A"][:4] or courseRoom["CS 101B"][:4]) != "Katz"):
            fitnessScore == fitnessScore * 0.03
        # one in bloch other is not
        if ((courseRoom["CS 101A"][:5] or courseRoom["CS 101B"][:5]) == "Bloch" and (courseRoom["CS 191A"][:5] or courseRoom["CS 191B"][:5]) != "Bloch" or (courseRoom["CS 191A"][:5] or courseRoom["CS 191B"][:5]) == "Bloch" and (courseRoom["CS 101A"][:5] or courseRoom["CS 101B"][:5]) != "Bloch"):
            fitnessScore == fitnessScore * 0.03

    adjacentTime = False
    # CS 201 and CS 291 are usually taken the same semester
    # Courses are scheduled for same time: -10% to score
    if (courseTime["CS 201A"] == courseTime["CS 291A"] or courseTime["CS 201A"] == courseTime["CS 291B"]):
        fitnessScore -= fitnessScore * .1

    # Courses are scheduled for same time: -10% to score
    elif (courseTime["CS 201B"] == courseTime["CS 291A"] or courseTime["CS 201B"] == courseTime["CS 291B"]):
        fitnessScore -= fitnessScore * .1

    adjacentTime = False
    # Courses are scheduled for adjacent times: +5% to score
    if (courseTime["CS 201A"] == (courseTime["CS 291A"] - 100) or courseTime["CS 101A"] == (courseTime["CS 191A"] + 100)):
        fitnessScore += fitnessScore * .05
        adjacentTime = True
    elif (courseTime["CS 201A"] == (courseTime["CS 291B"] - 100) or courseTime["CS 201A"] == (courseTime["CS 291B"] + 100)):
        fitnessScore += fitnessScore * .05
        adjacentTime = True
    elif (courseTime["CS 201B"] == (courseTime["CS 291A"] - 100) or courseTime["CS 201B"] == (courseTime["CS 291A"] + 100)):
        fitnessScore += fitnessScore * .05
        adjacentTime = True
    elif (courseTime["CS 201B"] == (courseTime["CS 291B"] - 100) or courseTime["CS 201B"] == (courseTime["CS 291B"] + 100)):
        fitnessScore += fitnessScore * .05
        adjacentTime = True

    if adjacentTime == True:
        # one in katz other is not
        if ((courseRoom["CS 201A"][:4] or courseRoom["CS201B"][:4]) == "Katz" and (courseRoom["CS 291A"][:4] or courseRoom["CS 291B"][:4]) != "Katz" or (courseRoom["CS 291A"][:4] or courseRoom["CS 291B"][:4]) == "Katz" and (courseRoom["CS 201A"][:4] or courseRoom["CS 201B"][:4]) != "Katz"):
            fitnessScore = fitnessScore * 0.03
        # one in bloch other is not
        if ((courseRoom["CS 201A"][:5] or courseRoom["CS201B"][:5]) == "Bloch" and (courseRoom["CS 291A"][:5] or courseRoom["CS 291B"][:5]) != "Bloch" or (courseRoom["CS 291A"][:5] or courseRoom["CS 291B"][:5]) == "Bloch" and (courseRoom["CS 201A"][:5] or courseRoom["CS 201B"][:5]) != "Bloch"):
            fitnessScore = fitnessScore * 0.03


    schedule.fitnessScore = fitnessScore

def mutate(course):
    '''Mutates a course'''
    instructorMutate = r.random()
    if instructorMutate < 0.01:
        course.instructor = r.choice(list(instructorClasses.keys()))

    roomMutate = r.random()

    if roomMutate < 0.01:
        course.room = r.choice(list(roomCapacities.keys()))

    timeMutate = r.random()
    if timeMutate < 0.01:
        course.time = r.choice(list(timeSlots))


def crossOver(scheduleA, scheduleB):
    '''Breeds two schedules together by splitting on a random division point'''
    divisionPoint = r.randint(1, 11)
    courses = scheduleA.courseArray[:divisionPoint]
    courses.extend(scheduleB.courseArray[divisionPoint:])

    #call mutation function for each course
    mutations = list(map(mutate, courses))
    return Schedule.Schedule(courses[0], courses[1], courses[2], courses[3], courses[4], courses[5], courses[6], courses[7], courses[8], courses[9], courses[10], courses[11])

def normalizeScores(population):
    sumOfSquares = 0
    for schedule in population: 
        if schedule.fitnessScore > 0:
            schedule.normalizedScore = schedule.fitnessScore ** 2
            sumOfSquares += schedule.normalizedScore
        else:
            schedule.normalizedScore = 0
    for schedule in population: 
        schedule.normalizedScore = schedule.normalizedScore / sumOfSquares

# Setup dictionaries for schedule use
coursesExpectedEnrollment = {"CS 101A": 40, "CS 101B": 25, "CS 201A": 30, "CS 201B": 30, "CS 191A": 60,
                             "CS 191B": 20, "CS 291B": 40, "CS 291A": 20, "CS 303": 50, "CS 341": 40, "CS 449": 55, "CS 461": 40}

instructorClasses = {"Hare": ["CS 101A", "CS 101B" "CS 201A", "CS 201B", "CS 291A", "CS 291B" "CS 303", "CS 449", "CS 461"],
                     "Bingham": ["CS 101A", "CS 101B" "CS 201A", "CS 201B", "CS 191A", "CS 191B", "CS 291A", "CS 291B", "CS 449"],
                     "Kuhail": ["CS 303", "CS 341"],
                     "Mitchell": ["CS 191A", "CS 191B", "CS 291A", "CS 291B", "CS 303", "CS 341"],
                     "Rao": ["CS 291A", "CS 291B", "CS 303", "CS 341", "CS 461"]
                     }

roomCapacities = {"Haag 301": 70, "Haag 206": 30, "Royall 204": 70,
                  "Katz 209": 50, "Flarsheim 310": 80, "Flarsheim 260": 25, "Bloch 0009": 30}

timeSlots = [1000, 1100, 1200, 1300, 1400, 1500, 1600]  # military time

population = []

for x in range(0, 1000):
    CS101A = Course.Course("CS 101A", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS101B = Course.Course("CS 101B", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS201A = Course.Course("CS 201A", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS201B = Course.Course("CS 201B", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS191A = Course.Course("CS 191A", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS191B = Course.Course("CS 191B", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS291B = Course.Course("CS 291B", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS291A = Course.Course("CS 291A", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS303 = Course.Course("CS 303", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS341 = Course.Course("CS 341", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS449 = Course.Course("CS 449", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))
    CS461 = Course.Course("CS 461", r.choice(list(instructorClasses.keys())), r.choice(
        list(roomCapacities.keys())), r.choice(list(timeSlots)))

    population.append(Schedule.Schedule(CS101A, CS101B, CS201A, CS201B,
                                        CS191A, CS191B, CS291B, CS291A, CS303, CS341, CS449, CS461))


# calls fitnesscalculation on the entire population 
x = list(map(fitnessCalculation, population))

#normalized the scores for the cumulative distribution
normalizeScores(population)
#sort list in place
#population.sort(key=operator.attrgetter('fitnessScore'))

#create cumulative distribution dict
cumulativeDistributionCounter = 0
cumulativeDistributionArr = []

for schedule in population:
    cumulativeDistributionArr.append((cumulativeDistributionCounter, schedule))
    cumulativeDistributionCounter += schedule.normalizedScore

# clear population to make room for children and clear memory
population.clear()

#create new population
while len(population) != 1000: 
    # select two schedules to breed
    j = r.random()

    idxA = 0
    while cumulativeDistributionArr[idxA][0] < j:
        idxA += 1
    
    k = r.random()
    idxB = 0
    while cumulativeDistributionArr[idxB][0] < k:
        idxB += 1
    
    population.append(crossOver(cumulativeDistributionArr[idxA][1], cumulativeDistributionArr[idxB][1]))
    
