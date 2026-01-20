import mod.client.extraClientApi as clientApi
import random  # 导入random模块
from XM_L4D2.config import ModConfig as ModConfig
from XM_L4D2.config.WeaponConfig import WeaponConfig
from XM_L4D2.client.api.XM_L4D2_molang import XM_L4D2_molang

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

playerId = clientApi.GetLocalPlayerId()
levelId = clientApi.GetLevelId()

# 在modMain中注册的Client System类
class XMClientSystem(ClientSystem):

    # 客户端System的初始化函数
    def __init__(self, namespace, systemName):
        super(XMClientSystem, self).__init__(namespace, systemName)
        self.Listen()
        self.weapon_detail = WeaponConfig

        self.uiNode = None     # UI节点引用
        #模块的注册
        self.zhucemokuai()

    def zhucemokuai(self):
        self.SetMolang = XM_L4D2_molang()

    
    def Listen(self):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self, self.OnUIInitFinished)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnLocalPlayerStopLoading", self, self.OnUIInitFinished)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnCarriedNewItemChangedClientEvent", self, self.LoadL4d2Player)


        self.ListenForEvent("XM_L4D2","XMServerSystem","RenderL4d2Player", self, self.RenderL4d2Player)
        self.ListenForEvent("XM_L4D2","XMServerSystem","RenderL4d2PlayerAnim", self, self.RenderL4d2PlayerAnim)



    def OnUIInitFinished(self, args):
        clientApi.RegisterUI(ModConfig.ModName, ModConfig.XM_L4D2UIName, ModConfig.XM_L4D2UIPyClsPath,
                             ModConfig.XM_L4D2UIScreenDef)

        argsDict = self.CreateEventData()
        argsDict["playerId"] = playerId          # 玩家ID
        # 通知服务器处理箭矢创建（客户端无权限直接创建实体）
        self.NotifyToServer("RenderL4d2Player", argsDict)



    def RegisterMolang(self):
        comp = clientApi.GetEngineCompFactory().CreateQueryVariable(levelId)
        comp.Register("query.mod.l4d2_item", 0.0)
        comp.Register("query.mod.l4d2_attack", 0.0)

    # 取消定时器的辅助方法
    def cancel_timer(self, timer_id):
        try:
            clientApi.CancelTimer(timer_id)
            if timer_id in self.timer_ids:
                self.timer_ids.remove(timer_id)
        except:
            pass  # 如果定时器已取消或不存在，忽略错误



    def LoadL4d2Player(self, args):
        playerId = clientApi.GetLocalPlayerId()

        xitong = self

        # 加载UI
        # 获取玩家手持物品信息
        comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
        carriedData = comp.GetCarriedItem()

        self.uiNode = clientApi.GetUI("XM_L4D2", "XM_L4D2UI")
        if carriedData!=None:
            if carriedData["newItemName"] in self.weapon_detail:
                weapon_query_name = self.weapon_detail[carriedData["newItemName"]]["query_name"]
                weapon_query_value = self.weapon_detail[carriedData["newItemName"]]["query_value"]
                #设置molang变量
                self.SetMolang.molang(playerId, weapon_query_name, weapon_query_value)

                self.RenderL4d2Player({"playerId":playerId})
                if self.uiNode == None:
                    clientApi.CreateUI("XM_L4D2", "XM_L4D2UI", {"isHud": 1,"xitong":xitong})

            else:
                #shezhi
                self.SetMolang.molang(playerId,"l4d2_item",0.0)
                if self.uiNode != None:
                    self.uiNode.SetRemove()
        else:
            self.SetMolang.molang(playerId,"l4d2_item",0.0)
            if self.uiNode != None:
                self.uiNode.SetRemove()

    
