#First time setup for easy use

#Make the variable SETCODE = your desired set to populate the database
#Then save the script file
#finally run the script until completion

from mtgDB import mtgDB

setcode = 'RNA'

#Create the DB
mtgDB.InitializeDB()

#Populate with SetCode from above
mtgDB.UpdateSet(setcode)
