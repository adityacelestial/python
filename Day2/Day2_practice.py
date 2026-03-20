# • Create a User class with private attributes and getter/setter methods 
# • Implement inheritance with AdminUser and CustomerUser classes 
# • Implement method overriding for display_profile() 
# • Build a composition-based Order class that contains Address and PaymentInfo

class User:
    def setusername(self,username):
        self.__username=username
    
    def setuserage(self,age):
        self.__age=age
    
    def getname(self):
        print(self.__username)
    def getage(self):
        print(self.__age)

sampleuser=User()

sampleuser.setusername("Aditya")
sampleuser.setuserage(22)

sampleuser.getname()
sampleuser.getage()
