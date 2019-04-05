# python3
import os
import datetime
from shutil import copyfile
from collections import OrderedDict

class Report:
    def __init__(self, path=None):
        self.rawLines = []
        self.sections = OrderedDict()
        if path:
            self.setSections__(path)

    def setSections__(self, path):
        self.rawLines = [line.strip() for line in open(path)]
    
        # section name is initialized as HEADER for texts 
        # without section title written in a head of a file.
        sectionName = 'HEADER'
        content = []
        for line in self.rawLines:
            if line.startswith('#') and not line.startswith('##'):
                if content:
                    self.sections[sectionName] = '\n'.join(content)
                
                sectionName = line[2:] if line.startswith('# ') else line[1:]
                content = []
            else:
                content.append(line)
            
            self.sections[sectionName] = '\n'.join(content)

    def isSameAs(self, rep):
        return self.rawLines==rep.rawLines

    def exportAsString(self):
        line = ''
        for key,value in self.sections.items():
            line += '# %s\n%s\n'%(key, value)
        return line

newReportPath = 'new_report.md'
templatePath = 'template.md'
reportsDir = 'reports/'

def checkDir():
    # check dir environment and show error messages if problems occur
    
    # check template.md
    hasTemplate = os.path.exists(templatePath)
    if not hasTemplate:
        print('there is no %s.'%templatePath)
        print('please make %s or git pull again.'%templatePath)
        exit()

    # check new_report.md
    # if there is no new_report.md, copy from template.md
    if not os.path.exists(newReportPath):
        if hasTemplate:
            copyfile(templatePath, newReportPath)
            print('make %s by copying %s'%(newReportPath, templatePath))

    # check reports dir
    if not os.path.exists(reportsDir):
        os.mkdir(reportsDir)
        print('make %s directory to store daily reports.'%reportsDir)

def hasDiff(report1, report2):
    return not report1.isSameAs(report2)

def copyReport():
    # save file as name of date
    todayReportPath = reportsDir+str(datetime.date.today())+'.md'    

    # check file exists
    if os.path.exists(todayReportPath):
        print('Today\'s report already exists.')
        print('Edit %s directly.'%(todayReportPath))
        exit()

    copyfile(newReportPath, todayReportPath)

def createTomorrowsReport(newReport, template):
    # copy todo
    rep = Report()
    for key in template.sections:
        if key.lower()=='todo':
            todoKey = [key for key in newReport.sections if key.lower()=='todo'][0]
            content = newReport.sections[todoKey]
        else:
            content = ''
        rep.sections[key] = content
    
    with open(newReportPath, 'w') as f:
        f.write(rep.exportAsString())
        
def update():
    checkDir()

    newReport = Report(newReportPath)
    template = Report(templatePath)

    if hasDiff(newReport, template):
        copyReport()
        createTomorrowsReport(newReport, template)
        print('daily report is updated!')
    else:
        print('%s has not writen today yet.'%newReportPath)

if __name__=='__main__':
    update()
