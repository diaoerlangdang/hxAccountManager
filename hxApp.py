#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 2018-1-4

@author: wise
'''
import wx
import hx
import _thread
import time

EVT_RESULT_ID = wx.NewId()  

def EVT_RESULT(win, func):  
    """Define Result Event."""  
    win.Connect(-1, -1, EVT_RESULT_ID, func)  


class ResultEvent(wx.PyEvent):  
    """Simple event to carry arbitrary result data."""  
    def __init__(self, data, success=True, errMsg=''):  
        """Init Result Event."""  
        wx.PyEvent.__init__(self)  
        self.SetEventType(EVT_RESULT_ID)  
        self.data = data  
        self.success = success
        self.errMsg = errMsg

class TestApp(wx.Frame):
    def __init__(self,parent,title):
        super(TestApp,self).__init__(parent,title=title,size=(500,300))
        #最小大小
        self.SetMinSize((500, 300))
        #初始化ui
        self.InitUI()
        #居中
        self.Centre()
        #显示
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        
        font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        
        titleFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        #间隙
        hvGap = 5;

        #主布局、水平
        mainHBox = wx.BoxSizer(wx.HORIZONTAL)

        #左侧布局、垂直
        leftVBox = wx.BoxSizer(wx.VERTICAL)

        #案例标题
        st1 = wx.StaticText(panel,label=u'用户列表')
        st1.SetFont(titleFont)
        leftVBox.Add(st1,flag=wx.LEFT|wx.RIGHT|wx.TOP, border = hvGap)

        #案例列表
        self.checkListBox =  wx.CheckListBox(panel, choices = [])
        self.Bind(wx.EVT_CHECKLISTBOX, self.onCheckListBoxSelect, self.checkListBox)
        leftVBox.Add(self.checkListBox, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = hvGap)
        leftVBox.Add((-1, 10))

        #全选
        self.selectAllCheckBox = wx.CheckBox(panel, label=u'全选', style=wx.CHK_3STATE)
        self.selectAllCheckBox.SetFont(font)
        self.Bind(wx.EVT_CHECKBOX, self.onCheckBoxSelectAll, self.selectAllCheckBox)
        leftVBox.Add(self.selectAllCheckBox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = hvGap)

        leftVBox.Add((-1, 10))


        # mainHBox.Add(leftVBox, proportion = 1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = hvGap)

        
        '''
        #右侧布局、垂直
        rightVBbox = wx.BoxSizer(wx.VERTICAL)

        #日志标题
        st2 = wx.StaticText(panel,label=u'日志')
        st2.SetFont(titleFont)
        rightVBbox.Add(st2,flag=wx.LEFT|wx.RIGHT|wx.TOP, border = hvGap)
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.logTextCtrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        hbox3.Add(self.logTextCtrl, proportion=1, flag=wx.EXPAND)
        rightVBbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND|wx.TOP, 
            border=hvGap)

        rightVBbox.Add((-1, 10))'''

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)

        #刷新列表
        self.refreshBtn = wx.Button(panel, label=u'刷新列表', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.onClickedRefreshBtn, self.refreshBtn)
        hbox5.Add(self.refreshBtn, flag=wx.LEFT|wx.BOTTOM, border=5)

        #删除按钮
        self.deleteBtn = wx.Button(panel, label=u'删除', size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.onClickedDeleteBtn, self.deleteBtn)
        hbox5.Add(self.deleteBtn, flag=wx.LEFT|wx.BOTTOM, border=5)

        
        leftVBox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=hvGap)

        mainHBox.Add(leftVBox, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = hvGap)
        
        panel.SetSizer(mainHBox)

        #默认全选
        # self.selectAllCheckBox.Set3StateValue(wx.CHK_CHECKED)
        # self.selectListAll(True)
        # self.checkListBox.SetSelection(1) #选中某行
        #self.checkListBox.SetSelection(-1) #取消选中

        EVT_RESULT(self, self.updateCheckListBox)  

        self.dlg = None

        self.memberListInfo = []

        if hx.configInfo.init_config():
            self.show_members()
            pass
        else:
            self.showError('配置文件错误')

        


    #显示错误
    def showError(self, message):
        messageDlg = wx.MessageDialog(self,message, caption=u'错误', style = wx.OK|wx.CENTRE|wx.ICON_ERROR)
        messageDlg.SetOKLabel(u'确定')
        messageDlg.Centre()
        messageDlg.ShowModal()
        messageDlg.Destroy()
        pass

    #更新界面
    def updateCheckListBox(self, msg):
        
        if msg.success:
            info = msg.data
            if isinstance(info,list):
                self.checkListBox.Items = info
            pass
        else :
            errMsg = msg.errMsg
            self.showError(errMsg)

        pass
    

    def get_members(self):
        listInfo = []
        memberList = hx.sql_query_member()
        if memberList is None:
            return None
            pass
        for member in memberList:
            self.memberListInfo.append(member)
            memberInfo = ''
            for key, info in member.items():
                memberInfo = memberInfo + str(info).ljust(30)# + '        '
                pass
            pass
            listInfo.append(memberInfo)

        return listInfo
        pass


    def show_members_thread(self, args):

        listInfo = self.get_members()

        if listInfo is None:
            wx.PostEvent(self, ResultEvent(listInfo, False, '数据库连接失败，请检查网络'))
            pass
        else :
            wx.PostEvent(self, ResultEvent(listInfo))

        
        pass

    def show_members(self):
        _thread.start_new_thread( self.show_members_thread, ('',) )
        pass

    #check列表 是否选中
    def onCheckListBoxSelect(self,event):
        #选中个数
        selectCount = len(self.checkListBox.GetCheckedItems())

        #全不选
        if selectCount == 0:
            self.selectAllCheckBox.Set3StateValue(wx.CHK_UNCHECKED)
            pass
        #全选
        elif selectCount == self.checkListBox.GetCount():
            self.selectAllCheckBox.Set3StateValue(wx.CHK_CHECKED)
            pass
        #未全选
        else:
            self.selectAllCheckBox.Set3StateValue(wx.CHK_UNDETERMINED) 
            pass
        pass

    #全选check box
    def onCheckBoxSelectAll(self, event):
        self.selectListAll(self.selectAllCheckBox.Get3StateValue() == wx.CHK_CHECKED)
        # self.checkListBox.SetChoice([u'测试案例1\t姓名',u'测试案例2',u'测试案例3'])
        pass

    #设置check box 不全选，需要checkBox支持3个状态，checkBox 为控件
    def setCheckBoxSelectNotAll(self, checkBox):
        checkBox.Set3StateValue(wx.CHK_UNDETERMINED)
        pass

    #选中所有或全部不选 isSelected=true 为全选；否则为全不选
    def selectListAll(self,isSelected):

        #全选
        if isSelected:
            #全选
            self.checkListBox.SetCheckedItems(range(0,self.checkListBox.GetCount()))
            pass
        else :
            #全不选
            self.checkListBox.SetCheckedItems([]) 
            pass
        pass

    #刷新串口列表
    def onClickedRefreshBtn(self,event):
        print(u'刷新列表')
        if hx.configInfo.init_config():
            self.show_members()
            self.selectAllCheckBox.Set3StateValue(wx.CHK_UNCHECKED)
            pass
        else:
            self.showError('配置文件错误')
        
        pass

    #删除
    def onClickedDeleteBtn(self,event):

        messageDlg = wx.MessageDialog(self, '确定要删除选中的数据吗？', caption=u'提示', style = wx.OK|wx.CENTRE|wx.CANCEL|wx.ICON_INFORMATION)
        messageDlg.SetOKCancelLabels(u'确定', '取消')
        messageDlg.Centre()
        result = messageDlg.ShowModal()
        messageDlg.Destroy()

        if wx.ID_OK == result:
            print(u'删除')
            self.delete_members()
            pass
        pass

    def delete_members_thread(self, memberList):

        for member in memberList:

            if not (hx.configInfo.major_key in member.keys()):
                self.dlg.EndModal(wx.ID_OK)
                self.dlg.Destroy()
                wx.PostEvent(self, ResultEvent(None, False, '配置文件错误'))
                return
                pass

            userId = member[hx.configInfo.major_key]
            self.dlg.setLabelInfo('删除用户'+str(userId)+'中...')
            if not hx.sql_delete_user(str(userId)) :
                self.dlg.EndModal(wx.ID_OK)
                self.dlg.Destroy()
                wx.PostEvent(self, ResultEvent(None, False, '删除数据失败，请检查网络'))
                return
            pass
        
        self.dlg.setLabelInfo('更新用户列表...')
        listInfo = self.get_members()

        self.dlg.EndModal(wx.ID_OK)
        self.dlg.Destroy()

        self.checkListBox.Items = listInfo
        self.selectAllCheckBox.Set3StateValue(wx.CHK_UNCHECKED)
        
        pass

    def delete_members(self):

        memberList =  [self.memberListInfo[x] for x in self.checkListBox.GetCheckedItems()]
        if len(memberList) <= 0:
            return

        self.dlg = ProgressDialog(self, u'操作中')
        self.dlg.setLabelInfo('删除用户中...')

        _thread.start_new_thread( self.delete_members_thread, (memberList,) )

        self.dlg.ShowModal()

        pass


''' 登录或者修改密码 对话框 '''
class ProgressDialog(wx.Dialog):
    """docstring for ProgressDialog"""

    #model 为模式 0 为登录 1 为修改密码
    def __init__(self, parent, title):
        super(ProgressDialog, self).__init__(parent, title = title, size = (250,140), style=wx.CAPTION) 

        #初始化ui
        self.InitUI()

        #居中
        self.Centre()
        pass

    def InitUI(self):

        panel = wx.Panel(self)

        hvGap = 5

        mainVBox = wx.BoxSizer(wx.VERTICAL)

        mainVBox.Add((-1,20))

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.label = wx.StaticText(panel,label=u'')
        hbox.Add(self.label,flag=wx.LEFT|wx.RIGHT|wx.TOP, border = hvGap)

        mainVBox.Add(hbox, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.TOP, border = hvGap)


        panel.SetSizer(mainVBox)

        pass

    #设置标签信息
    def setLabelInfo(self, info):
        self.label.SetLabel(info)
        pass


        
if __name__ == '__main__':
    app = wx.App()
    TestApp(None,title=u"账号（环信）管理工具")
    app.MainLoop()