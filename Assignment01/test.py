import threading
import random
import time

# Constants
MAX_MEALS = 100
MAX_WAIT_TIME = 0.1  # 100 milliseconds
SIMULATION_TIME = 10  # 10 seconds

# States
THINKING = 0
TAKING_LEFT_FORK = 1
TAKING_RIGHT_FORK = 2
EATING = 3
PUTTING_DOWN_LEFT_FORK = 4
PUTTING_DOWN_RIGHT_FORK = 5

def run_simulation(num_philosophers):
    global meals_eaten  # Declare meals_eaten as a global variable
    
    # Locks for each fork
    forks = [threading.Lock() for _ in range(num_philosophers)]

    # Initialize meals_eaten
    meals_eaten = [0] * num_philosophers

    # Function for each philosopher
    def philosopher(philosopher_id):
        global meals_eaten

        start_time = time.time()
        while time.time() - start_time < SIMULATION_TIME:

            # Thinking
            print_state(philosopher_id, THINKING)
            time.sleep(random.random() * MAX_WAIT_TIME)

            # Hungry - try to acquire left fork
            print_state(philosopher_id, TAKING_LEFT_FORK)
            if forks[philosopher_id].acquire(timeout=1):

                # Try to acquire right fork
                print_state(philosopher_id, TAKING_RIGHT_FORK)
                if forks[(philosopher_id + 1) % num_philosophers].acquire(timeout=1):

                    # Eating
                    print_state(philosopher_id, EATING)
                    meals_eaten[philosopher_id] += 1
                    time.sleep(random.random() * MAX_WAIT_TIME)

                    # Release left fork
                    print_state(philosopher_id, PUTTING_DOWN_LEFT_FORK)
                    forks[philosopher_id].release()

                    # Release right fork
                    print_state(philosopher_id, PUTTING_DOWN_RIGHT_FORK)
                    forks[(philosopher_id + 1) % num_philosophers].release()

                else:
                    # Continue program if encounter a deadlock
                    print(f"Deadlock encountered! Unable to acquire right fork by Philosopher {philosopher_id}.")
                    return False
            else:
                # Continue program if encounter a deadlock
                print(f"Deadlock encountered! Unable to acquire left fork by Philosopher {philosopher_id}.")
                return False
        return True

    # Create philosopher threads
    philosopher_threads = []
    for i in range(num_philosophers):
        philosopher_thread = threading.Thread(target=philosopher, args=(i,))
        philosopher_threads.append(philosopher_thread)

    # Start philosopher threads
    for philosopher_thread in philosopher_threads:
        philosopher_thread.start()

    # Join philosopher threads
    for philosopher_thread in philosopher_threads:
        philosopher_thread.join()

    return meals_eaten

def print_state(philosopher_id, state):
    states = ["Thinking", "Taking left fork", "Taking right fork", "Eating", "Putting down left fork", "Putting down right fork"]
    print(f"Philosopher {philosopher_id} is {states[state]}")

# Input array specifying the number of philosophers
num_philosophers_array = [2,4,6,8,10]

# 2D array to store meals eaten by each philosopher
meal_records = []

# Run simulations for different numbers of philosophers
for num_philosophers in num_philosophers_array:
    print(f"\nSimulating with {num_philosophers} philosophers:")
    meals_eaten = run_simulation(num_philosophers)
    total_meals = sum(meals_eaten)
    meal_records.append((meals_eaten, total_meals))

# Print table of meal records
print("\nMeal Records:")
print("# of Philosophers | Percentage of meals | Total Meals before deadlock")
for i, num_philosophers in enumerate(num_philosophers_array):
    meals_eaten, total_meals = meal_records[i]
    print(f"{num_philosophers} | {meals_eaten} | {total_meals}")
