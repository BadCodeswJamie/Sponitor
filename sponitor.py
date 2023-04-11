## import that shit babyyy
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,QStackedWidget,QScrollArea, QProgressBar, QHBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QThread, pyqtSignal,Qt
# from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from os.path import exists,join
from os import mkdir, remove
import spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials, CacheFileHandler
from shutil import rmtree
# import matplotlib.pyplot as plt, matplotlib.dates as mdates
import csv


## gui
class graphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.stats = QLabel(data.totalSongs())
        self.layout.addWidget(self.stats)

        self.graph= pg.PlotWidget()
        
        axis = pg.DateAxisItem()
        self.graph.setAxisItems({'bottom':axis})
        self.loadGraph()
        self.layout.addWidget(self.graph)

      
    
        self.move(0,0)
        self.setLayout(self.layout)

    def loadGraph(self):
        self.setWindowTitle(username)
        self.graph.clear()
        # graph.plot((lambda date : [datetime.datetime.strptime(i,'%Y-%m-%d').timestamp() for i in date])(date), numSongs)
        date_num= {}
        lastDate= ''
        for i in songData:
            date= songData[i][0]
            if date != lastDate:
                lastDate= date
                dateTime= datetime.strptime(date,'%Y-%m-%d').timestamp()
                date_num[dateTime]=0
            date_num[dateTime]+=1
        y= sorted(date_num)
        x= [date_num[i] for i in y]
        length= len(date_num)
        cumulative_x= [len(songData)]
        for i in range(length-1, 0,-1): # working backwards from totals songs subrtacting songs added per day
            elem= cumulative_x[0]- x[i]
            cumulative_x.insert(0,elem)

        perDay= ''
        if len(y) > 1:
            perDay= '  Songs per day: %s' % round((cumulative_x[-1]- cumulative_x[0])/(datetime.fromtimestamp(y[-1])- datetime.fromtimestamp(y[0])).days, 2)
        self.stats.setText(data.totalSongs()+ perDay)
        self.graph.plot(y,cumulative_x)
        print('Graph Loaded')


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        QApplication.font()
        self.graph= graphWindow() # new instance of graph window so to call the functions(of this specific graph) use self.graph.classfunc() <-- ignoring self
        self.resize(150,150)
        self.loadedUser= my_id

        # create pages(stacks)
        self.home = QWidget()
        self.changeUser = QWidget()
        self.main= QWidget()
        self.missingPage = QWidget()
        self.duplicatePage = QWidget()
        self.followArtists = QWidget()
        self.searchPage= QWidget()
        self.log= QWidget()
        self.addUser= QWidget()

        # create stack and add all pages
        self.Stack = QStackedWidget (self)
        self.Stack.addWidget (self.home)
        self.Stack.addWidget (self.changeUser)
        self.Stack.addWidget (self.main)
        self.Stack.addWidget (self.missingPage)
        self.Stack.addWidget (self.duplicatePage)
        self.Stack.addWidget (self.followArtists)
        self.Stack.addWidget (self.searchPage)
        self.Stack.addWidget (self.log)
        self.Stack.addWidget (self.addUser)
        
        
        # developing the pages
        self.create_home()
        self.create_changeUser()
        self.create_main()
        self.create_missingPage()
        self.create_duplicatePage()
        self.create_followArtists()
        self.create_searchPage()
        self.create_logPage()
        self.create_addUserPage()

        #placing stack in window (class)
        layout= QVBoxLayout()
        layout.addWidget(self.Stack)
        self.setLayout(layout)
        self.setWindowTitle("Home")

        self.show()


    # Home page
    def create_home(self):
        layout= QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        hLayout1= QHBoxLayout()
        hLayout2= QHBoxLayout()
        hLayout3= QHBoxLayout()

        self.currentUserLabel= QLabel("Current User: %s"  % username)
        self.currentUserLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.currentUserLabel)

        button1= QPushButton("Change User")
        button1.clicked.connect(self.showChangeUser)
        layout.addWidget(button1)

        button2= QPushButton("Run")
        button2.clicked.connect(self.run)
        hLayout1.addWidget(button2)

        button3= QPushButton("Graph")
        button3.clicked.connect(self.showGraph)
        hLayout1.addWidget(button3)

        layout.addLayout(hLayout1)

        button4= QPushButton("Missing")
        button4.clicked.connect(self.showMissingPage)
        hLayout2.addWidget(button4)

        button5= QPushButton("Duplicate")
        button5.clicked.connect(self.showDuplicatePage)
        hLayout2.addWidget(button5)

        layout.addLayout(hLayout2)

        button6=  QPushButton("Follow artists")
        button6.clicked.connect(self.showFollowArtists)
        hLayout3.addWidget(button6)

        button7=  QPushButton("Search")
        button7.clicked.connect(self.showSearchPage)
        hLayout3.addWidget(button7)

        layout.addLayout(hLayout3)

        button8= QPushButton('Log')
        button8.clicked.connect(self.showLogPage)
        layout.addWidget(button8)

        self.home.setLayout(layout)

    
    #Change user page
    def create_changeUser(self):
        layout= QVBoxLayout()
        scroll, scrollContent, self.userScrollLayout= self.scrollBox()
        scroll.setWidget(scrollContent)
        layout.addWidget(scroll)

        hLayout= QHBoxLayout()
        checkUser= QPushButton('Add')
        checkUser.clicked.connect(lambda event : self.showAddUser())
        hLayout.addWidget(checkUser)
        
        hLayout.addWidget(self.homeButton())
        layout.addLayout(hLayout)
        self.changeUser.setLayout(layout)

    def updateChangeUser(self):
        data.get_id_user()
        self.deleteLayoutItems(self.userScrollLayout)
        for i in id_user:
            button= QPushButton(id_user[i])
            button.clicked.connect(lambda event, x=i: data.changeActiveUser(x)) # clicked.connect passes a bool to the lambda func so event takes that who knwos why x=i to save the variable as i doesnt stay??????
            button.clicked.connect(lambda event : self.showHome()) # go(0)
            button.clicked.connect(lambda event : self.graph.loadGraph())
            self.userScrollLayout.addWidget(button)
        print('Updated Change User')


    # missing page
    def create_missingPage(self): # this wont update after run
        layout= QVBoxLayout()
        hLayout= QHBoxLayout()

        self.missingChange= QPushButton()
        self.missingChange.clicked.connect(self.showAllMissing)
        self.missingScroll, self.missingScrollContent, self.missingScrollLayout= self.scrollBox()
        layout.addWidget(self.missingScroll)
        self.missingScroll.setWidget(self.missingScrollContent)

        hLayout.addWidget(self.missingChange)   
        hLayout.addWidget(self.homeButton())
        
        layout.addLayout(hLayout)
        self.missingPage.setLayout(layout)
    
    def showAllMissing(self):
        self.setWindowTitle("Missing - All")
        self.changeScrollContent(data.missing(), func= 0, scrollLayout= self.missingScrollLayout, connectionFunction=self.missingUserConf)
        self.missingChange.setText('Show Deleted')
        self.changeConnection(self.missingChange.clicked, self.showDeleted)

    def showDeleted(self):
        self.setWindowTitle("Missing - Deleted")
        self.changeScrollContent(data.deleted(data.missing()), func= 1, scrollLayout= self.missingScrollLayout, connectionFunction=self.missingUserConf)
        self.missingChange.setText('Show Missing')
        self.changeConnection(self.missingChange.clicked, self.showMissing)
    
    def showMissing(self):
        self.setWindowTitle("Missing - Missing")
        self.changeScrollContent(data.remDel(data.missing()), func= 2, scrollLayout= self.missingScrollLayout, connectionFunction=self.missingUserConf)
        self.missingChange.setText('Show Unconf')
        self.changeConnection(self.missingChange.clicked, self.showUnConfMissing)

    def showUnConfMissing(self):
        self.setWindowTitle("Missing - Unconfirmed")
        self.changeScrollContent(data.remConf(data.missing()), func= 3, scrollLayout= self.missingScrollLayout, connectionFunction=self.missingUserConf)
        self.missingChange.setText('Show All')
        self.changeConnection(self.missingChange.clicked, self.showAllMissing)
        

    # duplicate page
    def create_duplicatePage(self):
        layout= QVBoxLayout()
        hLayout= QHBoxLayout()

        self.duplicateChange= QPushButton()
        self.duplicateChange.clicked.connect(self.showAllDuplicate)

        self.duplicateScroll, self.duplicateScrollContent, self.duplicateScrollLayout= self.scrollBox()
        
        layout.addWidget(self.duplicateScroll)
        self.duplicateScroll.setWidget(self.duplicateScrollContent)

        hLayout.addWidget(self.duplicateChange)   
        hLayout.addWidget(self.homeButton())
        
        layout.addLayout(hLayout)
        self.duplicatePage.setLayout(layout)

    def showAllDuplicate(self):
        self.setWindowTitle("Duplicates - All")
        self.changeScrollContent(data.duplicates(), func= 0, scrollLayout= self.duplicateScrollLayout, connectionFunction= self.duplicateUserConf)
        self.duplicateChange.setText('Show Allowed')
        self.changeConnection(self.duplicateChange.clicked, self.showAllowedDuplicate)
    
    def showIllegalDuplicate(self):
        self.setWindowTitle("Duplicates - Illegal")
        self.changeScrollContent(data.remAllowedDuplicates(data.duplicates()), func= 1, scrollLayout= self.duplicateScrollLayout, connectionFunction= self.duplicateUserConf)
        self.duplicateChange.setText('Show All')
        self.changeConnection(self.duplicateChange.clicked, self.showAllDuplicate)
    
    def showAllowedDuplicate(self):
        self.setWindowTitle("Duplicates - Allowed")
        self.changeScrollContent(list(allowedDup.keys()), func= 2, scrollLayout= self.duplicateScrollLayout, connectionFunction= self.duplicateUserConf)
        self.duplicateChange.setText('Show illegal')
        self.changeConnection(self.duplicateChange.clicked, self.showIllegalDuplicate)



    # main(run) page
    def create_main(self):
        layout= QVBoxLayout()
        self.mainLabel= QLabel("change with window.mainLabel.setText(str)")
        layout.addWidget(self.mainLabel)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.main.setLayout(layout)
    

    # follow artists page
    def create_followArtists(self):
        layout= QVBoxLayout()
        
        scroll, scrollContent, self.followScrollLayout= self.scrollBox()
        scroll.setWidget(scrollContent)
        layout.addWidget(scroll)

        self.followLabel= QLabel()
        layout.addWidget(self.followLabel)
        self.followProgress= QProgressBar()
        self.followProgress.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.followProgress)

        layout.addWidget(self.homeButton())
        self.followArtists.setLayout(layout)

    def updateFollowArtists(self):
        self.deleteLayoutItems(self.followScrollLayout)
        for playlistId in ids_playlists:
            button= QPushButton(ids_playlists[playlistId])
            button.clicked.connect(lambda event , playlistId= playlistId: self.create_followWorker(playlistId))
            self.followScrollLayout.addWidget(button)
        print('Updated follow playlists')

    def create_followWorker(self, playlistId): # creates worker to follow artists which updates follow artists page
        self.followWorker = Worker(caller= 'follow', playlistId= playlistId)
        self.followThread = QThread()
        self.followWorker.moveToThread(self.followThread)


        self.followThread.started.connect(self.followWorker.run)
        self.followWorker.finished.connect(self.followThread.quit)
        self.followWorker.progress.connect(self.update_followProgress)
        self.followWorker.mainLab.connect(self.update_followLabel)
        self.followWorker.finished.connect(self.followWorker.deleteLater)
        self.followThread.finished.connect(self.followThread.deleteLater)

        self.followThread.start()

    # search page
    def create_searchPage(self):
        layout= QVBoxLayout()
        
        self.searchThread= QThread()

        scroll, scrollContent, self.searchScrollLayout= self.scrollBox()
        self.searchBar= QLineEdit()
        self.searchBar.textChanged.connect(lambda event : self.search())
        layout.addWidget(self.searchBar)
        # search bar enter connect or button
        layout.addWidget(scroll)
        scroll.setWidget(scrollContent)
        layout.addWidget(self.homeButton())
        self.searchPage.setLayout(layout)

    def search(self):
        # stop previous search if ongoing(close thread opended in show search)
        self.searchThread.quit()
        toSearch= self.searchBar.text()
        self.searchWorker= Worker(caller= 'search')
        self.searchWorker.moveToThread(self.searchThread)

        self.searchThread.started.connect(self.searchWorker.run)
        self.searchWorker.finished.connect(self.searchThread.quit)
        self.searchWorker.finished.connect(self.searchWorker.deleteLater)
        self.searchWorker.searchResults.connect(self.addResults)

        if toSearch != '':
            self.searchThread.start()
        else:
            self.setWindowTitle('Search')
            self.deleteLayoutItems(self.searchScrollLayout)
        
    def clearSearch(self):
        print('Cleared search')
        self.searchBar.setText('')
        # self.deleteLayoutItems(self.searchScrollLayout)

    def addResults(self,trackIds):
        resultLayout= QVBoxLayout()
        resultLayout.setAlignment(Qt.AlignTop)
        self.setWindowTitle('Search - %s' % len(trackIds))
        for trackId in trackIds[:100]: # lagg if too many
            hLayout= QHBoxLayout()
            self.addSong(trackId,hLayout)
            resultLayout.addLayout(hLayout)
        self.deleteLayoutItems(self.searchScrollLayout) # using another layout and moving delete layout here removes flicker
        self.searchScrollLayout.addLayout(resultLayout)


    # log page
    def create_logPage(self):
        layout= QVBoxLayout()
        scroll, scrollContent, self.logScrollLayout= self.scrollBox()
        layout.addWidget(scroll)
        scroll.setWidget(scrollContent)

        hLayout= QHBoxLayout()
        clear= QPushButton('Clear')
        clear.clicked.connect(lambda event : self.clearLog())
        hLayout.addWidget(clear)
        hLayout.addWidget(self.homeButton())
        layout.addLayout(hLayout)

        self.log.setLayout(layout)

    def updateLog(self): #refreshes scroll area with string from log file
        label= QLabel(data.get_log())
        self.deleteLayoutItems(self.logScrollLayout)
        self.logScrollLayout.addWidget(label)

    def clearLog(self): # clears log then refreshes log scroll area
        data.clear_log()
        self.updateLog()


    # create user page
    def create_addUserPage(self):
        layout= QVBoxLayout()
        self.createThread= QThread()
        self.addUserLayout= QVBoxLayout()

        layout.addLayout(self.addUserLayout)

        hLayout= QHBoxLayout()
        self.createButton= QPushButton('Next')
        self.createButton.clicked.connect(lambda event, string= 'Id has not been input' : self.updateWarning())
        hLayout.addWidget(self.createButton)
        self.addUserBack= QPushButton('Back')
        self.addUserBack.clicked.connect(lambda event : self.showChangeUser())
        hLayout.addWidget(self.addUserBack)
        layout.addLayout(hLayout)

        self.addUser.setLayout(layout)

    def create_addUserLayout(self):
        label= QLabel()
        label.setText('Spotify Account Url:')
        self.addUserLayout.addWidget(label)

        self.Url= QLineEdit()
        self.Url.textChanged.connect(lambda event : self.checkUser())
        self.addUserLayout.addWidget(self.Url)

        label1= QLabel()
        label1.setText('Username:')
        self.addUserLayout.addWidget(label1)

        self.Username= QLabel()
        self.addUserLayout.addWidget(self.Username)

        self.warning= QLabel()
        self.warning.setStyleSheet('color: red')
        self.addUserLayout.addWidget(self.warning)

    def checkUser(self): # creates worker to check if if is viable need to change this so if no last user it works lol
        self.Url.text()
        # seems like workers arent being deleted
        self.create= Worker(caller= 'check')
        self.create.moveToThread(self.createThread)
        self.createThread.started.connect(self.create.run)
        self.create.finished.connect(self.createThread.quit)
        self.create.finished.connect(self.create.deleteLater)
        self.create.warning.connect(self.updateWarning)
        self.create.searchResults.connect(self.updateUsername) # username has been found

        # self.create.progress.connect(self.changeCreateConnection) # when progress is changed(auth conf) mainlab then changes username

        self.createThread.start()


    def updateWarning(self,string): # changes the warning label on the change user page if warning emitted means bad username
        self.warning.setText(string)
        self.Username.setText('Your Username will appear here')
        self.changeConnection(self.createButton.clicked, lambda event : self.checkUser())


    def updateUsername(self,newUserInfo): # updates username variable; when this func is called it means username is found so it changes state of button to allow progress
        self.newUsername= newUserInfo[1]
        self.warning.setText('')
        self.newId= newUserInfo[0]
        self.Username.setText(self.newUsername)
        self.changeConnection(self.createButton.clicked, lambda event : self.getVerification()) # button changes to allow progressaw


    def getVerification(self): # uses self.newId as user can still change the text box
        self.setAnweredState()

        self.deleteLayoutItems(self.addUserLayout)
        label= QLabel()
        print('align these pleaseeeeee')
        label.setText('Redirect Url:')
        self.addUserLayout.addWidget(label)
        self.redirect= QLineEdit()
        self.addUserLayout.addWidget(self.redirect)

        self.getAuthor= QThread()
        self.getFirstSp= checkAuth()
        self.getFirstSp.moveToThread(self.getAuthor)
        self.getAuthor.started.connect(self.getFirstSp.run)
        self.getFirstSp.finished.connect(self.getAuthor.quit)
        self.getFirstSp.finished.connect(self.getAuthor.deleteLater)
        self.getFirstSp.finished.connect(self.getFirstSp.deleteLater)
        self.getFirstSp.sp.connect(lambda sp : self.confAuth(sp)) # sp is given if None it has failed so need to retry
        
        self.getAuthor.start()
        
        self.changeConnection(self.createButton.clicked, lambda event, state= True : self.setAnweredState(state)) # button changes to allow progress

        # if auth worked
            # self.addConfUser()

    def setAnweredState(self, state= False):
        self.answered= state

    def confAuth(self, sp): # if auth worked/ didnt
        if sp == None: self.updateAddUser() # go back
        else: # set upd saved ids playlists
            self.deleteLayoutItems(self.addUserLayout)
            scroll, scrollContent, scrollLayout= self.scrollBox()
            
            scroll.setWidget(scrollContent)
            self.addUserLayout.addWidget(scroll)

            self.playlistsToAdd= []
            for playlistInfo in spotify.find_userPlaylists(sp, self.newId): #returns [ [id,name] ,..]
                background= QWidget()
                hLayout= QHBoxLayout()
                print('if buttons align wrong change here')
                hLayout.setAlignment(Qt.AlignLeft)
                button1= QPushButton('Y')
                button1.clicked.connect(lambda event, state= True, playlistInfo= playlistInfo, background= background : self.setPlaylistState(state, playlistInfo, background))
                hLayout.addWidget(button1)
                button2= QPushButton('N')
                button2.clicked.connect(lambda event, state= False, playlistInfo= playlistInfo, background= background : self.setPlaylistState(state, playlistInfo, background))
                hLayout.addWidget(button2)
                
                label= QLabel()
                label.setText(playlistInfo[1])
                hLayout.addWidget(label)
                
                background.setLayout(hLayout)
                scrollLayout.addWidget(background)

            self.changeConnection(self.createButton.clicked, self.addConfUser) # creates user saved playlist ids then goes home if only user sets user to made one

    def setPlaylistState(self, state, playlistInfo, background):
        if state:
            if playlistInfo not in self.playlistsToAdd:
                self.playlistsToAdd.append(playlistInfo)
            background.setStyleSheet('color: green')
        else:
            if playlistInfo in self.playlistsToAdd:
                self.playlistsToAdd.remove(playlistInfo)
            background.setStyleSheet('color: red')


    def addConfUser(self): # if create on add user pasge is pressed a user with gathered id and user name is created
        self.create= Worker(caller= 'create')
        self.create.moveToThread(self.createThread)

        self.createThread.started.connect(self.create.run)
        self.create.finished.connect(self.createThread.quit)
        self.create.finished.connect(self.create.deleteLater)
        self.create.finished.connect(self.createThread.deleteLater)
        self.create.finished.connect(self.showHome)

        self.createThread.start()
    
    def updateAddUser(self): # resets add user page to before user id has been checked or just sets it up
        self.deleteLayoutItems(self.addUserLayout)
        self.create_addUserLayout()
        # self.Url.setText('')
    # useful code
    def homeButton(self): # creates home button widget
        button1= QPushButton("Home")
        button1.clicked.connect(self.showHome)
        return button1

    def changeConnection(self, signal, newConnection): # changes connection of signal event eg button.clicked
        signal.disconnect()
        signal.connect(newConnection)

    def scrollBox(self): # creates scroll widget
        scroll= QScrollArea()
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scrollLayout.setAlignment(Qt.AlignTop)
        return scroll, scrollContent, scrollLayout

    def addSong(self, trackId, layout): # adds hlayout (song name , artist, playlists) to layout
        song= songData[trackId]
   
        songName= QLabel(song[1])      
        songName.setFixedWidth(70)
        layout.addWidget(songName)
        
        songArtists= QLabel(', '.join(song[2]))
        songArtists.setFixedWidth(70)
        layout.addWidget(songArtists)
        
        songPlaylists= QLabel(', '.join([ids_playlists[playlist[0]] for playlist in song[3]]))
        layout.addWidget(songPlaylists)

    def changeScrollContent(self, trackIds, func, scrollLayout, connectionFunction): # refreshes provided scrollLayout and adds all songs in provided list must give function(object) with 2 states(bool) for yes/no buttons
        self.deleteLayoutItems(scrollLayout)
        for trackId in trackIds:
            hScrollLayout= QHBoxLayout()

            hButtonsLayout= QHBoxLayout()
            hButtonsLayout.setSpacing(0)
            hButtonsLayout.setContentsMargins(0,0,0,0) # trying to get the buttons closer together
            
            button1= QPushButton('Y')
            button2= QPushButton('N')
            
            button1.clicked.connect(lambda event, Id= trackId, state= True, func= func, layout= hScrollLayout : connectionFunction(Id,state,func,layout))
            button2.clicked.connect(lambda event, Id= trackId, state= False, func= func, layout= hScrollLayout : connectionFunction(Id,state,func,layout))

            button1.setFixedWidth(30)
            button1.setContentsMargins(0,0,0,0)
            hButtonsLayout.addWidget(button1)

            button2.setFixedWidth(30)
            button2.setContentsMargins(0,0,0,0)
            hButtonsLayout.addWidget(button2)

            hScrollLayout.addLayout(hButtonsLayout)

            self.addSong(trackId,hScrollLayout)
            scrollLayout.addLayout(hScrollLayout)
            


    def deleteLayoutItems(self, layout): # deletes items in layout but it might only forget them lol
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteLayoutItems(item.layout())

    def missingUserConf(self, trackId, state, func, layout): # on button press it hides song from missing scroll(if needed) and changes deleted state
        hide= False
        if  func != 0:
            if func == 1 and not state: hide= True
            elif func == 2 and state: hide= True
            elif func == 3: hide= True
        
        if hide:
            self.deleteLayoutItems(layout) ## remove from view if not showing all what about showing 
            layout.deleteLater()

        data.setDeletedState(trackId,state)

    def duplicateUserConf(self,trackId,state,func,layout): #  on button press it hides song from duplicate scroll(if needed) and adds/removes from allowed duplicates
        hide= False
        if func != 0:
            if func == 1 and state: hide= True
            elif func == 2 and not state: hide= True

        if hide: ## this could be turned into a func
            self.deleteLayoutItems(layout) ## remove from view if not showing all what about showing 
            layout.deleteLater()

        if state: ## add to allowed duplicates
            data.add_allowedDup(trackId, [playlistData[0] for playlistData in songData[trackId][3]])
        else: ## remove from allowed duplicates
            data.rem_fromAllowedDup(trackId)


    ## button commands

    def showGraph(self):
        if self.graph.isVisible(): self.graph.hide()
        else: self.graph.show()

    def waitHome(self):
        from time import sleep
        sleep(1)
        self.showHome()

    def showHome(self): # the go funcs could be changed into func with passed variable for index and list of names with same index
        self.currentUserLabel.setText("Current User: %s"  % username)
        self.setWindowTitle("Home")
        self.Stack.setCurrentIndex(0)
        self.resize(150, 150)

    def showChangeUser(self):
        self.updateChangeUser()
        self.setWindowTitle("Change User")
        self.Stack.setCurrentIndex(1)

    def update_mainLabel(self,elem): # changes label on main page
        self.mainLabel.setText(elem)

    def run(self):
        self.setWindowTitle("Sponitor")
        self.Stack.setCurrentIndex(2)

        self.update_mainLabel('Starting')
        self.update_progress(0)
        self.thread = QThread()
        self.worker = Worker(caller= 'main')
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.mainLab.connect(self.update_mainLabel)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.waitHome)
        self.thread.finished.connect(lambda event=None : self.graph.loadGraph())
        self.thread.finished.connect(lambda event=None : self.updateMD())

        self.thread.start()

    def showMissingPage(self):
        self.updateMD()
        self.showUnConfMissing()
        self.Stack.setCurrentIndex(3)
        self.resize(430,300)
    
    def showDuplicatePage(self):
        self.updateMD()
        self.showIllegalDuplicate()
        self.Stack.setCurrentIndex(4)
        self.resize(430,300)

    def showFollowArtists(self):
        self.updateFollowArtists()
        self.setWindowTitle("Follow Artists")
        self.Stack.setCurrentIndex(5)

    def showSearchPage(self):
        self.clearSearch()
        self.setWindowTitle("Search")
        self.Stack.setCurrentIndex(6)

    def showLogPage(self):
        self.updateLog()
        self.setWindowTitle("Log")
        self.Stack.setCurrentIndex(7)

    def showAddUser(self):
        self.updateAddUser()
        self.setWindowTitle("Create User")
        self.Stack.setCurrentIndex(8)

    def update_progress(self, progress): # updates progress bar on main page
        self.progress.setValue(progress)

    def updateMD(self): # refreshes missing and duplicate scrollareas
        self.showUnConfMissing()
        self.showIllegalDuplicate()
        print('Updated Missing, Duplicates')

    def update_followLabel(self, text): ## could shorten this and update prgo with a lambda func that ypu give the self var to
        self.followLabel.setText(text) # changes label on follow artists page

    def update_followProgress(self, pos): # changes progress bar on folllow artists page
        self.followProgress.setValue(pos)

