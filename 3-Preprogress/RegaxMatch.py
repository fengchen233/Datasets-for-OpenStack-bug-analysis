# coding=utf-8
import xml.dom.minidom
import re
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class myxml:
    __reEB = []
    __reS2R = []
    __path = "original_data/9122_bug_xml1"

    def __init__(self, path):
        self.__path = path

    #主要正则匹配任务
    def mainTask(self,output):
        fileList = self.getFileList(self.__path)
        print fileList
        num = 0
        for filename in fileList:
            self.checkBugXml(filename,output)
            print "================================================================================================\n"
            num += 1
            print num

    def  BuR_F(self,bugInputPath,bugOutPath):
        bugfileList = self.getFileList(bugInputPath)
        for filename in bugfileList:
            flag = false
            dom = xml.dom.minidom.parse(filename)
            sentences = dom.documentElement.getElementsByTagName("sentence")
            for sent in sentences:
                result = checkEB_S2RSentence(sent))
                if result==true:
                    flag = true
                    break
            shutil.copyfile(filename, bugInputPath)


    def checkBugXml(self, fileName,output):
        eb_flag ="0eb";
        s2r_flag = "0s2r";
        dom = xml.dom.minidom.parse(fileName)
        #输出xml对象
        doc = xml.dom.minidom.Document()
        wroot = doc.createElement('bug')
        idnode = doc.createElement("id")
        bug = dom.getElementsByTagName("bug")
        doc.appendChild(wroot)
        bugid = bug[0].getAttribute("id")
        idnode.appendChild(doc.createTextNode(bugid))
        titlenode = doc.createElement("title")
        titlenode.appendChild(doc.createTextNode(dom.getElementsByTagName("title")[0].firstChild.data))
        wroot.appendChild(idnode)
        wroot.appendChild(titlenode)

        print fileName
        # 得到文档元素对象
        root = dom.documentElement
        sentences = root.getElementsByTagName("sentence")
        ss = ""
        for sent in sentences:
            child = sent.firstChild
            if child:
                ss = sent.firstChild.data.encode("UTF-8")
            sentencenode = doc.createElement("sentence")
            sentencenode.appendChild(doc.createTextNode(ss))
            if (self.checkEBSentence(ss)):
                sentencenode.setAttribute("eb", "x")
                print "true eb " + ss
                eb_flag = "1eb";
            else:
                print "false eb " + ss
                sentencenode.setAttribute("eb", "")

            if (self.checkS2RSentence(ss)):
                sentencenode.setAttribute("s2r", "x")
                print "true s2r " + ss
                s2r_flag = "1s2r";
            else:
                sentencenode.setAttribute("s2r", "")
                print "false s2r " + ss
            wroot.appendChild(sentencenode)
        bugid = "bug" + bug[0].getAttribute("id")
        if(eb_flag =="1eb" or s2r_flag =="1s2r"):
            f = codecs.open(output + eb_flag + s2r_flag + bugid + ".xml", 'w', encoding='utf-8')
            f.write(doc.toprettyxml(indent='    ', encoding='UTF-8'))
            f.close();



    def checkS2RSentence(self, sentence):
        matchNum = 0
        for reg in self.__reS2R:
            pattern = re.compile(reg)
            match = pattern.match(sentence)
            if match:
                matchNum += 1
        #print matchNum;

        if (matchNum >= 1):
            return True
        else:
            return False

    def checkEBSentence(self, sentence=""):
        matchNum = 0
        for reg in self.__reEB:
            pattern = re.compile(reg, flags=re.IGNORECASE)
            match = pattern.findall(sentence)
            if match:
                matchNum += 1

        reg1 = r'\bmust\b'
        reg2 = r'\bcould\b'
        reg3 = r'\bshould\b'
        pattern1 = re.compile(reg1, flags=re.IGNORECASE)
        pattern2 = re.compile(reg2, flags=re.IGNORECASE)
        pattern3 = re.compile(reg3, flags=re.IGNORECASE)
        search1 = pattern1.findall(sentence)
        search2 = pattern2.findall(sentence)
        search3 = pattern3.findall(sentence)
        if search1:
            matchNum += 1
        if search1:
            matchNum += 1
        if search1:
            matchNum += 1
        if (matchNum >= 1):
            return True
        else:
            return False

    def isSubString(self, SubStrList, Str):
        flag = True
        for substr in SubStrList:
            if not (substr in Str):
                flag = False

        return flag
        # ~ #----------------------------------------------------------------------

    def getFileList(self, FindPath, FlagStr=[]):
        import os
        FileList = []
        FileNames = os.listdir(FindPath)
        if (len(FileNames) > 0):
            for fn in FileNames:
                if (len(FlagStr) > 0):
                    # 返回指定类型的文件名
                    if (self.isSubString(FlagStr, fn)):
                        fullfilename = os.path.join(FindPath, fn)
                        FileList.append(fullfilename)
                else:
                    # 默认直接返回所有文件名
                    fullfilename = os.path.join(FindPath, fn)
                    FileList.append(fullfilename)

                    # 对文件名排序
        if (len(FileList) > 0):
            FileList.sort()

        return FileList

    def initREStr(self):
        ebFile = open("config/EB.txt")  # 读取EB的正则表达式
        try:
            lines = ebFile.readlines(100)
            for line in lines:
                str = line.replace("\n", "")
                self.__reEB.append(str)
        finally:
            ebFile.close()
        s2rFile = open("config/S2R.txt")
        try:
            lines = s2rFile.readlines(100)  # 读取S2R的正则表达式
            for line in lines:
                sstr = line.replace("\n", "")
                self.__reS2R.append(sstr)

        finally:
            ebFile.close()
       # print self.__reEB
       #print self.__reS2R

if __name__ == '__main__':
    myxml0 = myxml("D:/NLP_prase/bug/importance_high/1_removed_log")
    myxml0.initREStr()

    myxml0.mainTask("output/1203/high/")

    myxml1 = myxml("D:/NLP_prase/bug/importance_medium/1_removed_log")
    myxml1.initREStr()

    myxml1.mainTask("output/1203/mid/")


