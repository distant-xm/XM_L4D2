import mod.server.extraServerApi as serverApi
import math  # 添加math模块导入
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

levelId = serverApi.GetLevelId()


# 在modMain中注册的Server System类
class XMServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        print("xmxmxm init")
        self.sxunfu()


    #客户端传来的长按事件
    def sxunfu(self):
        self.ListenForEvent("XM_L4D2","XMClientSystem","RightClickBeforeClientEvent", self, self.Gun)
        self.ListenForEvent("XM_L4D2","XMClientSystem","xm_l4d2:select_player", self, self.RenderL4d2Player)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DimensionChangeFinishServerEvent",self, self.widu)


    # 处理客户端发送的右键事件（服务端）
    def RenderL4d2Player(self, args):
        playerId = args["playerId"]
        argsDict = self.CreateEventData()
        argsDict["playerId"] = playerId
        self.BroadcastToAllClient("RenderL4d2Player", argsDict)


    # 处理客户端发送的右键事件（服务端）
    def Gun(self, args):
        playerId = args["playerId"]
        
        print("11111111111111")
        # 获取玩家位置和旋转组件
        posComp = serverApi.GetEngineCompFactory().CreatePos(playerId)
        rotComp = serverApi.GetEngineCompFactory().CreateRot(playerId)
        pos = posComp.GetPos()
        rot = rotComp.GetRot()
        
        # 发射参数配置
        power = 1
        gravity = 0
        
        # 扇形发射参数：9发，总角度80度（-40到+40度）
        total_angle = 80  # 总扩散角度
        bullet_count = 9  # 子弹数量
        start_angle = -total_angle / 2  # 起始角度
        
        for i in range(bullet_count):
            # 计算当前子弹的角度偏移
            angle_offset = start_angle + (total_angle / (bullet_count - 1)) * i
            
            # 复制原始旋转并修改yaw角度（假设rot是(pitch, yaw, roll)元组）
            pitch = rot[0] if len(rot) > 0 else 0
            yaw = rot[1] if len(rot) > 1 else 0
            roll = rot[2] if len(rot) > 2 else 0
            new_rot = (pitch, yaw + angle_offset, roll)
            
            # 根据新旋转计算三维方向向量
            direct = serverApi.GetDirFromRot(new_rot)
            
            # 创建抛射物参数（保留原伤害值30，添加位置偏移+0.2）
            param = {
                'position': (pos[0], pos[1] + 0.2, pos[2]),  # 调整y轴位置，与原逻辑一致
                'direction': direct,      # 三维方向向量
                'power': power,           # 发射力量
                'gravity': gravity,       # 重力因子
                'damage': 30              # 保留原伤害值
            }
            
            # 创建弓箭抛射物
            projectile_comp = serverApi.GetEngineCompFactory().CreateProjectile(playerId)
            projectile_comp.CreateProjectileEntity(playerId, "minecraft:arrow", param)

    #读取结构
    def widu(self, args):
        pass