class checkAuth(QObject):
    finished = pyqtSignal()
    sp = pyqtSignal(object)

    def __init__(self):
        super(checkAuth, self).__init__()

    def run(self):
        print('check Auth')
        sp= spotify.getSp(window.newId,window)
        if sp == False:
            self.sp.emit(None) 
        else:
            self.sp.emit(sp) 

        self.finished.emit()

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    mainLab= pyqtSignal(str)
    warning= pyqtSignal(str)
    searchResults= pyqtSignal(list)

    def __init__(self, caller= '', playlistId= ''):
        super(Worker, self).__init__()
        self.caller= caller
        self.playlistId= playlistId

    def run(self):
        # Here we pass the update_progress (uncalled!)
        # function to the long_running_function:
        if self.caller == 'main':
            spotify.updateSongs(self.update_label, self.update_progress)
        elif self.caller == 'follow':
            spotify.followArtistsInPlaylists(self.update_label, self.update_progress, self.playlistId)
        elif self.caller == 'search': 
            self.searchResults.emit(spotify.search(window.searchBar.text()))
        elif self.caller == 'check':
           data.check_new_user(window.Url.text(), self.update_warning, self.update_label,self.update_results)
        elif self.caller == 'create':
            data.create_new_user(window.newId, window.newUsername, window.playlistsToAdd)
        self.finished.emit()

    def update_results(self,results):
        self.searchResults.emit(results)

    def update_warning(self, string):
        self.warning.emit(string)

    def update_progress(self, percent):
        self.progress.emit(percent)

    def update_label(self, string):
        self.mainLab.emit(string)

