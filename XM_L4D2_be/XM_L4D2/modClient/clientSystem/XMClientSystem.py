import mod.client.extraClientApi as clientApi
from common.utils.mcmath import Vector3
import math  # 添加math模块导入
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

playerId = clientApi.GetLocalPlayerId()
levelId = clientApi.GetLevelId()

# 在modMain中注册的Client System类
class XMClientSystem(ClientSystem):

    # 客户端System的初始化函数
    def __init__(self, namespace, systemName):
        super(XMClientSystem, self).__init__(namespace, systemName)
        self.shijian()
 
    #检测客户端玩家长按屏幕事件
    def shijian(self):
        self.ListenForEvent("XM_L4D2","XMServerSystem","RenderL4d2Player", self, self.RenderL4d2Player)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "RightClickBeforeClientEvent", self, self.Gun)
        # self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "PlayerAttackEntityEvent", self, self.attack)


    # def attack(self,args):
    #     # 获取玩家位置组件并获取当前坐标
    #     playerId = args["playerId"]
    #     victimId = args["victimId"]
        
    #     # 创建生物渲染组件（需要指定生物ID）
    #     comp = clientApi.GetEngineCompFactory().CreateActorRender(levelId, victimId)
        
    #     # 获取生物当前的动画状态参数
    #     animState = comp.GetActorRenderParams("animation_state")
    #     currentAnim = comp.GetActorRenderParams("current_animation")
        
    #     # 在聊天框显示生物动画状态（比print更直观）
    #     chatComp = clientApi.GetEngineCompFactory().CreateChat(playerId)
    #     chatComp.AddChatMessage(f"生物动画状态: {animState}, 当前动画: {currentAnim}")
        
    #     # 保留原有的打印调试信息
    #     textureKeys = comp.GetActorRenderParams("animations")
    #     print(f"生物动画参数: {textureKeys}")


#玩家使用物品
    def Gun(self,args):
        # 获取玩家位置组件并获取当前坐标
        playerComp = compFactory.CreatePos(playerId)
        playerPos = playerComp.GetPos()  # 获取玩家当前位置
        
        # 获取玩家手持物品信息
        comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
        carriedData = comp.GetCarriedItem()
        newItemName = carriedData["newItemName"]
        
        # 当手持物品为骨头时触发箭矢发射逻辑
        if newItemName == "minecraft:bone":
            # 构建事件数据，包含服务器创建箭矢所需的所有参数
            argsDict = self.CreateEventData()
            argsDict["playerId"] = playerId          # 玩家ID
            argsDict["playerPos"] = playerPos  
            # 通知服务器处理箭矢创建（客户端无权限直接创建实体）
            self.NotifyToServer("RightClickBeforeClientEvent", argsDict)
        # 当手持物品为骨头时触发箭矢发射逻辑
        if newItemName == "xm_l4d2:select_player":
            # 构建事件数据，包含服务器创建箭矢所需的所有参数
            argsDict = self.CreateEventData()
            argsDict["playerId"] = playerId          # 玩家ID
            argsDict["playerPos"] = playerPos  
            # 通知服务器处理箭矢创建（客户端无权限直接创建实体）
            self.NotifyToServer("xm_l4d2:select_player", argsDict)
            self.showUI()



    def RenderL4d2Player(self, args):
        playerId = args["playerId"]

        comp = clientApi.GetEngineCompFactory().CreateActorRender(playerId)
        comp.AddPlayerGeometry("default", "geometry.l4d2.bill")
        comp.AddPlayerTexture("default", "textures/l4d2/player/bill")
        # 添加新的动画控制器
        comp.AddPlayerAnimationController("root", "controller.animation.steve.root_controller")
        comp.AddPlayerAnimationController("third_person_controller", "controller.animation.steve.third_person_controller")
        comp.AddPlayerAnimationController("third_person_controller.move_controller", "controller.animation.steve.third_person_controller.move_controller")
        # 添加新的动画
        comp.AddPlayerAnimation("idle_ram", "animation.steve.idle_ram")
        comp.AddPlayerAnimation("idle_leg", "animation.steve.idle_leg")
        comp.AddPlayerAnimation("walk_arm", "animation.steve.walk_arm")
        comp.AddPlayerAnimation("walk_leg", "animation.steve.walk_leg")
        comp.AddPlayerAnimation("run_arm", "animation.steve.run_arm")
        comp.AddPlayerAnimation("run_leg", "animation.steve.run_leg")
        comp.AddPlayerAnimation("jump_arm", "animation.steve.jump_arm")
        comp.AddPlayerAnimation("jump_leg", "animation.steve.jump_leg")
        comp.AddPlayerAnimation("jump_move_arm", "animation.steve.jump_move_arm")
        comp.AddPlayerAnimation("jump_move_leg", "animation.steve.jump_move_leg")
        comp.AddPlayerAnimation("jump_remove_arm", "animation.steve.jump_remove_arm")
        comp.AddPlayerAnimation("jump_remove_leg", "animation.steve.jump_remove_leg")
        comp.AddPlayerAnimation("sneak_arm", "animation.steve.sneak_arm")
        comp.AddPlayerAnimation("sneak_leg", "animation.steve.sneak_leg")
        comp.AddPlayerAnimation("down", "animation.steve.down")
        comp.AddPlayerAnimation("landing", "animation.steve.landing")
        comp.AddPlayerAnimation("landing_2", "animation.steve.landing_2")
        comp.AddPlayerAnimation("first_person_base", "animation.steve.first_person_base")
        comp.AddPlayerAnimation("third_person_base", "animation.steve.third_person_base")
        comp.RebuildPlayerRender()

    def showUI(self):
        # 获取UI组件
        uiComp = clientApi.GetEngineCompFactory().CreateUI(playerId)
        # 加载UI文件（假设UI文件位于ui目录下的l4d2_ui.json）
        uiComp.LoadUI("ui/l4d2_ui.json")
        # 显示UI界面
        uiComp.ShowUI()