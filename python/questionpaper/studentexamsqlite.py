#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      NTalukdar
#
# Created:     14-01-2013
# Copyright:   (c) NTalukdar 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sqlite3
import string
import time
import logging


class MyDataBase:
    """ Class to interface to underlying database. """
    def __init__(self, dbfilename):
        self.dbfile = dbfilename
        self.dbcon = sqlite3.connect(self.dbfile)
        self.dbcursor = self.dbcon.cursor()

        self.caches = {}
        # populate caches
        self.populatecache()

        self.nextvalues = {}
        """ next id for various elements """

        self.dbcursor.execute("select name, value from nextvalue")
        allr = self.dbcursor.fetchall()
        for i in allr:
            self.nextvalues[i[0]] = i[1]

        self.subjects = {}
        """ Cache for the subjects and corresponding supbject id. """
        self.dbcursor.execute("select subjectid, name from subjects")
        allr = self.dbcursor.fetchall()
        for i in allr:
            self.subjects[i[0]] = i[1]

        self.questionoptions = ['option1', 'option2', 'option3', 'option4', \
                                'option5', 'correctoption']

        self.validqtypeid = [1, 2]

    def addstudent(self, name, lastname):
        """
        Adds a student record.
        Returns True if successfully added
        """
        tempname = name.lower()
        templastname = lastname.lower()
        fullname = tempname + " " + templastname
        self.dbcursor.execute("select * from students")
        allr = self.dbcursor.fetchall()
        for r in allr:
            if r[0].lower() == fullname:
                return False
        studentname = name + " " + lastname
        self.dbcursor.execute("insert into students values('" + studentname + \
            "', " + str(self.nextvalues['studentid']) + " )")
        self.nextvalues['studentid'] += 1
        try:
            self.dbcursor.execute("update nextvalue set value=" + \
                str(self.nextvalues['studentid']) + " where name='studentid'")
            self.dbcon.commit()
        except squlite3.Error as e:
            print(e.args[0])
            return False

        return True

    def addsubject(self, name):
        """
        Add Subjects.
        Returns True on success, False on Failure
        """
        tempname = name.lower()
        try:
            self.dbcursor.execute("select * from subjects")
            allr = self.dbcursor.fetchall()
            for r in allr:
                if r[1].lower() == tempname:
                    return False
            self.dbcursor.execute("insert into subjects values(" + \
                str(self.nextvalues['subjectid']) + ", '" + tempname +"')")
            self.nextvalues['subjectid'] += 1
            self.dbcursor.execute("update nextvalue set value=" + \
                str(self.nextvalues['subjectid']) + " where name='subjectid'")
            self.dbcon.commit()
        except sqlite3.Error as e:
            print(e.args[0])
            return False

        return True

    def getnextqnumber(self, paperid):
        try:
            statement = "select questionnumber from questionpaper where " \
                "paperid=" + str(paperid);
            self.dbcursor.execute(statement)
            r = self.dbcursor.fetchone()
            nextquestion = r[0]
            return nextquestion
        except sqlite3.Error as e:
            print(e.args[0])
            return -1
        return 0

    def addquestion(self, question, paperid , nextqnum):
        """ Adds a question, but doesn't commit """
        qkey = [ 'qtext' , 'questiontypeid', 'mark']
        for k in qkey:
            if k not in question:
                return False

        if question['questiontypeid'] !=2 and question['questiontypeid'] !=1:
            return False

        optionstring = ""

        if  2 == question['questiontypeid']:
            for opt in self.questionoptions:
                if opt not in question:
                    return False
            for opt in self.questionoptions:
                optionstring += ", " + question[opt]
        else:
            optionstring = " , NULL, NULL, NULL, NULL, NULL, NULL "

        try:
            statement = "insert into questions values(" + \
                str(paperid) + ", '" + question['qtext'] + "', " + \
                str(nextqnum) + " , " + \
                str(question['questiontypeid']) + optionstring + ", " +\
                str(question['mark']) + " )"

            self.dbcursor.execute(statement)

        except sqlite3.Error as e:
            print(e.args[0])
            return False
        return True

    def paperexist(self, paperid):
        """ Checks if a question paper with the paperid exist """
        statement = "select paperid from questionpaper where paperid=" + \
                str(paperid)
        self.dbcursor.execute(statement)
        allr = self.dbcursor.fetchall()
        if (len(allr) != 1):
            return False
        return True

    def addquestions(self, questions, paperid):
        """
        Adds a batch of questions.
        Returns the number of questions successfully added
        Commits after all the questions are added
        """
        if (not self.paperexist(paperid)):
            return False
        numquestionadded = 0
        nextqnum = self.getnextqnumber(paperid)

        for q in questions:
            if (self.addquestion( q, paperid, nextqnum)):
                numquestionadded += 1
                nextqnum += 1

        if (numquestionadded > 0):
            try:
                statement = "update questionpaper set questionnumber=" + \
                    str(nextqnum) + " where paperid=" + str(paperid)
                self.dbcursor.execute(statement)
                self.dbcon.commit()
            except sqlite3.Error as e:
                return 0

        return numquestionadded

    def addqpaper(self, subjectid, description):
        """
        Adds a question paper
        On success return paperid of the added question paper
        On failure returns -1
        """
        if subjectid not in self.subjects:
            return-1

        paperid = -1

        try:
            statement = "insert into questionpaper values(" + \
                str(self.nextvalues['paperid']) + ", '" + description +"'," + \
                str(subjectid) +", 0, " + "(SELECT strftime('%s','now')) )"
            self.dbcursor.execute(statement)
            nextpaperid = self.nextvalues['paperid'] + 1
            statement = "update nextvalue set value=" + str(nextpaperid) + \
                " where name='paperid'"
            self.dbcursor.execute(statement)
            self.dbcon.commit()
            self.nextvalues['paperid'] = nextpaperid
            paperid = nextpaperid -1

        except sqlite3.Error as e:
            print(e.args[0])

        return paperid

    def getquestions(self, paperid):
        if (not self.paperexist(paperid)):
            return False
        statement = "select * from questions where paperid=" + str(paperid)
        try:
            self.dbcursor.execute(statement)
            allqs = self.dbcursor.fetchall()
            return allqs

        except sqlite3.Error as e:
            print(e.args[0])
            return False

        return True

    def valid(self, keyname, onevalue):
        if keyname not in self.caches:
            return False
        if onevalue not in self.caches[keyname] :
            return False

        return True

    def populatecache(self):
        try:
            statement = "select studentid, name from students"
            self.dbcursor.execute(statement)
            allr = self.dbcursor.fetchall()
            self.caches['studentids'] = {}
            for r in allr:
                self.caches['studentids'][r[0]] = r[1]

            statement = "select subjectid, name from subjects"
            self.dbcursor.execute(statement)
            allr = self.dbcursor.fetchall()
            self.caches['subjects'] = {}
            for r in allr:
                self.caches['subjects'][r[0]] = r[1]

            statement = "select paperid from questionpaper"
            self.dbcursor.execute(statement)
            allr = self.dbcursor.fetchall()
            self.caches['paperids'] = []
            for r in allr:
                self.caches['paperids'].append(r[0])

            statement = "select * from studentschedule"
            self.dbcursor.execute(statement)
            allr = self.dbcursor.fetchall()
            self.caches['studentschedules'] = {}
            for r in allr:
                self.caches['studentschedules'][r[0]] = {\
                    'studentid' : r[1], 'paperid' : r[2], 'closed' : r[3], \
                    'createdtime' : r[4], 'sheduledtime' : r[5] }



        except sqlite3.Error as e:
            return False

    def createschedule(self, studentid, paperid, scheduletime):
        if not self.valid('studentids', studentid ):
            return False
        if not self.valid('paperids', paperid):
            return false
        curtime = int(time.time())
        if (scheduletime < curtime):
            return False

        # So everything is fine till now
        try:
            nextsch = str(self.nextvalues['scheduleid'])
            statement = "insert into studentschedule values(" + nextsch + ", "\
                + str(studentid)  + ", " + str(paperid) + ", 0, " + \
                "(SELECT strftime('%s','now')) , " + str(scheduletime) + " )"

            self.dbcursor.execute(statement)
            nextsch = str(self.nextvalues['scheduleid'] + 1)
            statement = "update nextvalue set value=" + nextsch + \
                    " where name='scheduleid'"
            self.dbcursor.execute(statement)
            self.dbcon.commit()
            self.nextvalues['scheduleid'] += 1
        except sqlite3.Error as e:
            print(e.args[0])
            return False

        return True

    def addanswers(self, paperid, studentid, scheduleid, answers, anspaperid):
        if not self.valid('studentschedules', scheduleid):
            return False
        if not self.valid('studentids', studentid):
            return False
        if not self.valid('paperids', paperid):
            return False

        # Check if question numbers are correct
        values = ""
        i  = 0;
        for r in answers:
            if  i == 1:
                values += " , "
            else:
                i = 1
            values += str(r['questionnumber'])

        if values == "":
            return
        statement = "select questionnumber from questionpaper where " \
            " questionnumber not in (" + values + " )  and paperid=" + paperid
        try:
            self.dbcursor.execute(statement)
            allr = self.dbcursor.fetchall()
            if len(allr) > 0:
                return False
        except sqlite3.Error as e:
            return False

        # Now add the questions
        statement = "insert into answers values "
        addcomma = 0

        for r in answers:
            if addcomma == 1:
                statement += ", "
            else:
                addcomma = 1
            statement += "(%d, %d, %s , 0 , 0)" %(anspaperid, r['questionnumber'], \
                            r['ans'])
        if addcomma:
            try:
                self.dbcursor.execute(statement)
                self.dbcon.commit()
            except sqlite3.Error as e:
                return False

        return True

    def addanswerpaper(self, paperid, studentid, scheduleid, answers):
        self.addanswers(1, 1, 1, 1)
        if not self.valid('paperids', paperid):
            return False, -1
        if not self.valid('studentids', studentid):
            return False, -1
        if not self.valid('studentschedules', scheduleid):
            return False, -1

        # check if the student already added an answerpaper for the question
        # paper which is not evaluated. If it is there than return the old
        # paper id

        statement = "select answerpaperid, evaluated from answerpaper where " \
            " studentid=" + str(studentid) + " and paperid=" + str(paperid)

        self.dbcursor.execute(statement)
        allr = self.dbcursor.fetchall()
        for r in allr:
            if r[1] == 0:
                return False, r[0]

        nextap = self.nextvalues['answerpaperid']
        statement = "insert into answerpaper values(%d,%d,%d,%d,%d,%d,%d)" \
         %(paperid, studentid, scheduleid,nextap,0,0, int(time.time()))
        self.dbcursor.execute(statement)

        statement = "update nextvalue set value=%d where name='answerpaperid'"\
                %(nextap + 1)
        self.dbcursor.execute(statement)

        return True, self.nextvalues['answerpaperid']

    def addanswerforpaper(self, paperid, studentid, scheduleid, answers):

        status, anspaperid = self.addanswerpaper(paperid,studentid, scheduleid)
        if not status:
            return False
        status = self.addanswerforpaper(paperid, studentid, scheduleid, answers\
                    , anspaperid)

        if (status):
            try:

                self.dbconn.commit()
                self.nextvalues['answerpaperid'] += 1
                self.autoevaluate(anspaperid)
                return status
            except sqlite3.Error as e:
                print(e.args[0])
                return False
        return status

    def autoevaluate(self, answerpaperid):
        """
        All the optional papers are auto evaluated as we already know the
        correct option
        """

        pass

    def evaluate(self, answerpaperid):
        pass

    def __del__(self):
        self.dbcon.close()


def main():
    mydb = MyDataBase("d:\\abhiani\\\questions")
    mydb.addstudent("rang", "xBang")
    t = int(time.time()) + 860000
    mydb.createschedule(1, 50, t)
    mydb.addanswerpaper(50, 1, 19)
    """
    paperid = mydb.addqpaper(1, 'My Paper for physics')
    print("paperid added " + str(paperid))
    print("Adding questions to paperid=" + str(paperid))

    i = 1
    x = []
    while (i < 4):
        question = {}
        question['qtext'] = "Which is the most populous country"
        question['questiontypeid'] = 2
        question['mark'] = 10
        question['option1'] = '\'China\''
        question['option2'] = '\'Nepal\''
        question['option3'] = '\'Bhutan\''
        question['option4'] = '\'Bangladesh\''
        question['option5'] = '\'Franch\''
        question['correctoption'] = str(1)
        x.append(question)
        i += 1
    mydb.addquestions(x, 40)
    y = mydb.getquestions(40)
    print(y)
    """
if __name__ == '__main__':
    main()
