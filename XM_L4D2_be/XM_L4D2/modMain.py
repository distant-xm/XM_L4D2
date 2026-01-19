from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

from XM_L4D2.modConfig import modConfig
#XM_L4D2 等于mod名称
@Mod.Binding(name = modConfig.ModName, version = modConfig.ModVersion)

class XM_L4D2(object):

    @Mod.InitServer()
    def XMServerSystem(self):
        # 函数可以将System注册到服务端引擎中，实例的创建和销毁交给引擎处理。第一个参数是MOD名称，第二个是System名称，第三个是自定义MOD System类的路径
        #注册mod名字，然后给服务端文件类的名字，然后读取这个类的文件路径（api文件--文件名--服务端文件名字）
        serverApi.RegisterSystem(modConfig.ModName, modConfig.ServerSystemName, modConfig.ServerSystemClsPath)
        print("XMServerSystem Init")

    @Mod.InitClient()
    def XMClientSystem(self):
        # 函数可以将System注册到客户端引擎中，实例的创建和销毁交给引擎处理。第一个参数是MOD名称，第二个是System名称，第三个是自定义MOD System类的路径
        #注册mod名字，然后给刻度换文件类的名字，然后读取这个类的文件路径（api文件--文件名--客户端文件名字）
        clientApi.RegisterSystem(modConfig.ModName, modConfig.ClientSystemName, modConfig.ClientSystemClsPath)
        print("XMClientSystem Init")
    
    @Mod.DestroyServer()
    def XMServerDestroy(self):
        print("DestroyServer")

        
    @Mod.DestroyClient()
    def XMClientDestroy(self):
        print("DestroyClient")