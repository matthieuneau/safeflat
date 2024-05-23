import pickle

# Open the cookies file
with open("cookies.pkl", "rb") as file:
    # Load cookies from the file
    cookies = pickle.load(file)

    # Print each cookie in the file
    for cookie in cookies:
        print(cookie)
