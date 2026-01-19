# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import mod.client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()
from mod_log import logger
from XM_L4D2.modConfig import modConfig

# 所有的UI类需要继承自引擎的ScreenNode类
class XML4D2Screen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        # 这个变量保存了控制视野范围的变量
        self.mOriginalFov = 1.0
        # 这个变量保存了是否显示瞄准界面
        self.mShowSight = False
        # 这个变量保存了当前视角（0表示第一人称，1表示第三人称等）
        self.mPersective = 0
        # 当前客户端的玩家Id
        self.mPlayerId = clientApi.GetLocalPlayerId()
        # 射击组件，用于处理射击逻辑
        self.mShootComp = None

        # UI元素路径定义
        self.mButtonPanel = "/XM_L4D2_panel"  # 按钮面板路径
        self.mAttackButton = self.mButtonPanel + "/XM_L4D2_melee_attack_button"  # 瞄准按钮路径
        # self.mShootButtonRight = self.mButtonPanel + "/shootButtonRight"  # 右射击按钮路径
        # self.mShootButtonLeft = self.mButtonPanel + "/shootButtonLeft"  # 左射击按钮路径
        # self.mChangeButton = self.mButtonPanel + "/changeButton"  # 换子弹按钮路径
        # self.mAimPanel = "/aimPanel"  # 瞄准面板路径
        # self.mAimImage = self.mAimPanel + "/aimImage"  # 准星图像路径
        # self.mAimingImage = self.mAimPanel + "/aimingImage"  # 瞄准镜图像路径

    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        logger.info("===== XML4D2Screen Create =====")
        # 为各个按钮添加触摸事件处理器
        self.AddTouchEventHandler(self.mAttackButton, self.OnShootButtonTouch, {"isSwallow": True})

    # 界面的一些初始化操作
    def Init(self):
        # 隐藏原生的中心图标（游戏默认的准星）
        self.SetCrossHair(False)
        # 隐藏瞄准界面（初始状态不显示瞄准镜图像）
        self.SetVisible(self.mAimingImage, False)
        # 获取原始情况下的视野范围大小
        cameraComp = clientApi.CreateComponent(clientApi.GetLevelId(), modConfig.Minecraft, modConfig.CameraComponent)
        clientApi.CreateComponent(self.mPlayerId, modConfig.Minecraft, modConfig.ModelCompClient)
        self.mOriginalFov = cameraComp.GetFov()
        # 创建射击组件实例
        self.mShootComp = clientApi.CreateComponent(self.mPlayerId, modConfig.ModName, modConfig.ClientShootComponent)

    # 绑定了瞄准按钮的 Down 点击事件
    def OnAimButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        # 点击坐标
        touchPos = args["TouchPosX"], args["TouchPosY"]
        # 触控在按钮范围内弹起时
        if touchEvent == touchEventEnum.TouchUp:
            logger.info("============= touch up  =========")
        # 按钮按下时
        elif touchEvent == touchEventEnum.TouchDown:
            self.Aim()
            logger.info("============= touch down  =========")
        # 触控在按钮范围外弹起时
        elif touchEvent == touchEventEnum.TouchCancel:
            logger.info("============= touch cancel  =========")
        # 按下后触控移动时
        elif touchEvent == touchEventEnum.TouchMove:
            logger.info("============= touch move  =========")

    # 绑定了射击按钮的 Up 点击事件
    def OnShootButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        # 只在按钮弹起时执行射击
        if touchEvent == touchEventEnum.TouchUp:
            self.Shoot()

    # 绑定了换子弹的按钮事件，但是没有写逻辑
    def OnChangeButtonTouch(self, args):
        logger.info("============= touch change button  =========")

    # 继承自ScreenNode的方法，会被引擎自动调用，1秒钟30帧
    def Update(self):
        """
        node tick function
        """
        pass

    # 瞄准按钮的逻辑
    def Aim(self):
        # 如果当前是开镜状态，关闭开镜UI并恢复视野范围，并显示角色
        if self.mShowSight:
            self.mShowSight = False  # 切换为非瞄准状态
            self.UpdateCrossHairShow()  # 更新准星显示
            self.SetVisible(self.mAimingImage, False)  # 隐藏开镜瞄准图像
            # 恢复原始视野范围
            cameraComp = clientApi.GetComponent(clientApi.GetLevelId(), modConfig.Minecraft, modConfig.CameraComponent)
            cameraComp.SetFov(self.mOriginalFov)
            # 显示玩家角色模型
            modelComp = clientApi.GetComponent(self.mPlayerId, modConfig.Minecraft, modConfig.ModelCompClient)
            modelId = modelComp.GetModelId()
            modelComp.ShowModel(modelId)
        # 如果当前是不开镜状态，那么就开镜并调整视野范围，并隐藏角色
        else:
            self.mShowSight = True  # 切换为瞄准状态
            self.UpdateCrossHairShow()  # 更新准星显示
            self.SetVisible(self.mAimingImage, True)  # 显示开镜瞄准图像
            # 缩小视野范围（模拟开镜效果）
            cameraComp = clientApi.GetComponent(clientApi.GetLevelId(), modConfig.Minecraft, modConfig.CameraComponent)
            cameraComp.SetFov(self.mOriginalFov + modConfig.SightFieldOfView)  # 视野值通过配置调整
            # 隐藏玩家角色模型（第一人称开镜时隐藏自身模型）
            modelComp = clientApi.GetComponent(self.mPlayerId, modConfig.Minecraft, modConfig.ModelCompClient)
            modelId = modelComp.GetModelId()
            modelComp.HideModel(modelId)

    # 射击按钮的逻辑
    def Shoot(self):
        # 设置射击状态为True，触发射击行为
        self.mShootComp.SetShoot(True)
    
    def UpdateCrossHairShow(self):
        # 根据是否瞄准或视角状态决定是否显示准星
        if self.mShowSight or self.mPersective == 0:
            self.SetVisible(self.mAimImage, True)
        else:
            self.SetVisible(self.mAimImage, False)
