import requests
import argparse


# this function checks if the API key is valid (contain 64 characters) or not.
def check_key(api_key):
    if len(api_key) == 64:
        print("Valid key\n")
        return True
    else:
        print("Invalid key!\n")
        return False


# this function checks if the file exist inside the directory, if not it will print error.
def check_file(file_name):
    try:
        f = open(file_name)
        f.close()
        return True
    except IOError:
        print("File does not exist\n")
        return False


# using requests library to sent HTTP requests to VT with the required parameters.
# the method used is GET method to receive response and analyze it.
# after parsing it to json format, this function extract the resource code that will determine if the hash can be
# found on VT db.
def analyze_sha1(key, hash):
    parameters = {"apikey": key, "resource": hash}
    url = requests.get("https://www.virustotal.com/vtapi/v2/file/report", params=parameters)
    j_resp = url.json()
    response = int(j_resp.get("response_code"))
    # data st. for all the engines and their values
    scans = []
    values = []
    scans = j_resp.get("scans")

    if response == 0:
        print("Hash file not found on Virus Total data base\n")

    elif response == 1:
        positives = int(j_resp.get("positives"))
        # searching for Microsoft engine or Check Point engine
        # with the condition of their detection to be True
        for scan in scans:
            values = scans[scan]
            if (scan == 'Microsoft' or scan == "ZoneAlarm by Check Point") and values['detected'] == True:
                print("Check Point or Microsoft engine detected this file as Malicious\n")
                exit()
        # if non of the engines above has detected it as malicious, this condition will check if the engine count
        # is at least 50
        if positives >= 50:
            print("Malicious\n")
        else:
            print("Not Malicious\n")


# using VT API, this function will checks a certain hash file (specifically SHA-1) on Virus Total
# data base and returns if the hash file is malicious (over 50 engines detects it as malicious) or not.
if __name__ == '__main__':
    # two arguments are required to run this program: Valid API key and path to file
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--api_key", required=True)
    parser.add_argument("-i", "--input", required=True)
    args = parser.parse_args()

    if check_key(args.api_key) and check_file(args.input):
        print("Processing\n")
        f = open(args.input, "r")
        # this section can handles file with one SHA-1 and can be transform to handles file with multiple SHA-1.
        sha1_input = f.readline()

        analyze_sha1(args.api_key, sha1_input)

    # if the api key or the file are invalid an error will be printed
    else:
        print("The key or hash file you provided are invalid")