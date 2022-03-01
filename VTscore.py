import requests
import argparse

# this function checks if the API key does not contain 64 characters its not valid.
def check_key(api_key):
    if len(api_key) == 64:
        print("Valid key\n")
        return True
    else:
        print("Invalid key!\n")
        return False


# this function checks if the file exist inside the directory, if not it will exit the program.
def check_file(file_name):
    try:
        f = open(file_name)
        print("Searching for file\n")
        f.close()
        return True
    except IOError:
        print("File does not exist\n")
        return False


def analyze_sha1(key, hash):
    print(key +"\n"+ hash)
    parameters = {"apikey": key, "resource": hash}
    url = requests.get("https://www.virustotal.com/vtapi/v2/file/report", params=parameters)
    j_resp = url.json()
    response = int(j_resp.get("response_code"))

    if response == 0:
        print("Unknown\n")
    elif response == 1:
        positives = int(j_resp.get("positives"))
        if positives >= 50:
            print("Malicious\n")
        else:
            print("Not malicious\n")

if __name__ == '__main__':
    # api key: 8abe0b4cd868be301d050be4dcfef73f34f41092063118f236f9cd203f9d0e54
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--api_key", required=True)
    parser.add_argument("-i", "--input", required=True)
    args = parser.parse_args()

    if check_key(args.api_key) and check_file(args.input):
        print("YAS")
        f = open(args.input, "r")
        # this section can handles file with one SHA-1 and can be transform to handles file with multiple SHA-1.
        sha1_input = f.readline()

        analyze_sha1(args.api_key, sha1_input)

    else:
        print("NOOO")