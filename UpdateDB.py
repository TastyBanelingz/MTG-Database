#Script to update the Database 

#Make the variable SETCODE = your desired set to populate the database
#Then save the script file
#finally run the script until completion

#WARNING

#THIS SCRIPT HAS A LONG RUNTIME IF YOUR DATABASE IS FAIRLY EMPTY
#Plan to have this run for about few hours

from mtgDB import mtgDB

mtgDB.UpdateDB()

