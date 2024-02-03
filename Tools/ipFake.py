import random
from fake_useragent import UserAgent

def createIP():
	ip = ".".join(str(random.randrange(257)) for _ in range(4))
	return ip
	
def random_ipFake():
	with open('fake_ip.txt','r') as ip:
		list_ip = [line.strip() for line in ip.readlines()]
		for _ in range(10):
			list_ip.append(createIP())
		#print(list_ip)
		ip_random = random.choice(list_ip)
		return ip_random
		
# -----------

def UserAgentFake():
	ugf_create = UserAgent()
	ugf = ugf_create.random
	return ugf
	

#print(createIP());print(random_ipFake());print(UserAgentFake())
