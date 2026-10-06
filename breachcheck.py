# Libraries

import requests
import matplotlib.pyplot as plt


print ("-------------------------------")


# API Variables & Input
while True:
    query = input("Email/Username : ").strip()
    if len(query) < 3:
        print("Please enter at least 3 characters.")
    elif any(c.isspace() for c in query):
        print("Spaces are not allowed.")
    elif not any(c.isalnum() for c in query):
        print("Must contain at least one letter or digit.")
    else:
        break

url = "https://leakcheck.io/api/public"
p={"check": query}
try:
    response = requests.get(url, params=p, timeout=10)
    code = response.status_code
    data = response.json()
except requests.exceptions.RequestException as e:
    print("API request failed:", e)
    exit(1)


# Filtering Variables
Lorigin=[]
years=[]
nob=[]


# Main
def main():
    print ("-------------------------------")
    print("Response :", code)
    if code == 200 and data.get("found", 0) > 0:
        print("-> Found : "+ str(len(data["sources"]))+"\n")
        print("Matches for this identifier were found in these sources:")
        print ("-------------------------------")
        for element in data["sources"]:
            breachdate=element["date"]
            if (breachdate==''):
                print(element["name"]+" ----> Unkown")
            else:
                print(element["name"]+" ----> "+breachdate)
                breachdate=breachdate[:breachdate.find("-")]
                Lorigin.append(breachdate)
        print ("-------------------------------")
        if ((2<=(len(data["sources"])))):
            graphcreation()
    elif code != 200:
        print("An error occured!", data.get("error", ""))
    else:
        print("-> No matches!")


# Graph Creation
def graphcreation():
    Lorigin.sort()
    years=list(set(Lorigin))
    years.sort()
    
    for i in years:
        nob.append((Lorigin.count(i)))


    fig, axes = plt.subplots(2, 1)
    axes[0].set_xlabel("Number of Breaches")
    axes[0].set_ylabel("Year")
    axes[0].set_title("Breaches Per Year Graph")

    axes[1].set_xlabel("Number of Breaches")
    axes[1].set_ylabel("Year")
    axes[1].set_title("Breaches Per Year Graph")

    axes[1].bar(years,nob)
    axes[0].plot(years,nob)

    plt.tight_layout()
    plt.show()




# Calling functions
main()
