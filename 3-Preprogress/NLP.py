#coding:utf-8
import os
import  xml.dom.minidom
import nltk
import  re

class s2r:
    #155

    S_SR_WHEN_AFTER = [
        r"when(.*)after.*", r"if(.*)after.*"
    ]

    #154
    S_SR_TRY = [
        r"try", r"have tried", r"has tried", r"has attempted to", r"have attempted to"

    ]

    #153
    S_SR_TRIGGERS = [
        r"\w+ing(.*)can trigger", r"\w+ing(.*)triggers"

    ]
    #150Sentence ending with an action to achieve a goal/purpose  需要对匹配到的词做词性判断是否为动词
    S_SR_PURPOSE_ACTION = [
        r"to\s(\w+)\s", r"in order to\s(\w+)\s"
    ]
    #149
    S_SR_MENU_SELECT = [
        r"select(s)?(.*)menu.*", r"select(s)?(.*)option(s)?.*"
    ]

    # 148 Sentence captures navigation through a menu
    S_SR_MENU_SELECT = [
        r"->(.*)->(.*)->(.*)->.*"
    ]
    #需要全部句子判断
    S_SR_COND_THEN_SEQ = [

        r"if(.*)then(.*)then.*", r"when(.*)when(.*)when.*", r"while(.*)while(.*)while.*"
    ]
    S_SR_COND_OBS = [
        r"if(.*),.*",  r"when(.*),.*",  r"whlie(.*),.*"
    ]

    #找到by后面那个词判断是否为动名词
    S_SR_BY_ACTION = [
        r"by\s(\w+)\s",
    ]

    #after那个词 是否为副词
    S_SR_AFTER = [

        r"After\s(\w+)\s"
    ]

    S_SR_ACTIONS_SEPARATOR = [
        r"-(.*)-(.*)-.*"

    ]

    P_SR_LABELED_PARAGRAPH = [

        r"What I have tried", r"steps to recreate", r"steps to reproduce",
    ]

    P_SR_COND_SEQUENCE = [
        r"^While|when"
    ]
    P_SR_COND_SEQUENCE_NOT = [
        r"do not", r"don't", r"did not", r"didn't", r"is not", r"is't", r"does not", r"doesn't", r"can not", r"can't" r"couldn't", r"could not", r"should not", r"shouldn't"

    ]

    def P_SR_ACTIONS_INF(self, str):
        pattern = r".*1\..*2\..*3\..*"
        if re.search(pattern, str, re.I): return 1
        return 0

    def P_SR_ACTIONS___(self,list):
        sum = 0
        fag = 1
        pattern = r".*-.*"
        for sent in list:
            if re.search(pattern, sent, re.I) and fag == 1:
                fag = 1
                sum += 1
            else:
                fag = 0
        if (sum >= 3):
            return 1
        else:
            return 0

    def P_SR_ACTIONS_MULTI_OBS_BEHAVIOR(self,list):
        sum = 0

        for sent in list:
            sentence = nltk.word_tokenize(sent)
            sentence = nltk.pos_tag(sentence)
            grammar = "S2R: {^<CC>?<VB>}"
            cp = nltk.RegexpParser(grammar)
            result = cp.parse(sentence)
            for subtree in result.subtrees():
                if subtree.label() == 'S2R':
                    sum = sum + 1
        #print  sum
        if (sum >= 3):
            return 1
        else:
            return 0

    def P_SR_HAVE_SEQUENCE(self,list):
        sum = 0
        pattern = r".*have|has|had.*"
        fag = 1
        for sent in list:
            if re.search(pattern, sent, re.I) and fag == 1:
                sum = sum + 1
                fag = 1
            else:
                fag = 0
        if (sum >= 2):
            return 1
        else:
            return 0

    def P_SR_SIMPLE_PAST(self,list):
        sum = 0

        for sent in list:
            sentence = nltk.word_tokenize(sent)
            sentence = nltk.pos_tag(sentence)
            grammar = "S2R: {<VBD>}"
            cp = nltk.RegexpParser(grammar)
            result = cp.parse(sentence)
            ##result.draw()
            for subtree in result.subtrees():
                if subtree.label() == 'S2R':
                    sum = sum + 1
        if (sum >= 3):
            return 1
        else:
            return 0

    def P_SR_TO_REPRO(self,list):
        n = 0
        pattern = r".*to repro(duce)?.*"
        for sent in list:
            n = n + 1
            if re.search(pattern, sent, re.I) and n < len(list):
                target = n
                sentence = nltk.word_tokenize(list[target])
                sentence = nltk.pos_tag(sentence)
                grammar = "S2R: {^<CC>?<VB>}"
                cp = nltk.RegexpParser(grammar)
                result = cp.parse(sentence)
                for subtree in result.subtrees():
                    if subtree.label() == 'S2R':
                        return 1
        return 0

    def S_SR_CONTINOUS_PRESENT(self,list):
        n = -1
        pattern = r".*('m|am|are|'re).*"
        for sent in list:
            n += 1
            if re.search(pattern, sent, re.I):
                sentence = nltk.word_tokenize(list[n])
                sentence = nltk.pos_tag(sentence)
                grammar = "S2R: {<VBP><VBG>}"
                cp = nltk.RegexpParser(grammar)
                result = cp.parse(sentence)
                for subtree in result.subtrees():
                    if subtree.label() == 'S2R':
                        return 1
        return 0

    def S_SR_SIMPLE_PRESENT_SUBORDINATES(self,list):

        for sent in list:
            sum = 0
            sentences = re.split(r"and|,", sent)
            if sentences:
                for sentence in sentences:
                    if sentence.strip() !="":
                        sentence = nltk.word_tokenize(sentence)
                        sentence = nltk.pos_tag(sentence)
                        grammar = "S2R: {<VB>}"
                        cp = nltk.RegexpParser(grammar)
                        result = cp.parse(sentence)
                        for subtree in result.subtrees():
                            if subtree.label() == 'S2R':
                                sum += 1

                if sum >= 2:
                    return 1

        return 0

    def S_SR_IMPERATIVE_SUBORDINATES(self,list):
        for sent in list:
            sentence = nltk.word_tokenize(sent)
            sentence = nltk.pos_tag(sentence)
            grammar = "S2R: {^<CC>?<VB>}"
            cp = nltk.RegexpParser(grammar)
            result = cp.parse(sentence)
            for subtree in result.subtrees():
                if subtree.label() == 'S2R':
                    sentences = re.split(r"and|,", sent)
                    if sentences:
                        for i in range(1, len(sentences)):
                            senten = nltk.word_tokenize(sentences[i])
                            senten = nltk.pos_tag(senten)
                            grammar = "S2R: {<VB>}"
                            cp = nltk.RegexpParser(grammar)
                            result = cp.parse(senten)
                            for subtree in result.subtrees():
                                if subtree.label() == 'S2R':
                                    return 1
        return 0


    def check_S_SR_PURPOSE_ACTION(self, description):
        result = 0
        if (self.checkReg(description, self.S_SR_PURPOSE_ACTION) !="-1"):
            des = self.checkReg(description, self.S_SR_PURPOSE_ACTION)
            #print des[0]
            text = nltk.pos_tag(nltk.word_tokenize(description))
            #print text
            for i in range(0,len(text)):
                if (text[i][0] == des[0]) :
                    if text[i-1][0] == "to":
                        if (text[i][1] == "VB"):
                            # print t
                            result = 1
                            break


        return result


    def check_S_SR_MENU_NAV(self,description):
        if(self.checkReg(description,self.S_SR_MENU_SELECT) !="-1"):
            #return self.checkReg(description,self.S_SR_MENU_SELECT)
            return 1
        else:
            return 0

    def check_S_SR_MENU_SELECT(self,description):
        if(self.checkReg(description,self.S_SR_MENU_SELECT) !="-1"):
            return 1
        else:
            return 0

    def check_S_SR_TRY(self,description):
        if(self.checkReg(description,self.S_SR_TRY)!="-1"):
            return 1
        else:
            return 0

    def checkS_SR_TRIGGERS(self,description):
        if(self.checkReg(description,self.S_SR_TRIGGERS)!="-1"):
            return 1
        else:
            return 0

    def check_S_SR_WHEN_AFTER(self,description):
        if(self.checkReg(description,self.S_SR_WHEN_AFTER)!="-1"):
            return 1
        else:
            return 0

    #检查正则匹配
    def checkReg(self, description, regs=[]):
        matchNum = 0
        name =""
        for reg in regs:
            pattern = re.compile(reg, flags=re.IGNORECASE+re.MULTILINE)
            match = pattern.findall(description)
            if match:
                matchNum = 1
                name = match
        if (matchNum == 1):
            #print "true"
            return name
        else:
            #print "false"
            return "-1"

    #返回一个bugFile的句子列表
    def getBugSentences(self,bugFile):
        dom = xml.dom.minidom.parse(bugFile)
        # 得到文档元素对象
        root = dom.documentElement
        id = dom.getElementsByTagName('bug')[0].getAttribute("id")
        # sentence = dom.getElementsByTagName('sentence')[0]
        description = dom.getElementsByTagName('description')[0]
        sentences = dom.getElementsByTagName("sentence")
        #print sentences[0].firstChild.data
        bugSentences = []
        for i in range(0, len(sentences)):
            #print i
            child = sentences[i].firstChild;
            if child.data.strip() !="":
                bugSentences.append(child.data)
            #else:
                #bugSentences.append("")
        return bugSentences

    def check_P_SR_COND_SEQUENCE(self,sentences):
        sum = 0
        fag = 1
        index = 0
        for i in range(0,len(sentences)):
            #sen =
           # print sentences[i]
            if (self.checkReg(sentences[i], self.P_SR_COND_SEQUENCE) !="-1" and fag == 1):
                sum = sum + 1
                fag = 1
                index = i
                #print index
               # print "ifsum:" + str(sum)
            else:
                fag = 0
        #print "ifsum:" + str(sum)
        if (sum >=2 and index <len(sentences)-1):
            if self.checkReg(sentences[index+1], self.P_SR_COND_SEQUENCE_NOT) != "-1":
                return 1
            else:
                return 0
        else:
            return 0



    #判断一个bugFile是不是S2R
    def IsS2R(self,bugFile):
        S2R = [];
        sentences = self.getBugSentences(bugFile)
        sentences_str = ""
        for sent in sentences:
            sentences_str += sent
        #num_S_SR_PURPOSE_ACTION = self.check_S_SR_PURPOSE_ACTION(sentences_str)#0
        num_S_SR_MENU_NAV = self.check_S_SR_MENU_NAV(sentences_str)#1
        num_check_S_SR_MENU_SELECT = self.check_S_SR_MENU_SELECT(sentences_str)#2
        num_check_S_SR_TRY = self.check_S_SR_TRY(sentences_str)#3
        num_checkS_SR_TRIGGERS = self.checkS_SR_TRIGGERS(sentences_str)#4
        num_check_S_SR_WHEN_AFTER = self.check_S_SR_WHEN_AFTER(sentences_str)#5
        num_check_P_SR_COND_SEQUENCE = self.check_P_SR_COND_SEQUENCE(sentences)#6
        S2R.append(0)
        S2R.append(num_S_SR_MENU_NAV)
        S2R.append(num_check_S_SR_MENU_SELECT)
        S2R.append(num_check_S_SR_TRY)
        S2R.append(num_checkS_SR_TRIGGERS)
        S2R.append(num_check_S_SR_WHEN_AFTER)
        S2R.append(num_check_P_SR_COND_SEQUENCE)

        #print "11223344----------------------------------------------------------------------"

        num_P_SR_ACTIONS_INF = self.P_SR_ACTIONS_INF(sentences_str)#7
        num_P_SR_ACTIONS___ = self.P_SR_ACTIONS___(sentences)#8
        num_P_SR_ACTIONS_MULTI_OBS_BEHAVIORS2R = self.P_SR_ACTIONS_MULTI_OBS_BEHAVIOR(sentences)#9
        num_P_SR_HAVE_SEQUENCE= self.P_SR_HAVE_SEQUENCE(sentences)#10
        num_P_SR_SIMPLE_PAST= self.P_SR_SIMPLE_PAST(sentences)#11
        num_P_SR_TO_REPRO = self.P_SR_TO_REPRO(sentences)#12
        num_S_SR_CONTINOUS_PRESENT = self.S_SR_CONTINOUS_PRESENT(sentences)#13
        #num_S_SR_SIMPLE_PRESENT_SUBORDINATES = self.S_SR_SIMPLE_PRESENT_SUBORDINATES(sentences)#14
        num_S_SR_IMPERATIVE_SUBORDINATES = self.S_SR_IMPERATIVE_SUBORDINATES(sentences)#15

        S2R.append(num_P_SR_ACTIONS_INF)
        S2R.append(num_P_SR_ACTIONS___)
        S2R.append(num_P_SR_ACTIONS_MULTI_OBS_BEHAVIORS2R)
        S2R.append(num_P_SR_HAVE_SEQUENCE)
        S2R.append(num_P_SR_SIMPLE_PAST)
        S2R.append(num_P_SR_TO_REPRO)
        S2R.append(num_S_SR_CONTINOUS_PRESENT)
        S2R.append(0)
        S2R.append(num_S_SR_IMPERATIVE_SUBORDINATES)
       # print S2R
        return S2R
    #测试所有的S2R
    def testAllS2R(self,pathFilePath,targetPath):
        pathDir = os.listdir(pathFilePath)
        allS2R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        for allDir in pathDir:
            #print allDir
            # 打开xml文档
            file =pathFilePath + "\\" + allDir
            print file
            s2rnum = self.IsS2R(file)
            for i in range(0,len(s2rnum)):
                allS2R[i] +=s2rnum[i]
            print allS2R
            if(1 in s2rnum):
                sourceF = os.path.join(pathFilePath, allDir)
                targetF = os.path.join(targetPath, allDir)
                open(targetF, "wb").write(open(sourceF, "rb").read())

        print "all info\n"
        print allS2R



if __name__ == '__main__':
   demo = s2r()
   bugpath = "bug/importance_critical/1_removed_log/"
   targetPath = "S2R/1203/critical/"
   demo.testAllS2R(bugpath,targetPath)
'''
   bugpath = "bug/importance_high/1_removed_log/"
   targetPath = "S2R/1203/high/"
   demo.testAllS2R(bugpath, targetPath)

   bugpath = "bug/importance_medium/1_removed_log/"
   targetPath = "S2R/1203/mid/"
   demo.testAllS2R(bugpath, targetPath)
   '''