#玩家使用物品
    def RenderL4d2PlayerAnim(self, args):
        playerId = args["playerId"]
        state = args["state"]
        # 当状态为1时触发动画
        if state == 1:
            self.SetMolang.SetMolang(playerId)
        if state == 3:
            self.SetMolang.Set_amolang(playerId)



    def RenderL4d2Player(self, args):
        playerId = args["playerId"]
        
        self.RegisterMolang()

        comp = clientApi.GetEngineCompFactory().CreateActorRender(playerId)
        comp.AddPlayerGeometry("default", "geometry.l4d2.bill")
        # 添加武器几何体配置
        comp.AddPlayerGeometry("offhand_weapon.baseball_bat", "geometry.l4d2.baseball_bat")
        comp.AddPlayerGeometry("offhand_weapon.chainsaw", "geometry.l4d2.chainsaw")
        comp.AddPlayerGeometry("offhand_weapon.cricket_bat", "geometry.l4d2.cricket_bat")
        comp.AddPlayerGeometry("offhand_weapon.crowbar", "geometry.l4d2.crowbar")
        comp.AddPlayerGeometry("offhand_weapon.electric_guitar", "geometry.l4d2.electric_guitar")
        comp.AddPlayerGeometry("offhand_weapon.fireaxe", "geometry.l4d2.fireaxe")
        comp.AddPlayerGeometry("offhand_weapon.frying_pan", "geometry.l4d2.frying_pan")
        comp.AddPlayerGeometry("offhand_weapon.golf_club", "geometry.l4d2.golf_club")
        comp.AddPlayerGeometry("offhand_weapon.katana", "geometry.l4d2.katana")
        comp.AddPlayerGeometry("offhand_weapon.knife", "geometry.l4d2.knife")
        comp.AddPlayerGeometry("offhand_weapon.machete", "geometry.l4d2.machete")
        comp.AddPlayerGeometry("offhand_weapon.nightstick", "geometry.l4d2.nightstick")
        comp.AddPlayerGeometry("offhand_weapon.pitchfork", "geometry.l4d2.pitchfork")
        comp.AddPlayerGeometry("offhand_weapon.riot_shield", "geometry.l4d2.riot_shield")
        comp.AddPlayerGeometry("offhand_weapon.shovel", "geometry.l4d2.shovel")


        comp.AddPlayerTexture("default", "textures/l4d2/player/bill")
        comp.AddPlayerTexture("offhand_weapon.baseball_bat", "textures/l4d2/models/offhand_weapon/baseball_bat")
        comp.AddPlayerTexture("offhand_weapon.chainsaw", "textures/l4d2/models/offhand_weapon/chainsaw")
        comp.AddPlayerTexture("offhand_weapon.cricket_bat", "textures/l4d2/models/offhand_weapon/cricket_bat")
        comp.AddPlayerTexture("offhand_weapon.crowbar", "textures/l4d2/models/offhand_weapon/crowbar")
        comp.AddPlayerTexture("offhand_weapon.electric_guitar", "textures/l4d2/models/offhand_weapon/electric_guitar")
        comp.AddPlayerTexture("offhand_weapon.fireaxe", "textures/l4d2/models/offhand_weapon/fireaxe")
        comp.AddPlayerTexture("offhand_weapon.frying_pan", "textures/l4d2/models/offhand_weapon/frying_pan")
        comp.AddPlayerTexture("offhand_weapon.golf_club", "textures/l4d2/models/offhand_weapon/golf_club")
        comp.AddPlayerTexture("offhand_weapon.katana", "textures/l4d2/models/offhand_weapon/katana")
        comp.AddPlayerTexture("offhand_weapon.knife", "textures/l4d2/models/offhand_weapon/knife")
        comp.AddPlayerTexture("offhand_weapon.machete", "textures/l4d2/models/offhand_weapon/machete")
        comp.AddPlayerTexture("offhand_weapon.nightstick", "textures/l4d2/models/offhand_weapon/nightstick")
        comp.AddPlayerTexture("offhand_weapon.pitchfork", "textures/l4d2/models/offhand_weapon/pitchfork")
        comp.AddPlayerTexture("offhand_weapon.riot_shield", "textures/l4d2/models/offhand_weapon/riot_shield")
        comp.AddPlayerTexture("offhand_weapon.shovel", "textures/l4d2/models/offhand_weapon/shovel")

        # 添加新的动画控制器
        comp.AddPlayerAnimationController("root", "controller.animation.steve.root_controller")
        comp.AddPlayerAnimationController("third_person_controller", "controller.animation.steve.third_person_controller")
        comp.AddPlayerAnimationController("third_person_controller.move_controller", "controller.animation.steve.third_person_controller.move_controller")

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

        comp.AddPlayerAnimationController("shovel_controller", "controller.animation.l4d2.shovel_controller")
        comp.AddPlayerAnimation("shovel_holding", "animation.steve.shovel.holding")
        comp.AddPlayerAnimation("shovel_pushing", "animation.steve.shovel.pushing")
        comp.AddPlayerAnimation("shovel_attack_1", "animation.steve.shovel.attack_1")
        comp.AddPlayerAnimation("shovel_attack_2", "animation.steve.shovel.attack_2")
        comp.AddPlayerAnimation("shovel_attack_3", "animation.steve.shovel.attack_3")
        
        comp.AddPlayerAnimationController("riot_shield_controller", "controller.animation.l4d2.riot_shield_controller")
        comp.AddPlayerAnimation("riot_shield_holding", "animation.steve.riot_shield.holding")
        comp.AddPlayerAnimation("riot_shield_pushing", "animation.steve.riot_shield.pushing")
        comp.AddPlayerAnimation("riot_shield_attack_1", "animation.steve.riot_shield.attack_1")
        comp.AddPlayerAnimation("riot_shield_attack_2", "animation.steve.riot_shield.attack_2")
        comp.AddPlayerAnimation("riot_shield_attack_3", "animation.steve.riot_shield.attack_3")
        
        comp.AddPlayerAnimationController("pitchfork_controller", "controller.animation.l4d2.pitchfork_controller")
        comp.AddPlayerAnimation("pitchfork_holding", "animation.steve.pitchfork.holding")
        comp.AddPlayerAnimation("pitchfork_pushing", "animation.steve.pitchfork.pushing")
        comp.AddPlayerAnimation("pitchfork_attack_1", "animation.steve.pitchfork.attack_1")
        comp.AddPlayerAnimation("pitchfork_attack_2", "animation.steve.pitchfork.attack_2")
        comp.AddPlayerAnimation("pitchfork_attack_3", "animation.steve.pitchfork.attack_3")

        comp.AddPlayerAnimationController("nightstick_controller", "controller.animation.l4d2.nightstick_controller")
        comp.AddPlayerAnimation("nightstick_holding", "animation.steve.nightstick.holding")
        comp.AddPlayerAnimation("nightstick_pushing", "animation.steve.nightstick.pushing")
        comp.AddPlayerAnimation("nightstick_attack_1", "animation.steve.nightstick.attack_1")
        comp.AddPlayerAnimation("nightstick_attack_2", "animation.steve.nightstick.attack_2")
        comp.AddPlayerAnimation("nightstick_attack_3", "animation.steve.nightstick.attack_3")
        
        comp.AddPlayerAnimationController("machete_controller", "controller.animation.l4d2.machete_controller")
        comp.AddPlayerAnimation("machete_holding", "animation.steve.machete.holding")
        comp.AddPlayerAnimation("machete_pushing", "animation.steve.machete.pushing")
        comp.AddPlayerAnimation("machete_attack_1", "animation.steve.machete.attack_1")
        comp.AddPlayerAnimation("machete_attack_2", "animation.steve.machete.attack_2")
        comp.AddPlayerAnimation("machete_attack_3", "animation.steve.machete.attack_3")
        
        comp.AddPlayerAnimationController("knife_controller", "controller.animation.l4d2.knife_controller")
        comp.AddPlayerAnimation("knife_holding", "animation.steve.knife.holding")
        comp.AddPlayerAnimation("knife_pushing", "animation.steve.knife.pushing")
        comp.AddPlayerAnimation("knife_attack_1", "animation.steve.knife.attack_1")
        comp.AddPlayerAnimation("knife_attack_2", "animation.steve.knife.attack_2")
        comp.AddPlayerAnimation("knife_attack_3", "animation.steve.knife.attack_3")
        
        comp.AddPlayerAnimationController("katana_controller", "controller.animation.l4d2.katana_controller")
        comp.AddPlayerAnimation("katana_holding", "animation.steve.katana.holding")
        comp.AddPlayerAnimation("katana_pushing", "animation.steve.katana.pushing")
        comp.AddPlayerAnimation("katana_attack_1", "animation.steve.katana.attack_1")
        comp.AddPlayerAnimation("katana_attack_2", "animation.steve.katana.attack_2")
        comp.AddPlayerAnimation("katana_attack_3", "animation.steve.katana.attack_3")
                
        # 添加高尔夫球杆动画
        comp.AddPlayerAnimationController("golf_club_controller", "controller.animation.l4d2.golf_club_controller")
        comp.AddPlayerAnimation("golf_club_holding", "animation.steve.golf_club.holding")
        comp.AddPlayerAnimation("golf_club_pushing", "animation.steve.golf_club.pushing")
        comp.AddPlayerAnimation("golf_club_attack_1", "animation.steve.golf_club.attack_1")
        comp.AddPlayerAnimation("golf_club_attack_2", "animation.steve.golf_club.attack_2")
        comp.AddPlayerAnimation("golf_club_attack_3", "animation.steve.golf_club.attack_3")
        
        # 添加平底锅动画
        comp.AddPlayerAnimationController("frying_pan_controller", "controller.animation.l4d2.frying_pan_controller")
        comp.AddPlayerAnimation("frying_pan_holding", "animation.steve.frying_pan.holding")
        comp.AddPlayerAnimation("frying_pan_pushing", "animation.steve.frying_pan.pushing")
        comp.AddPlayerAnimation("frying_pan_attack_1", "animation.steve.frying_pan.attack_1")
        comp.AddPlayerAnimation("frying_pan_attack_2", "animation.steve.frying_pan.attack_2")
        comp.AddPlayerAnimation("frying_pan_attack_3", "animation.steve.frying_pan.attack_3")
        
        # 添加消防斧动画
        comp.AddPlayerAnimationController("fireaxe_controller", "controller.animation.l4d2.fireaxe_controller")
        comp.AddPlayerAnimation("fireaxe_holding", "animation.steve.fireaxe.holding")
        comp.AddPlayerAnimation("fireaxe_pushing", "animation.steve.fireaxe.pushing")
        comp.AddPlayerAnimation("fireaxe_attack_1", "animation.steve.fireaxe.attack_1")
        comp.AddPlayerAnimation("fireaxe_attack_2", "animation.steve.fireaxe.attack_2")
        comp.AddPlayerAnimation("fireaxe_attack_3", "animation.steve.fireaxe.attack_3")
        
        # 添加电吉他动画
        comp.AddPlayerAnimationController("electric_guitar_controller", "controller.animation.l4d2.electric_guitar_controller")
        comp.AddPlayerAnimation("electric_guitar_holding", "animation.steve.electric_guitar.holding")
        comp.AddPlayerAnimation("electric_guitar_pushing", "animation.steve.electric_guitar.pushing")
        comp.AddPlayerAnimation("electric_guitar_attack_1", "animation.steve.electric_guitar.attack_1")
        comp.AddPlayerAnimation("electric_guitar_attack_2", "animation.steve.electric_guitar.attack_2")
        comp.AddPlayerAnimation("electric_guitar_attack_3", "animation.steve.electric_guitar.attack_3")
        
        # 添加铁撬动画
        comp.AddPlayerAnimationController("crowbar_controller", "controller.animation.l4d2.crowbar_controller")
        comp.AddPlayerAnimation("crowbar_holding", "animation.steve.crowbar.holding")
        comp.AddPlayerAnimation("crowbar_pushing", "animation.steve.crowbar.pushing")
        comp.AddPlayerAnimation("crowbar_attack_1", "animation.steve.crowbar.attack_1")
        comp.AddPlayerAnimation("crowbar_attack_2", "animation.steve.crowbar.attack_2")
        comp.AddPlayerAnimation("crowbar_attack_3", "animation.steve.crowbar.attack_3")
        
        # 添加板球棒动画
        comp.AddPlayerAnimationController("cricket_bat_controller", "controller.animation.l4d2.cricket_bat_controller")
        comp.AddPlayerAnimation("cricket_bat_holding", "animation.steve.cricket_bat.holding")
        comp.AddPlayerAnimation("cricket_bat_pushing", "animation.steve.cricket_bat.pushing")
        comp.AddPlayerAnimation("cricket_bat_attack_1", "animation.steve.cricket_bat.attack_1")
        comp.AddPlayerAnimation("cricket_bat_attack_2", "animation.steve.cricket_bat.attack_2")
        comp.AddPlayerAnimation("cricket_bat_attack_3", "animation.steve.cricket_bat.attack_3")
        
        # 添加电锯动画
        comp.AddPlayerAnimationController("chainsaw_controller", "controller.animation.l4d2.chainsaw_controller")
        comp.AddPlayerAnimation("chainsaw_idle", "animation.steve.chainsaw.idle")
        comp.AddPlayerAnimation("chainsaw_start", "animation.steve.chainsaw.start")
        comp.AddPlayerAnimation("chainsaw_holding", "animation.steve.chainsaw.holding")
        comp.AddPlayerAnimation("chainsaw_pushing", "animation.steve.chainsaw.pushing")
        comp.AddPlayerAnimation("chainsaw_attack_1", "animation.steve.chainsaw.attack_1")
        comp.AddPlayerAnimation("chainsaw_attack_2", "animation.steve.chainsaw.attack_2")
        comp.AddPlayerAnimation("chainsaw_attack_3", "animation.steve.chainsaw.attack_3")
        
        # 添加棒球棍动画
        comp.AddPlayerAnimationController("baseball_bat_controller", "controller.animation.l4d2.baseball_bat_controller")
        comp.AddPlayerAnimation("baseball_bat_holding", "animation.steve.baseball_bat.holding")
        comp.AddPlayerAnimation("baseball_bat_pushing", "animation.steve.baseball_bat.pushing")
        comp.AddPlayerAnimation("baseball_bat_attack_1", "animation.steve.baseball_bat.attack_1")
        comp.AddPlayerAnimation("baseball_bat_attack_2", "animation.steve.baseball_bat.attack_2")
        comp.AddPlayerAnimation("baseball_bat_attack_3", "animation.steve.baseball_bat.attack_3")

        comp.AddPlayerAnimationController("weapon_controller", "controller.animation.l4d2.weapon_controller")


        comp.AddPlayerRenderController('controller.render.l4d2_item', 'query.mod.l4d2_item > 0')

        comp.AddPlayerScriptAnimate("first_person_base", "v.is_first_person")
        comp.AddPlayerScriptAnimate("third_person_base", "!v.is_first_person")
        comp.AddPlayerScriptAnimate("weapon_controller", "(1.0)")

        # comp.SetPlayerItemInHandVisible(False, 0)
        comp.RebuildPlayerRender()


