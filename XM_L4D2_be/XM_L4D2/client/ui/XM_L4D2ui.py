# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import mod.client.extraClientApi as clientApi



ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()
playerId = clientApi.GetLocalPlayerId()
# 所有的UI类需要继承自引擎的ScreenNode类


class XM_L4D2Screen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        # 系统变量
        self.mXitong = param["xitong"]
        self.ClientSystem = clientApi.GetSystem("XM_L4D2", "XMClientSystem")

        # 添加冷却时间相关变量，默认0.5秒
        # self.mCooldownTime = param.get("cooldown_time", 1)
        # 确保冷却状态变量始终存在
        self.mIsInCooldown = False

        # UI元素路径定义
        self.mButtonPanel = "/XM_L4D2_panel"  # 按钮面板路径
        self.mAttackButton = self.mButtonPanel + \
            "/XM_L4D2_melee_attack_button"  # 瞄准按钮路径

    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        self.uiNode = clientApi.GetUI("XM_L4D2", "XM_L4D2UI")
        #点击右侧技能选项
        buttonyyf = self.uiNode.GetBaseUIControl(self.mAttackButton).asButton()  # 获取按钮对象
        buttonyyf.AddTouchEventParams({"isSwallow": True})  # 设置按钮吞噬事件
        buttonyyf.SetButtonTouchDownCallback(self.OnAttackButtonTouch)  # 设置点击回调
        #buttonyyf.SetButtonTouchUpCallback(self.UpCallback)  # 设置弹起

    def SetCooldown(self):
        # cd
        mCooldownTime = 0.625
        """设置按钮进入冷却状态"""
        if self.mIsInCooldown:
            return

        self.mIsInCooldown = True
        # 使用定时器在冷却时间后重置状态
        # 修复：使用正确的客户端定时器组件
        gameComp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        gameComp.AddTimer(mCooldownTime, self.ResetCooldown)

    def ResetCooldown(self):
        """重置按钮冷却状态"""
        self.mIsInCooldown = False

    # 绑定了射击按钮的 Up 点击事件
    def OnAttackButtonTouch(self, args):
        if self.mIsInCooldown:
            return
        # 设置按钮进入冷却状态
        self.SetCooldown()

        argsDict = self.mXitong.CreateEventData()
        argsDict["playerId"] = playerId          # 玩家ID
        argsDict["state"] = 1        #触发动画
        # 通知服务器处理箭矢创建（客户端无权限直接创建实体）
        self.mXitong.NotifyToServer("RenderL4d2PlayerAnim", argsDict)

        # 延迟0.13秒后发送事件到服务端
        gameComp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        gameComp.AddTimer(0.13, self.SendGunEvent)


    def SendGunEvent(self):
        """延迟发送Gun事件到服务端"""
        # 构建事件数据，包含服务器创建箭矢所需的所有参数
        argsDict = self.mXitong.CreateEventData()
        argsDict["playerId"] = playerId          # 玩家ID
        # 通知服务器处理箭矢创建（客户端无权限直接创建实体）
        self.mXitong.NotifyToServer("Gun", argsDict)


        # def UpCallback(self, args):
        #     pass

        # tick +=1
        # if tick % 60 == 0:
        #     pass

        #print("{}".format(playerId))

        # selectedControl = self.uiNode.GetBaseUIControl("/skill_panel_main/label").asLabel()
        # selectedControl.SetText("x:{}/j:{}".format(1,2))