## spotify monitor
class data():
    # def create_saved_ids_playlists(saved_ids_playlists):# creates/ updates saved ids_playlists(playlists that get saved)
    #     with open(join(my_id, 'saved_ids_playlists.txt'),'w+',encoding='utf-8') as file:  # replace with if loc not exists create_file
    #         first= True
    #         for i in list(saved_ids_playlists.keys()):
    #             to_write= i+'##'+ saved_ids_playlists[i]
    #             if not first:
    #                 to_write= '\n'+to_write
    #             file.write(to_write)
    #             first=False

    def checkFile(loc):
        if not exists(loc):
            data.createFile(loc)

    def create_saved_ids_playlists(Id,playlistInfo):
        toAdd= []
        for playlist in playlistInfo:
            toAdd.append("##".join(playlist))
        toAdd= '\n'.join(toAdd)
        loc= join(Id, 'saved_ids_playlists.txt')
        with open(loc, 'w+', encoding= 'UTF-8') as file:
            file.write(toAdd)
                
    def get_saved_ids_playlists(): # returns dict of id:playlists that need to be saved
        global ids_playlists
        ids_playlists={}
        loc= join(my_id, 'saved_ids_playlists.txt')
        if not exists(loc):
            data.add_log(loc+' does not exist for '+ username)

        with open(loc,'r',encoding='utf-8') as file:
            for i  in file.readlines():
                i= i.replace('\n','')
                i= i.split('##')
                ids_playlists[i[0]]= i[1] 
        if len(ids_playlists) == 0:
            print('create_ids_playlists(code meee)')

    def createFile(file_loc, string= ''):
        with open(file_loc,'w+',encoding='utf-8') as last:
            if string != '':
                last.write(string)
            print("Created %s." % file_loc)

    def get_id_user():# returns dict{id:user}(str)
        global id_user
        id_user={}
        idUser_loc= 'id_user.txt'
        data.checkFile(idUser_loc)

        with open(idUser_loc,'r',encoding='utf-8') as ids:
            for line in ids.readlines():
                temp= line.split('##')
                id_user[temp[0]]= temp[1].replace('\n','')


    def get_log():
        loc= join(my_id, username+ '_log.txt')
        data.checkFile(loc)

        with open(loc, 'r', encoding= 'UTF-8') as file:
            log= file.read()
        
        if log == '':
            log= 'No log entries'
        return log

    def add_log(string):
        loc= join(my_id, username+ '_log.txt')
        data.checkFile(loc)

        with open(loc, 'a', encoding= 'UTF-8') as file:
            file.write('\n'+ string)

    def clear_log():
        loc= join(my_id, username+ '_log.txt')
        with open(loc, 'w+', encoding= 'UTF-8') as file:
            print('Cleared log')
        

    def check_new_user(Id, update_warning, update_label, update_results): # adds id and username to file returns user id
        if 'user/' in Id: Id= Id.split('user/')[1][:25]
        tempUsername= spotify.verifyUsername(Id)
        if tempUsername == False:
            spotify.update_ui(text= 'Cannot fetch username', update_label= update_warning)
            return
        else:
            spotify.update_ui(text= tempUsername, update_label= update_label)
        update_results([Id,tempUsername])


    def create_new_user(Id,temp_username, playlistInfo):
        data.get_id_user()
        length= len(id_user)
        
        mkdir(Id)
        with open('id_user.txt','a+',encoding='utf-8') as ids:
            to_write= Id+ '##'+ temp_username
            if length > 0: to_write= '\n'+ to_write
            ids.write(to_write)
        data.get_id_user()
        data.create_saved_ids_playlists(Id,playlistInfo)
        data.add_log('Created user %s - %s' % (temp_username, Id))

