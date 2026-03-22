import os
import re

class Session:
    def __init__ (self,snalID:str):
        self.changedwords={}#bfr:aft
        self.index=0
        self.txt=open("./kaidanhaku/scenalio/"+snalID+".txt",'r',encoding="utf-8")
        #lines=txt.readline()
        self.name=line2str(self.txt.readline(),"シナリオ名:","\\n")
        self.url=line2str(self.txt.readline(),"URL:","\\n")
        self.keyword=line2str(self.txt.readline(),"キーワード:","\\n").split(",")
        self.pwdSection:str=None
        self.resultSections=[]
    def __str__(self):
        return self.name
    def getKeyword(self):
        ans=""
        for kw in self.keyword:
            ans+=(re.sub("_@_","O: ",kw) if  "_@_" in kw  else "X: "+kw)+"\n"
        ans+=str(len(list(filter(lambda sc: "_@_" in sc,self.keyword))))+"/"+str(len(self.keyword))
        return ans
    def getSection(self):
        return self.pwdSection
    def nextSection(self):
        section=""
        line=self.txt.readline()
        if line =="" :
            section="終了"
        else:
            while ""!=line and "\n"!=line:
                section+=line
                line=self.txt.readline()
        if self.pwdSection is not None and self.pwdSection !="終了":
            print("書き込み")
            self.resultSections.append(self.pwdSection)
        self.pwdSection=section
        #return section

    def updateSection(self):
        self.pwdSection=self.replaceDictional(self.pwdSection)
        return self.pwdSection

    def addChangewords(self,bfr:str,aft:str):#{(aa:BB)(BB:cc)} → {(aa:cc)}
       self.changedwords[bfr]=aft
       kwresul=bfr in self.keyword
       if kwresul :
           self.keyword[self.keyword.index(bfr)]="_@_"+bfr
       return kwresul

    def getResultSections(self):#
        return  list(map(self.replaceDictional,self.resultSections))
    
    def replaceDictional(self,text:str):
        if any(self.changedwords):
            for bfr,aft in self.changedwords.items() :
                    text=re.sub(bfr,aft,text)
        return text
        
def line2str(text:str,stBfr:str,fnBfr:str,stAft="",fnAft=""):
    return re.sub(f"{fnBfr}$",fnAft,
                    re.sub(f"^{stBfr}",stAft,text))
#***********テスト***********
'''
tes=Session("id01")
flg=tes.addChangewords("男","漢")
'''

'''
python 文字列操作/正規表現
文字列操作
str_data = "abcde"
if("あ" in  str_data): #"あ" がstr_data内にある？
list=str_data.aplit('c') #["ab","de"]に分割
aft_str=re.sub('c',"C",str_data) #文字列置換(c→C)

正規表現
str="あ0123あabcd"
re.sub(r'\\W',"",str)   #\\W(英数字以外)を""へ
re.sub(r'^あ',)
'''