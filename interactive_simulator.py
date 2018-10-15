from simulator import *

def createEnvFromUserInput(bin_size):
    fig = create_env()
    ax = add_bin(fig, bin_size, bin_size)
    return fig, ax

def main():
    bin_size = eval(input("Enter the side length of the bin (5 to 30 inclusive): "))
    while (bin_size < 5 or bin_size > 30):
        bin_size = eval(input("Try again. Enter the side length of the bin (5 to 30 inclusive): "))
    fig, ax = createEnvFromUserInput(bin_size)
    print("Creating a " + str(bin_size) + "x" + str(bin_size) + " bin.\n")

    num_objects = eval(input("Enter the number of objects to be placed (1 to 10 inclusive): "))
    while (num_objects < 1 or num_objects > 10):
        num_objects = eval(input("Try again. Enter the number of objects to be placed (1 to 10 inclusive): "))
    print("Placing " + str(num_objects) + " objects.\n")

    print("For each object (square), enter the side length and transform below.")
    objects = []
    for i in range(num_objects):
        side_length = eval(input("Enter a side length for square " + str(i+1) + " (1 to 10 inclusive): "))
        while (side_length < 1 or side_length > 10):
            side_length = eval(input("Try again. Enter a side length for square " + str(i+1) + " (1 to 10 inclusive): "))

        transform = input("Enter the transform for square " + str(i+1) + " as a list [[a,b,c],[d,e,f],[g,h,i]]: ")
        while (np.array(eval(transform)).shape != (3,3)):
            input("Try again. Enter the transform for square " + str(i+1) + " as a list [[a,b,c],[d,e,f],[g,h,i]]: ")
        square = Square(side_length, np.array(eval(transform)))
        objects.append(square)

    for square in objects:
        add_square(fig, ax, square)

    pyplot.show()

if __name__ == "__main__" : main()
