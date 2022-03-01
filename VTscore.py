
def check_if_valid(sha1_string):
    size = len(sha1_string)
    print("the size is: " + str(size))

    if size != 40:
        print("invalid sha1")
        return False
    else:
        print("The sha1 is: " + sha1_string)
        return True

# User need to choose how to upload sha1.
# The user can type (or paste) directly to the terminal or he can upload text file containing only one sha1.

if __name__ == '__main__':

    print("please choose method for uploading sha1\n1 for uploading text file\n2 for manual typing")
    method = input()

    # if the user choose method 1, the user need to insert sha1 directly to the terminal
    if method == '1':
        print("you choose " + method)

        sha1_input = input("please type sha1\n")
        # size check; if the sha1 does not contain 40 characters its invalid sha1.
        if check_if_valid(sha1_input):
            print("valid")

    # user must create text file named sha1 with only 1 sha1.
    # once the user type 2 the file will upload automatically
    if method == '2':
        print("you choose " + method)
        print("please upload text file")
        f = open("sha1.txt", "r")
        sha1_input = f.read()
        check_if_valid(sha1_input)
        print("the sha1 from the text file is: " + sha1_input)