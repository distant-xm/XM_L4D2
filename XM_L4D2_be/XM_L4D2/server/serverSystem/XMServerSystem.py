import mod.server.extraServerApi as serverApi
import math  # 添加math模块导入
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

levelId = serverApi.GetLevelId()


# 在modMain中注册的Server System类
class XMServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.sxunfu()

    #客户端传来的长按事件
    def sxunfu(self):
        self.ListenForEvent("XM_L4D2","XMClientSystem","Gun", self, self.Gun)
        self.ListenForEvent("XM_L4D2","XMClientSystem","RenderL4d2Player", self, self.RenderL4d2Player)
        self.ListenForEvent("XM_L4D2","XMClientSystem","RenderL4d2PlayerAnim", self, self.RenderL4d2PlayerAnim)
        # self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DimensionChangeFinishServerEvent",self, self.widu)
        



    # 处理客户端发送的右键事件（服务端）
    def RenderL4d2Player(self, args):
        playerId = args["playerId"]
        argsDict = self.CreateEventData()
        argsDict["playerId"] = playerId
        self.BroadcastToAllClient("RenderL4d2Player", argsDict)


    def RenderL4d2PlayerAnim(self, args):
        playerId = args["playerId"]
        state = args["state"]
        argsDict = self.CreateEventData()
        argsDict["playerId"] = playerId
        argsDict["state"] = state
        self.BroadcastToAllClient("RenderL4d2PlayerAnim", argsDict)



    # 处理客户端发送的右键事件（服务端）
    def Gun(self, args):
        playerId = args["playerId"]



        # 获取玩家位置和旋转组件
        posComp = serverApi.GetEngineCompFactory().CreatePos(playerId)
        rotComp = serverApi.GetEngineCompFactory().CreateRot(playerId)
        pos = posComp.GetPos()
        rot = rotComp.GetRot()
        
        # 发射参数配置
        power = 5
        gravity = 0
        
        # 扇形发射参数：7发，总角度40度
        total_angle = 75  # 总扩散角度
        bullet_count = 9  # 子弹数量
        start_angle = -total_angle / 2  # 起始角度
        
        # 获取完整方向向量（基于玩家完整旋转，包含俯仰角）
        forward_direction = serverApi.GetDirFromRot(rot)
        
        # 计算向上向量（通常为(0,1,0)）
        up_direction = (0, 1, 0)
        
        # 计算右侧向量（垂直于前进方向和上方向）
        # 叉积计算：forward × up 得到右侧向量
        right_x = forward_direction[1] * up_direction[2] - forward_direction[2] * up_direction[1]
        right_y = forward_direction[2] * up_direction[0] - forward_direction[0] * up_direction[2]
        right_z = forward_direction[0] * up_direction[1] - forward_direction[1] * up_direction[0]
        
        # 标准化右侧向量
        right_length = math.sqrt(right_x**2 + right_y**2 + right_z**2)
        if right_length > 0:
            right_direction = (right_x/right_length, right_y/right_length, right_z/right_length)
        else:
            # 如果forward和up平行（罕见情况），使用默认右侧方向
            right_direction = (1, 0, 0)
        
        # 计算扇形发射的方向向量
        for i in range(bullet_count):
            # 计算当前子弹相对于中心线的角度偏移（以度为单位）
            angle_offset = math.radians(start_angle + (total_angle / max(1, (bullet_count - 1))) * i)
            
            # 使用角度偏移在横向扇形面内计算新方向
            cos_a = math.cos(angle_offset)
            sin_a = math.sin(angle_offset)
            
            # 合成方向：主方向 + 横向偏移
            final_x = forward_direction[0] * cos_a + right_direction[0] * sin_a
            final_y = forward_direction[1] * cos_a + right_direction[1] * sin_a
            final_z = forward_direction[2] * cos_a + right_direction[2] * sin_a
            
            # 归一化最终方向向量
            length = math.sqrt(final_x**2 + final_y**2 + final_z**2)
            if length > 0:
                final_x /= length
                final_y /= length
                final_z /= length
            else:
                # 如果长度为0，使用原始方向
                final_x, final_y, final_z = forward_direction
            
            # 创建抛射物参数（保留原伤害值30，添加位置偏移+0.2）
            param = {
                'position': (pos[0], pos[1] + 0.0, pos[2]),  # 调整y轴位置，与原逻辑一致
                'direction': (final_x, final_y, final_z),
                'power': power,
                'gravity': gravity
            }
        
            # 创建弓箭抛射物
            projectile_comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
            projectile_comp.CreateProjectileEntity(playerId, "minecraft:snowball", param)

    # #读取结构
    # def widu(self, args):
    #     pass