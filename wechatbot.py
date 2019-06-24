import itchat
import requests

global user
global user_word
global xb 
global mode
global groupname 
global needAt
user = ''
user_word = ''
mode = 0
groupname = ''
needAt = True

@itchat.msg_register(itchat.content.TEXT)
def individual_msg(msg):
    global user
    global user_word
    global mode
    global groupname
    global needAt
    #print('receive individual msg:'+msg.text+' user:'+msg['FromUserName'])
    if msg.text == 'mode0': #No robot
        print('mode0')
        mode = 0
    elif msg.text == 'mode1': #individual robot
        print('mode1')
        mode = 1
    elif msg.text.startswith('mode2 '): #group robot
        print('mode2')
        mode = 2
        needAtNum = msg.text[6]
        if needAtNum == '1':
            needAt = True
        else:
            needAt = False
        groupname = msg.text[8:]
        print('groupname:'+groupname)
        #group = itchat.search_chatrooms(name=groupname)
    else:
        if mode == 1:
            user = msg['FromUserName']
            itchat.send_msg(msg.text, xb)

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_msg(msg):
    global groupname 
    global needAt
    print(msg['User']['NickName'])
    if mode == 2 and msg['User']['NickName'] == groupname:
        if not needAt or (needAt and msg.isAt):
            user = msg['FromUserName']
            itchat.send_msg(msg.text, xb)
        #if len(group) > 0:
           # itchat.send_msg(msg.text, group[0]['UserName'])

@itchat.msg_register(itchat.content.TEXT, isMpChat=True) #xiaobing's response
def public_msg(msg):
    print('xiaobing msg')
    if mode == 1:
        print('mode == 1')
        itchat.send_msg(msg.text, user)
    elif mode == 2:
        print('mode == 2')
        group = itchat.search_chatrooms(name=groupname)
        if len(group) > 0:
            itchat.send_msg(msg.text, group[0]['UserName'])

itchat.auto_login(True)
xiaobing = itchat.search_mps(name='小冰')
xb = xiaobing[0]['UserName']

itchat.run()