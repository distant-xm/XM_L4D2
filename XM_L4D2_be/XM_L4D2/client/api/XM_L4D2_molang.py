import mod.client.extraClientApi as clientApi
compFactory = clientApi.GetEngineCompFactory()

playerId = clientApi.GetLocalPlayerId()
levelId = clientApi.GetLevelId()

import random

from XM_L4D2.config.WeaponConfig import WeaponConfig


class XM_L4D2_molang:  # 类名规范：首字母大写
    def __init__(self):
        self.weapon_detail = WeaponConfig
        
        self.timer_ids = []    # 存储定时器ID列表

#1111111111111111111111111111111111111111111
    def SetMolang(self, playerId):
        comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
        carriedData = comp.GetCarriedItem()
        newItemName = carriedData["newItemName"]
        
        # 当手持物品为骨头时触发箭矢发射逻辑
        if newItemName in self.weapon_detail:
            # 构建事件数据，包含服务器创建箭矢所需的所有参数
            attack_value = random.randint(1, 3)
            # 使用新方法设置攻击值并在0.3秒后重置为0
            self.set_attack_with_reset(playerId, attack_value, 0.3)

    
    # 设置攻击值并在指定时间后重置为0的方法
    def set_attack_with_reset(self, playerId, attack_value, delay=0.3):
        # 设置攻击值
        self.molang(playerId, "l4d2_attack", float(attack_value))
        # 创建一个定时器，在delay秒后将攻击值重置为0
        def reset_attack():
            self.molang(playerId, "l4d2_attack", 0.0)
        # 启动定时器并保存ID以便后续管理
        comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
        timer_id = comp.AddTimer(delay, reset_attack)
        
        # 确保timer_ids属性存在
        if not hasattr(self, 'timer_ids'):
            self.timer_ids = []
        self.timer_ids.append(timer_id)

    
    def molang(self, playerId,weapon_query_name,weapon_query_value):
        mcomp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
        xx = mcomp.Set("query.mod."+weapon_query_name, weapon_query_value)
        print(xx,weapon_query_name,weapon_query_value)
#11111111111111111111111111111111111




#222222222222222222222222222222222222222
    def Set_amolang(self, playerId):
        pass

#222222222222222222222222222222222222222


#333333333333333333333333333333333333333
    def Set_amolang(self, playerId):
        pass

#333333333333333333333333333333333333333