## update with gui
    def remove_user(): # removes user from id_user and deletes their files
        print('Remove user')
        user_id= data.select_user()
        if user_id == my_id:
            print('this would result in no current user')
        #id last user user to be removed then change it (select new user)
        # what if removing all users? return to home (only oprion is create new usedr
        # homepage()
        username_to_delete= data.user(user_id)
        password= input('Input password to confirm deletion of %s\n' % username_to_delete)
        if password == 'delete':
            if exists(username_to_delete):
                rmtree(username_to_delete) # cant remove folders with nhabitants
            else:
                print("Folder already deleted?")
            with open('id_user.txt','r',encoding='utf-8') as file:
                temp= file.read()
            temp= temp.replace(my_id+'##'+username_to_delete+'\n','') # either or
            temp= temp.replace('\n'+my_id+'##'+username_to_delete,'')
            remove('id_user.txt')
            with open('id_user.txt','w+',encoding='utf-8') as file:
                file.write(temp)
            # remove from id_user
        else:print('Incorrect password')

## update with gui
    def select_user(): # returns selected id but does not change last user
        data.get_id_user()
        for i,item in enumerate(list(id_user.keys())):
            print(str(i+1)+') '+ id_user[item] )
        while True:
            temp= input('Select user(num): ')
            try: 
                temp= int(temp)
                break
            except:print('Invalid input')
        selected_id= list(id_user.keys())[temp-1]
        print('User selected:', id_user[selected_id])
        return selected_id

    def update_last_user_id(my_id): # updates user id in file
        with open('last_id.txt','w+',encoding='utf-8') as last:
            last.write(my_id)
    
    def get_last_user_id():# returns last user to load in with
        last_idLoc= 'last_id.txt'
        data.checkFile(last_idLoc)

        with open(last_idLoc,'r',encoding='utf-8') as last:
            return last.read()

    def changeActiveUser(Id): 
        print(Id)
        global ids_playlists,my_id,username
        my_id= Id
        data.update_last_user_id(my_id)
        username= id_user[my_id]
        data.get_saved_ids_playlists()
        data.load_songData()

        print('Active user changed to', username)

    def save_songData():
        columns= ['Track Id','Date First Added','Name','Artists','Current Playlists/Date Addded','Missing','Deleted']
        with open(join(my_id,username+'_songData.csv'), 'w', newline='', encoding= 'UTF-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for trackId in songData:
                song= songData[trackId]
                artists=seperator.join(song[2])
                playlists_dates=[]
                for playlist_date in song[3]:
                    playlists_dates.append(seperator.join(playlist_date))
                playlists_dates= seperator2.join(playlists_dates)
                row= dict(zip(columns, [trackId,song[0],song[1], artists, playlists_dates,song[4],song[5]]))
                writer.writerow(row)
        print('Saved songData')
            

    def load_songData():
        global songData
        songData= {}
        loc= join(my_id,username+'_songData.csv')
        data.checkFile(loc)

        with open(loc, 'r', newline='', encoding= 'UTF-8') as csvfile:
            morp= csv.reader(csvfile)
            for pos,row in enumerate(morp):
                if pos != 0:
                    artists= row[3].split(seperator)
                    playlists_dates= []
                    for elem in row[4].split(seperator2):
                        playlists_dates.append(elem.split(seperator))

                    songData[row[0]]= [row[1], row[2], artists, playlists_dates, row[-2], row[-1]]
        print('Loaded songData')

    #new
    def r_nestedElem(pos,nestedList): # returns indexed val of nested list
        temp=[]
        for eggList in nestedList:
            temp.append(eggList[pos])
        return temp


    def get_allowedDup():
        global allowedDup
        path= join(my_id,username+'_allowedDuplicates.txt')
        data.checkFile(path)
        with open(path, 'r', encoding= 'UTF-8') as file:
            temp= file.readlines()

        allowedDup= {}
        if temp != ['']:
            for i in temp:
                i= i.replace('\n','')
                i= i.split(seperator)
                allowedDup[i[0]]= i[1:]
        print('Loaded allowed duplicates')

    def save_allowedDup():
        path= join(my_id,username+'_allowedDuplicates.txt')
        temp= '\n'.join([i+ seperator+ seperator.join(allowedDup[i]) for i in allowedDup])
        with open(path, 'w+', encoding= 'UTF-8') as file:
            file.write(temp) 


    def add_allowedDup(trackId, playlists):
        if type(playlists) != list: playlists= [playlists]
        if trackId in allowedDup:
            allowedDup[trackId].extend(playlists) ## adds new playlists to end of allowed playlist list
        else:
            allowedDup[trackId]= playlists

        data.save_allowedDup()
        # return allowedDup

    def rem_fromAllowedDup(trackId): ## removes track from allowed duplicates file
        allowedDup.pop(trackId)
        data.save_allowedDup()
        # return allowedDup
    
    def remAllowedDuplicates(trackIds= {}): #removes duplicates that are not allowed returns list of ids
        for trackId in allowedDup:
            if trackId in trackIds: # if it is an allowed duplicate
                allowedPlaylistIds= allowedDup[trackId]
                rem= True
                for playlistId in trackIds[trackId]:
                    if playlistId not in allowedPlaylistIds: 
                        rem= False
                if rem: # if allowed to be duplicate remove
                    del trackIds[trackId]
                else:# it has been added to another playlist so user has to re authenticate it as allowed
                    data.rem_fromAllowedDup(trackId)
                
        return list(trackIds.keys())

    def duplicates():# returns all duplicates except songs that have been user deleted
        duplicates= {}

        for trackId in songData:
            song= songData[trackId]
            if len(song[3]) > 1 and not song[5] == 'true': ## if duplicate(in multiple playlists) and not deleted
                duplicates[trackId]= [playlistData[0] for playlistData in song[3]]
        return duplicates

        # also ignore missing and deleted duplicates?
        for trackId in songData:
            song= songData[trackId]
            if len(song[3]) > 1 and not song[4] == 'true' or song[5] == 'true':# if song duplicated and not missing or deleted then count it
                if trackId in allowedDup:
                    allowed+= len(allowedDup[trackId])-1 #allowed to be duplicated - 'original'
                    for i in song[3]:
                        if i[0] not in allowedDup[trackId]:
                            if input('Allowed duplicate %s is also in %s allow?:' % (song[1], ids_playlists[i[0]])) == 'y':
                                allowedDup= data.add_allowedDup(trackId,i[0], allowedDup)
                                allowed+=1
                        
                else:
                    print(song[1],','.join(song[2]),','.join([ids_playlists[playlist[0]] for playlist in song[3]]))
                    if input('add to allowed duplicate list? ') == 'y':
                        playlists= [playlist[0] for playlist in song[3]]
                        allowedDup= data.add_allowedDup(trackId,playlists, allowedDup)
                        allowed+= len(song[3])
                    
                total+=len(song[3])-1
        return total,allowed
    # 'track_id':['date first added', 'name', ['artist'], (current playlist/s)[['current playlist','date added'], ...], 'missing', 'deleted]

    #new
    #add gui

    def setDeletedState(trackId, state):

        if state:
            changeState= 'true' # delete tag updated
        else:
            changeState= 'false' # delete tag updated
        song= songData[trackId]
        if changeState != song[5]: #only updates songData if state changed
            song[5]= changeState
            data.add_log('%s delteted state set to %s' % (song[1], changeState))
            songData[trackId]= song
            data.save_songData()



    def missing():# returns list of missing trackIds
        missingList= []
        for trackId in songData:
            if songData[trackId][4] == 'true': # if missing
                missingList.append(trackId)
        return missingList

    def remConf(trackIds):
        toRem=[]
        for trackId in trackIds:
            if songData[trackId][5] in ['true','false']: # if it has been user confirmed remove it
                toRem.append(trackId)
        for trackId in toRem:
            trackIds.remove(trackId)
        return trackIds
    
    def remDel(trackIds):
        toRem=[]
        for trackId in trackIds:
            if songData[trackId][5] =='true': # if it has been user confirmed remove it
                toRem.append(trackId)
        for trackId in toRem:
            trackIds.remove(trackId)
        return trackIds

    def deleted(missingList): # returns deleted(user confirmed) songs from list of misssing trackId
        deletedList= []
        for trackId in missingList:
            if songData[trackId][5] == 'true':
                deletedList.append(trackId)
        return deletedList

    def totalSongs():
        missingList= data.missing()
        deletedList= data.deleted(missingList)
        delSongs= len(deletedList)
        missSongs= len(missingList)- delSongs
        duplicates= data.duplicates() #dictionary
        dupSongs= len(duplicates)
        total= len(songData)-delSongs
        return 'Total songs: %s  Duplicate songs: %s  Missing songs: %s' % (total,dupSongs, missSongs)


class spotify():
    # new and not sure if working
    def getAuth(Id,window=None):
        print('getting Auth', window)
        as_dict= True
        cid, secret= spotify.get_keys()
        scope = ['user-library-read', 'playlist-read-private', 'playlist-read-collaborative', 'user-follow-read', 'user-follow-modify']
        
        # sp= getAuth(cid, secret, scope, Id).sp
        handler= CacheFileHandler(username= Id)
        auth= SpotifyOAuth(scope=scope,client_id=cid, client_secret=secret,redirect_uri= 'https://i.dailymail.co.uk/i/pix/2012/06/04/article-2154283-136ED7F3000005DC-412_634x412.jpg', cache_handler=handler, show_dialog=True)#, username= my_id

        def getCode(window):
            print('get code', window)
            auth._open_auth_url()
            if window == None: # if no window open
                redirect= input('Redirect Url: ')
            else:
                while window.answered  ==  False:
                    pass 
                redirect= window.redirect.text()
            state, code= auth.parse_auth_response_url(redirect)
            return code

        token_info = auth.validate_token(auth.cache_handler.get_cached_token())
        if token_info is not None:
            if auth.is_token_expired(token_info):
                token_info = auth.refresh_access_token(
                    token_info["refresh_token"]
                )
            auth._save_token_info(token_info if as_dict else token_info["access_token"])
            return auth


        payload = {
                "redirect_uri": auth.redirect_uri,
                "code": getCode(window),
                "grant_type": "authorization_code",
            }

        if auth.scope:
            payload["scope"] = auth.scope
        if auth.state:
            payload["state"] = auth.state

        headers = auth._make_authorization_headers()


        response = auth._session.post( # token info needed
                    auth.OAUTH_TOKEN_URL,
                    data=payload,
                    headers=headers,
                    verify=True,
                    proxies=auth.proxies,
                    timeout=auth.requests_timeout,
                )

        token_info = response.json()
        token_info = auth._add_custom_values_to_token_info(token_info)
        auth.cache_handler.save_token_to_cache(token_info)

        auth._save_token_info(token_info if as_dict else token_info["access_token"])
        return auth

    #new
    def getSp(Id, window= None):
        print('getting Sp')
        try:
            # auth= SpotifyOAuth(scope=scope,client_id=cid, client_secret=secret,redirect_uri= 'https://i.dailymail.co.uk/i/pix/2012/06/04/article-2154283-136ED7F3000005DC-412_634x412.jpg', username= Id, show_dialog=True)#, username= my_id
            # sp = spotipy.Spotify(client_credentials_manager=auth)
            sp = spotipy.Spotify(client_credentials_manager=spotify.getAuth(Id, window))
            test= sp.current_user_playlists(limit=1)
            print('got authentication')
        except:
            data.add_log('Authentication failed for %s' % username)
            return False
        return sp

    def verifyUsername(Id):
        cid, secret= spotify.get_keys()
        auth= SpotifyClientCredentials(client_id= cid, client_secret= secret)
        tempSp = spotipy.Spotify(client_credentials_manager= auth)
        try:
            newUsername= tempSp.user(Id)['display_name']
            return newUsername
        except:
            return False
        
    def find_userPlaylists(sp,Id): # generates all user playlists user to create ids_playlists
        playlistInfo= [[playlist['owner']['id'],playlist['uri'], playlist['name']] for playlist in sp.current_user_playlists(limit=50)['items']]
        toReturn= []
        for playlist in playlistInfo:
            if playlist[0]== Id: # if id owner is the playlist owner
                toReturn.append(playlist[1:])
        return toReturn

    def update_ui(text= None, percent= None, update_label= None, update_progress= None):
        if text != None:
            print('text:',text)
            if update_label != None:
                update_label(string= text)
        if percent != None and update_progress != None:
                update_progress(percent= percent)

    #new
    #add gui
    ## update with gui ( parse self then call gui.setMainLabel(self,string)
    def updateSongs(update_label= None, update_progress= None): # does not get active user songs only jamies because of spotipy things
        global songData
        state= 'Auto' if __name__ == 'Main' else 'Manual'
        data.add_log('\n%s: (%s) Updating songs for %s:' % (state , datetime.now().strftime("%d-%m-%Y %H:%M:%S"), username) ) 
        sp= spotify.getSp(my_id)
        playlistIds= [playlist['uri'] for playlist in sp.current_user_playlists(limit=50)['items']] # if you have more than 50 playlists fuck you
        # songData= [['spotify:track:2dje3ZBu1j1r0QfR7mtS0l', 'spotify:playlist:1JTU5zqtgA1zzqb90papUO', '2021-08-16'], ['spotify:track:5H3swhQ72PiGd5PYz4P61P', 'spotify:playlist:1JTU5zqtgA1zzqb90papUO', '2021-08-16']]
        loadedSongs=[]# [[id, [ [playlist,date added] ]],...next]
        playlistsForDown= list(ids_playlists.keys())
        num=0
        for playlist_id in playlistIds:
            if playlist_id in playlistsForDown:
                spotify.update_ui(text= 'Loading %s...' % ids_playlists[playlist_id], update_label= update_label)
                start= 0
                while True:# the limit is 100 songs so it must be iterated to get all songs
                    total=0
                    for items in sp.playlist_tracks(playlist_id, offset=start)["items"]:
                        artists=[]
                        for artist in items['track']['artists']:
                            artists.append(artist['name'])
                        loadedSongs.append([items['track']['uri'],[[playlist_id, items['added_at'][:-10]]],items['track']['name'],artists])
                        total+=1
                        
                    start+=100 # if playlist is exactly a mutiple of 100 this still works
                    if total != 100:
                        break
                num+=1
                spotify.update_ui(percent= round((num/len(playlistsForDown))*100), update_progress= update_progress)

        if loadedSongs == []:
            spotify.update_ui(text= 'No songs found', update_label= update_label)
        else:
            spotify.update_ui(text= 'Begin compilation...', update_label= update_label)
            loaded_songData={}
            total= len(loadedSongs)
            pos=0
            while loadedSongs != []:
                song= loadedSongs.pop(0)
                # song= loadedSongs.pop(0) # removes first song and sets song equal to it
                
                # song= [track_id,[ [current_playlist,dateAdded] ],name,[artists]]
                trackId= song[0]
                while True:
                    all_trackIds= data.r_nestedElem(0,loadedSongs) # run everytime to update (0 refers to id)
                    if trackId in all_trackIds:# if duplicate exists
                        temp= loadedSongs.pop(all_trackIds.index(trackId))  # removes duplictate song and sets temp equal to it
                        # combine duplicated song data
                        song[1].append(temp[1][0])# song[1]= [[current_playlist_a,dateAdded_a],[current_playlist_b,dateAdded_b]]
                        song[1]= sorted(song[1], key= lambda playDate: datetime.strptime(playDate[1],'%Y-%m-%d').timestamp()) # sorts list of current playlists by date added
                    else:break
                loaded_songData[trackId]= song[1:] # [ [ [cur play,date] ],name,artist]
                pos+=1
                # print('%s/%s' % (pos, total), end= '\r')
                spotify.update_ui(percent= round((pos/total)*100), update_progress= update_progress)
                # loaded_songData should be { id: [ [curPlaylist,dateAdded] ]],id: [ [curPlaylistA,dateAddedA],[curPlaylistB,dateAddedB] ] }
                # when value in loaded_songData has more than one elem it is duplicated
            #songData format
            # 'track_id':['date first added', 'name', ['artist'], (current playlist/s)[['current playlist','date added'], ...], 'missing', 'deleted]
            data.load_songData()
            # if update_ui != None: update_ui(percent=50)
            # for saved tracks
            text= 'total songs: %s' % total
            for trackId in songData:
                song= songData[trackId]
                if trackId in loaded_songData: 
                    song[4]= 'false' # set missing value
                    song[5]= 'notConf' # set deleted value to not Confirmed so if missing user has to set deleted to either true or false
                    # loaded song= [ [curPlaylist,dateAdded],name ,[aritists,..] ]
                    loadedSong= loaded_songData[trackId]
                    if song[3] != loadedSong[0]:# if current playlists have changed update songData
                        tempSong= loadedSong[0]
                        for playlist in song[3]:
                            # playlist= [playlist,date added]
                            if playlist not in loadedSong[0]:
                                temp= '%s removed from %s' % (song[1], ids_playlists[playlist[0]])
                                data.add_log(temp)
                                text+=temp
                                print(temp) ## throwing key error if duplicate in same playlist removed?
                            else:
                                tempSong.remove(playlist) # remove playlists that are present in both leaving only new playlists

                        if tempSong != []: # if new playlist ^^ added
                            temp=  '%s added to %s'% (song[1], ids_playlists[tempSong[0][0]])
                            data.add_log(temp)
                            text+=temp
                            print(temp) ## throwing key error if duplicate in same playlist removed?

                        song[3]= loadedSong[0] # current playlists updated
                        
                        
                    if song[1] != loadedSong[1] or song[2] != loadedSong[2]:# if name or artist changed then update   
                        temp= 'Name or artists changed from\n%s %s to %s %s' %(song[1],  ','.join(song[2]), loadedSong[1], ','.join(loadedSong[2]))
                        data.add_log(temp)
                        print(temp)
                        if input('Confirm rename? y/n(add to gui somehow)') == 'y':
                            song[1]= loadedSong[1]
                            song[2]= loadedSong[2]

                    # remove song from loaded_songData to leave only new songs
                    del loaded_songData[trackId]
                else: 
                    # song is missing/deleted
                    if song[4] == 'false': # first time recorded as missing
                        data.add_log('%s - %s is missing' % (song[1],  ','.join(song[2])))
                    song[4]= 'true' # missing tag updated
                songData[trackId]= song # songData updated with new values
            spotify.update_ui(text= text, update_label= update_label)
            # if update_ui != None: update_ui(percent=75)
            # new songs
            # only new songs left in loaded data
            if loaded_songData != {}: # if new songs exist
                numNew= len(loaded_songData)
                temp= '\nAdding %s new song(s)' % numNew
                data.add_log(temp)
                print(temp)
                for pos,newTrackId in enumerate(loaded_songData):
                    print('%s/%s' % (pos, numNew), end= '\r')
                    song= loaded_songData[newTrackId]# [ [ [cur playlist, date added ], []... ], name, [artists]]
                    playlist_date= song[0]
                    dateFirstAdded= playlist_date[0][1] # first date recorded as loaded song data is sorted
                    # name, artist= spotify.get_nameArtist(sp, newTrackId) # if track worked i would have used this but i have to add names from search through playlist now :(
                    name= song[1]
                    artist= song[2]
                    songData[newTrackId]= [dateFirstAdded,name,artist,playlist_date,'false','false'] # not missing or deleted # could be added to multiple new playlists?
                    temp= '%s, %s added to %s' % (name, artist[0], ids_playlists[playlist_date[0][0]])
                    data.add_log(temp)
                    print(temp)
            data.save_songData()
            data.totalSongs()
            spotify.update_ui(text= 'Done', update_label= update_label)



## update with gui
    def get_keys(): # returns client id, client secret
        accessLoc= 'spotify access.txt'
        if not exists(accessLoc):
            cid=input('File %s does not exist\nInput client id: ' % accessLoc)
            secret= input('Input client secret: ')
            data.createFile(accessLoc, string= cid+'\n'+secret)
        else:
            with open(accessLoc,'r',encoding= 'utf-8') as keys:
                keys= keys.readlines()
                cid= keys[0].replace('\n','')
                secret= keys[1]
        return cid , secret

## update with gui
    # def user_playlists(sp,saved_ids_playlists={}): 
    # # creates dict of found(within saved ids) user made playlists (id; name) for downloading
    # # DO NOT PARSE SAVED PLAY IDS IF FIRST TIME SETUP
    #     ids_playlists={}
    #     results = sp.current_user_playlists(limit=50)# if you have more than 50 playlists i dont like you :)
    #     pos=0
    #     for i in results['items']:
    #         if i['owner']['id'] == my_id:
    #             ids_playlists[results['items'][pos]['uri']]= results['items'][pos]['name']
    #             if saved_ids_playlists != {}: # remove the ones not needed useful option for first set up to find all playlists if needed
    #                 for play_id in list(ids_playlists.keys()):
    #                     if play_id not in list(saved_ids_playlists.keys()): del ids_playlists[play_id]
    #         pos+=1

    #     if saved_ids_playlists == {}: 
    #         print('Found %s user playlists:' % len(ids_playlists))    
    #         for i,item in enumerate(ids_playlists.keys()):
    #             print(i+1,ids_playlists[item]+ ' ---> '+ item) #newest name used (but saved with oldest name) incase user changes playlist id
    #         del_list= []
    #         for item in ids_playlists.keys():
    #             if input('save %s?[y]' % ids_playlists[item]) != 'y':
    #                 del_list.append(item)
    #                 print('deleted')
    #         for item in del_list:
    #             del ids_playlists[item]
    #     else: 
    #         print('Found %s user playlists for download:\n' % (str(len(ids_playlists))+'/'+ str(len(saved_ids_playlists))))
    #         for i in ids_playlists.keys():
    #             print(ids_playlists[i]) #newest name used (but saved with oldest name) incase user changes playlist idi actually resaved with new name
    #     print()
    #     print('Loading...',end='\r')
    #     return ids_playlists



## major change needed ? move to data
    def update_saved_ids_playlists(saved_ids_playlists,update_dict): # replaces old playlist names with new ones
        for i in list(update_dict.keys()):
            saved_ids_playlists[i]= update_dict[i]
        return saved_ids_playlists

    ## gui
    def search(searchString):
        searchString= searchString.lower()
        results= []
        for pos, data in enumerate(songData.values()):
            if data[5] != 'true': # if not deleted
                if searchString in data[1].lower(): # artist name
                    results.append(pos)
                for artistName in data[2]:
                    if searchString in artistName.lower():
                        if pos not in results: results.append(pos) # could have already been adde

        # Ids= list(songData.keys())
        # for pos in results:
        #     song= songData[Ids[pos]]
        #     name= song[1]
        #     artist= song[2][0]
        #     currentPlaylist= ids_playlists[song[3][0][0]]
        #     print('%s, %s --- %s' % (name,artist, currentPlaylist))

        results= [list(songData.keys())[pos] for pos in results] # turns list of positions into correlated song ids from songData
        return results

    def followArtistsInPlaylists(update_label, update_progress, playlistId): # follows artists that have more than one song in the playlist
        tempArtists= []
        toFollow= []
        playlistSongs= []
        sp= spotify.getSp(my_id)
        length= len(songData)
        spotify.update_ui(percent= 0, update_progress= update_progress)
        spotify.update_ui(text= 'Collecting songs from playlist...', update_label= update_label)
        for pos,Id in enumerate(songData):
            data= songData[Id]
            if data[3][0][0] == playlistId:  # current playlist id
                playlistSongs.append(Id)
            spotify.update_ui(percent= round((pos/length)*100), update_progress= update_progress)
                
        spotify.update_ui(text= 'Converting track ids to artist ids...', update_label= update_label)
        spotify.update_ui(percent= 0, update_progress= update_progress)
        length= len(playlistSongs)
        if length > 50:
            pos= 50
            while pos <= length+ 49:
                tempArtists.extend([ song['artists'][0]['id'] for song in sp.tracks(playlistSongs[pos-50:pos])['tracks']])
                spotify.update_ui(percent= round((pos/length)*100), update_progress= update_progress)
                pos+=50
        else:
            tempArtists= [ song['artists'][0]['id'] for song in sp.tracks(playlistSongs)['tracks']]
            spotify.update_ui(percent= 100, update_progress= update_progress)
                
        while tempArtists != []:
            artistId= tempArtists.pop(0)
            if artistId in tempArtists: # if multiple songs by artists exist in playlist
                while True:
                    try:
                        tempArtists.remove(artistId)
                    except:
                        break
                toFollow.append(artistId)
        

        following= []
        pos= 50
        spotify.update_ui(text= 'Finding followed artists...', update_label= update_label)
        while pos <= len(toFollow)+ 49:
            following.extend(sp.current_user_following_artists(toFollow[pos-50:pos])) # has a limit even though docs do not mention it
            pos+=50

        total= 0
        for i in following: 
            if not i: total+=1
        print(total)

        if total == 0: 
            spotify.update_ui(text= 'No artists to follow', update_label= update_label)
            return

        # self.sp.user_follow_artists(artists) # can do entire list of artists at once(probs max 50 at a time)
        length= len(toFollow)
        for pos, artistId in enumerate(toFollow):
            if not following[pos]: # if not following artist
                name= sp.artist(artistId)['name']
                temp= 'Followed %s' % name
                data.add_log(temp)
                spotify.update_ui(text= temp, update_label= update_label)
                spotify.update_ui(percent= round((pos/length)*100), update_progress= update_progress)
                sp.user_follow_artists([artistId])
        spotify.update_ui(percent= 100, update_progress= update_progress)
        spotify.update_ui(text= 'Finished', update_label= update_label)
        



#on start 
print('newly missing songs do not end up in unonfirmed area after running once deleteing then running again also happens when just deleted???')
seperator= "%$%"
seperator2= "$%$"


# if auto run just close if id and stuff is missing and dont run gui
my_id= data.get_last_user_id() # might do weird shit cus i changed this from user_id
if my_id == '': # if no last user means this is first open
    if __name__ != '__main__':
        data.add_log('!! NO LAST USER PROGRAM ENDED !!')
        quit()
    else: print('create a user')
data.get_id_user()
data.changeActiveUser(my_id) #updates user to latest
data.get_allowedDup()


if __name__ == '__main__':
    # from followArtists import followArtists as fA
    # fA('spotify:playlist:33JwDwoh3u3HjKix4i995j' ,songData, spotify.getSp())
    # input('this is an input')
    #gui
    # spotify.updateSongs()
    # data.totalSongs() 
      
    # while True: 
    #     results= spotify.search(input())
    #     if results != []:
    #         for i in results:
    #             print('%s:%s' % (i,songData[i][1]))
    #     else: print('no songs')
    app = QApplication([])
    window = MainWindow()
    window.show()

    # run should also add search
    # spotify.updateSongs()
    # then have button
    # print(data.totalSongs())
    # then have button for accept or not
    app.exec()

else:
    spotify.updateSongs()



