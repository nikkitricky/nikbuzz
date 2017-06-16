"""
    @authors: Nishanth and Nikhith !!
"""
from pycricbuzz import Cricbuzz
import json
import sys
""" Writing a CLI for Live score """
try:
    cric_obj = Cricbuzz() # cric_obj contains object instance of Cricbuzz Class
    matches = cric_obj.matches()
except:
    print "Connection dengindi bey!"
    sys.exit(0)

 # matches func is returning List of dictionaries
""" Key items in match dict : 1) status -- ex) Starts on Jun 15 at 09:30 GMT
                              2) mnum   -- ex) 2nd Semi-Final (A2 VS B1)
                              3) mchdesc-- ex) BAN vs IND
                              4) srs    -- ex) ICC Champions Trophy, 2017
                              5) mchstate- ex) preview / abandon / Result / complete
                              6) type   -- ex) ODI
                              7) id     -- ex) 4 / 6 (anything random given)
                              """
"""CLI must contain commands for
        -- current matches
        -- selecting match by match id
        -- getCommentary
"""
def upcomingmatches():
    """Prints upcoming matches list
       """
    count = 1
    for match in matches:
        if match['mchstate'] == "preview":
            print str(count)+". "+str(match['mchdesc'])+ " - "+ str(match['srs'])+"- - "+str(match['status'])
            count = count + 1

def currentlive():
    """Prints Current LIVE MATCHES"""
    count = 1
    for match in matches:
        #print str(match['mchdesc']) + "      match id: " + str(match['mchstate'])
        if (match['mchstate'] == "innings break" ) :
            print str(match['mchdesc'])+"      match id: "+str(match['id'])
            count = count + 1
        if (match['mchstate'] == "inprogress" ) :
            print str(match['mchdesc'])+"      match id: "+str(match['id'])
            count = count + 1
        if match['mchstate'] == "delay":
            print str(match['mchdesc'])+" -> match has been delayed due to rain..! Enjoy the drizzle..!!"
    if count == 1:
        print "\nNO LIVE MATCHES RIGHT NOW!\n"
        print "UPCOMING MATCHES TODAY!"
        upcomingmatches()
    else:
        id = input("Enter corresponding match id : ")
        gotolive(id)
        return id


def calculate_runrate(runs, overs):
    balls = str(overs)
    arr = balls.split('.')
    if len(arr) == 2:
        rr = float(int(arr[0])*6)+int(arr[1])
    else:
        rr = float(int(arr[0])*6)
    return (float(runs)/rr)*6


def gotolive(matchid):

    batobj = cric_obj.livescore(matchid)['batting']
    bowlobj = cric_obj.livescore(matchid)['bowling']
    print "\n                "+str(batobj['team'])+" vs "+str(bowlobj['team'])+"\n"
    print "     "+str(cric_obj.livescore(matchid)['matchinfo']['status'])+"\n"
    if (bowlobj['score'] == []):
        print "1st INNINGS: "+str(batobj['team'])+" => "+str(batobj['score'][0]['runs'])+"/"+str(batobj['score'][0]['wickets'])+" ("+str(batobj['score'][0]['overs'])+" Overs)"
        print "Batting:"
        try:
            print "    " + str(batobj['batsman'][0]['name']) + " : " + str(batobj['batsman'][0]['runs']) + " (" + str(batobj['batsman'][0]['balls']) + ")"
            print "    " + str(batobj['batsman'][1]['name']) + " : " + str(batobj['batsman'][1]['runs']) + " (" + str(batobj['batsman'][1]['balls']) + ")"
        except:
            print "Wicket!!!!"
        print "Bowling:"
        print "    " + str(bowlobj['bowler'][0]['name']) + " : " + str(bowlobj['bowler'][0]['runs']) + " /" + str(bowlobj['bowler'][0]['wickets']) + " (" + str(bowlobj['bowler'][0]['overs']) + ")"
        print "    " + str(bowlobj['bowler'][1]['name']) + " : " + str(bowlobj['bowler'][1]['runs']) + " /" + str(bowlobj['bowler'][1]['wickets']) + " (" + str(bowlobj['bowler'][1]['overs']) + ")"
        print "Runrate:"
        print '    {:1.2f}'.format(calculate_runrate(str(batobj['score'][0]['runs']),str(batobj['score'][0]['overs'])))
    else:
        print "1st INNINGS: "+str(bowlobj['team'])+" => "+str(bowlobj['score'][0]['runs'])+"/"+str(bowlobj['score'][0]['wickets'])+" ("+str(bowlobj['score'][0]['overs'])+" Overs)"
        print "2nd INNINGS: "+str(batobj['team'])+" => "+str(batobj['score'][0]['runs'])+"/"+str(batobj['score'][0]['wickets'])+" ("+str(batobj['score'][0]['overs'])+" Overs)"
        print "Batting:"
        try:
            print "    "+str(batobj['batsman'][0]['name'])+" : "+str(batobj['batsman'][0]['runs'])+" ("+str(batobj['batsman'][0]['balls'])+")"
            print "    " + str(batobj['batsman'][1]['name']) + " : " + str(batobj['batsman'][1]['runs']) + " (" + str(batobj['batsman'][1]['balls']) + ")"
        except:
            print "Wicket!!"
        print "Bowling:"
        print "    " + str(bowlobj['bowler'][0]['name']) + " : " + str(bowlobj['bowler'][0]['runs'])+" /"+str(bowlobj['bowler'][0]['wickets']) + " (" + str(bowlobj['bowler'][0]['overs']) + ")"
        print "    " + str(bowlobj['bowler'][1]['name']) + " : " + str(bowlobj['bowler'][1]['runs']) + " /" + str(bowlobj['bowler'][1]['wickets']) + " (" + str(bowlobj['bowler'][1]['overs']) + ")"
        print "Summary:"
        print "    " + str(cric_obj.livescore(4)['matchinfo']['status'])


def last12Balls():
    pass

def commentary(matchid):
    print "\nCommentary: "
    try:
        for i in range(6):
            print "     "+str(cric_obj.commentary(matchid)['commentary'][i])
        print "************************************************************************************************"
    except:
        print "No running commentary.. now..!!"
if __name__ == '__main__':
    matchid=currentlive()
    commentary(matchid)
