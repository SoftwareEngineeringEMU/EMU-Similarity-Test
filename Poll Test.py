# By Isaac Andreas
# Help from Caleb H
#This program will look at "EMU Similarity Test".csv and email each person's top five similar people at EMU.
import numpy as np
import pandas as pd
import time

data = pd.read_csv('EMU Similarity Test.csv')

#Variables
responses = len(data)
similarities = 0
average = 0
max_points = 45

#Dictionary of all pairs
record = {}
top5 = {}
for n1 in range(responses):
    top5[n1] = []
    for n2 in range(responses):
        #add a > to eliminate repeats below
        if n1==n2: continue
        for column in data.columns.tolist():

        #To compare easy, non-spectrum, single answer questions
            if data[column][n1] == data[column][n2]:
                if column != "Timestamp" and column != "Username":
                    similarities += 1
        #To compare spectrum questions
            if column == "How happy are you at EMU?":
                if data[column][n1] == data[column][n2]:
                    if abs(int(data[column][n1]) - int(data[column][n2])) == 1:
                        similarities += .5

        #Add weight to specific questions
            #Bonus for same Enneagram
            elif column == "What is your Enneagram type? ":
                if data[column][n1] == data[column][n2]:
                    similarities += 1
            #Small bonus for maybe children
            elif column == "Do you want children?":
                if data[column][n1] != data[column][n2]:
                    if data[column][n1] == "Maybe" or data[column][n2] == "Maybe":
                        similarities += .5
            #Correct for third choice
            elif column == "There is a button that will instantly stop all future COVID-19 sickness and deaths, but it also kills you instantly. Would you press it?":
                if  data[column][n1] != "Yes" and data[column][n2] != "No"\
                and data[column][n2] != "Yes" and data[column][n1] != "No":
                    similarities += 1

        #To compare questions with multiple check boxes
            elif  column == 'What are your favorite EMU sports? Select all that apply.' or \
                column == "What are your favorite music genres? Select all that apply.":
                if not isinstance(data[column][n2], float) and not isinstance(data[column][n1], float):
                    dat0 = data[column][n1].split(",")
                    dat1 = data[column][n2].split(",")
                    common = 0
                    for i in range(len(dat0)):
                        for j in range(len(dat1)):
                            if dat0[i] == dat1[j]:
                                common += 1
                    agree = 14 - len(dat0) - len(dat1) + common
                    similarities += agree / 2
                    if data[column][n1] == data[column][n2]: #Correct for double count
                        similarities -= 1
            elif column == "What makes you laugh out loud? Select all that apply." or \
                 column == "What kinds of jokes do you make? Select all that apply.":
                if not isinstance(data[column][n2], float) and not isinstance(data[column][n1], float):
                    dat0 = data[column][n1].split(",")
                    dat1 = data[column][n2].split(",")
                    common = 0
                    for i in range(len(dat0)):
                        for j in range(len(dat1)):
                            if dat0[i] == dat1[j]:
                                common += 1
                    agree = 6 - len(dat0) - len(dat1) + common
                    similarities += agree/2
                    if data[column][n1] == data[column][n2]: #correct for double count
                        similarities -= 1

                    if not isinstance(data[column][n2], float) and not isinstance(data[column][n1], float):
                        dat0 = data[column][n1].split(",")
                        dat1 = data[column][n2].split(",")
                        for i in range(len(dat0)):
                            for j in range(len(dat1)):
                                if dat0[i] == dat1[j]:
                                    similarities += 1

    # Turn on for visible emails not numbers
        # if not isinstance(data['Username'][n2], float) and not isinstance(data['Username'][n1], float):
        #     name1 = data['Username'][n1].split("@")[0]
        #     name2 = data['Username'][n2].split("@")[0]
        #     record[name1, name2] = similarities
        # else:
        record[n1, n2] = similarities
        top5[n1].append((similarities,n2))
        # if  top5[n1] == 0 or similarities > top5[n1][0]:
        #     top5[n1] = (n2, similarities)
        average += similarities
        similarities = 0

average = average/len(record)
print(top5)
#[print(key[0], "&", key[1],':',value) for key, value in record.items()]
print("Total Resonses:", responses)

#Finds most and least similar pair
recordsort = sorted(record.items(), key = lambda kv:(kv[1], kv[0]))
print("The most similar pair is ", recordsort[-1][0], "with ", recordsort[-1][1]/max_points*100, "%")
print("The least similar pair is ", recordsort[0][0], "with ", recordsort[0][1]/max_points*100, "%")

# -----------------------------------------------------------------------------------------------------------------------
# This deals with sending the emails
import smtplib, ssl

def sendmail(person2, outtext2):
    port = 465
    server = smtplib.SMTP_SSL("smtp.gmail.com", port)

    password = input("Type your password and press enter: ")
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("pollingemu@gmail.com", password)

        sender_email = "pollingemu@gmail.com"
        receiver_email = data["Username"][person2]

        printname = ''
        for name in range(0, len(outtext2)):
            printname = str(data['Username'][outtext2[name][1]]) + " with " + str([outtext2[name][0]][0]) + ' points\n' + printname

        message = """\
        EMU Similarity Test (Trial 3)
Hi """ + str(data['Username'][person2].split(".")[0]) + str(
            responses) + ",\n\nThank you for taking the EMU Similarity Test! Your 5 most similar people at EMU are: \n\n" + \
            str(printname) + "\nThe total similarity points possible are " + str(max_points) + ". \nThe average score between two people was " + \
            str(round(average,1)) + "\n\nIf you would like to see which similarities you share with these people, please go to this link:\n\
            https://forms.gle/MPL5NWp6EgJ8DG5h9" + \
            "\n\nWarmly,\nThe Similarity Test Committee\n"


        try:
            time.sleep(1)
            server.sendmail(sender_email, receiver_email, message)  # This actually sends the code
            return ''
        except Exception:
            return data["Username"][person2]


# -----------------------------------------------------------------------------------------------------------------------

#Finds top 5 for each person:
print("top 5:")
failmail = ''
for person in range(len(top5)):
    print(data['Username'][person].split(".")[0], end ='')
    top5[person].sort(key=lambda x: x[0])
    outtext = top5[person][-5:]
    print(outtext)
    failmail += sendmail(person, outtext)       #sends the emails
print("Unsuccessful emails were: " + failmail)


#Make sure to save the .csv file named "EMU  Similarity  Test" (Check for double spaces)


