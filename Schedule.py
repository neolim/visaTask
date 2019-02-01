# Schedule Task
#
# We have point A where people are coming and point B which is destination where we need to transfer people from A
# As input we have:
#   numBuses - number of busses available for transportation
#   busCapacity - capacity of each bus (all busses are similar)
#   arrivals - sorted array of time when people are coming to point B
#       arrivals.value - number of seconds starting from 00:00
#       0 <= arrivals.value <= 86400
# Return schedule of buses so total waiting time is minimized
# Output:
#   tuple(total waiting time, bus stops array in seconds from 00:00)
#   -1 if there is no way to build schedule to transfer all people

def routes(numArrivals, numBuses, busCapacity, startPoint):

    # If number of buses smaller than number of stops, then exit from recursion and go back in backtracking
    if len(startPoint) > numBuses:
        return []

    # Get last stop from route array
    lastElem = startPoint[-1]

    # Accumulate possible routs result if number of people in arrivals array equal to last stop index and exit from
    # recursion
    if numArrivals == lastElem:
        return [startPoint]

    # Backtracking from last stop by number of ways of busCapacity
    routsResult = []
    for i in range(lastElem + 1, lastElem + busCapacity + 1):
        if i > numArrivals:
            continue
        temp = startPoint + [i]
        routsResult += routes(numArrivals, numBuses, busCapacity, temp)
    return routsResult

def schedule(numBuses, busCapacity, arrivals):
    
    # Corner case when amount of people are more than capacity of all buses
    if len(arrivals) > numBuses * busCapacity:
        return -1

    # Create possible groups
    l = len(arrivals)
    groups = []

    # Create routes for each starting point from 0 to bus capacity.
    for c in range(busCapacity):
        groups += routes(l - 1, numBuses, busCapacity, [c])

    # Measure waiting time for groups with memorization
    memo = dict()
    resultWaitingTime = float('inf')
    result = []
    for group in groups:
        waitingTime = 0
        tempStartPoint = 0
        for elem in group:
            busStopTime = arrivals[elem]
            index = (busStopTime, arrivals[tempStartPoint])

            # Check if total waiting time of all people from arrivals[tempStartPoint] to busStopTime is already
            # calculated. Othervise calculate waiting time and add it to memorization hash map
            if memo.get(index):
                waitingTime += memo[index]
                continue

            groupTotalWaitingTime = 0
            for i in range(tempStartPoint, elem + 1):
                groupTotalWaitingTime += busStopTime - arrivals[i]

            memo[index] = groupTotalWaitingTime
            waitingTime += groupTotalWaitingTime
            tempStartPoint = elem + 1

        # if group total waiting time less than previous value, reassign result
        if waitingTime < resultWaitingTime:
            resultWaitingTime = waitingTime
            result = group

    # Return total waiting time in seconds and indexes of arrivals what buses can use as stop points
    return (resultWaitingTime, result)
