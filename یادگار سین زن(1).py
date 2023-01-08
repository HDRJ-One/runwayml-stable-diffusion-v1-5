import os
try:
	import pyfiglet
except:
	os.system("pip install pyfiglet")
	print("نصب شد!")
	print("_"*40)
	os.system("clear")
try:
	from re import findall
except:
	os.system("pip install re")
	print("نصب شد!")
	print("_"*40)
	os.system("clear")
try:
	from random import choice
except:
	os.system("pip install random")
	print("نصب شد!")
	print("_"*40)
	os.system("clear")
try:
	import time
except:
	os.system("pip install time")
	print("نصب شد!")
	print("_"*40)
	os.system("clear")
try:
	from libraryArsein.Arsein import Robot_Rubika
except:
	os.system("pip install libraryArsein")
	print("نصب شد!")
	print("_"*40)
	os.system("clear")
	os.system("pip install pycryptodome")
	print("نصب شد!")
	print("_"*40)
	os.system("clear")


import os
import time
import pyfiglet
import datetime
from re import findall
from random import choice
from libraryArsein.Arsein import Robot_Rubika
os.system("clear")

red = '\033[31m' 
green = '\033[32m' 
blue = '\033[36m' 
pink = '\033[35m' 
yellow = '\033[93m' 
darkblue = '\033[34m' 
white = '\033[00m'
print('\033[31m'+pyfiglet.figlet_format("  YASIN BOT",font='slant')+ "\n "+'\033[34m'+"_"*67+white)

auths=["kjiaetasnbtymzhtfafleuyfbupuipyp"]
your_Group_Link="https://rubika.ir/joing/DEJJIFBC0FSBJRECVQJJQKBBNTJWYSPF"


for i in auths:
	Robot_Rubika(i).joinGroup(your_Group_Link)
	try:
		channelGuid=bot.getInfoByUsername("my_channel_2221")['data']['channel']['channel_guid']
		Robot_Rubika(i).joinChannelByID(channelGuid)
	except:pass

bot = Robot_Rubika(choice(auths))
Group_Guid=bot.joinGroup(your_Group_Link)["data"]["group"]["group_guid"]

alarm=10
TImeeSleep=5
errFor=0
forMsg=0
answered=[]
stop_finish=[]


Linkdooni_Guid = ["c0BTXy05d5dbf4aa17e8c92e7e260973","c0Btyq095a83abe72ecf41080c6f1c35","c0Ee8O06d4d835c994ab8a51ea0e4880","c0Ee9X09008b057804dadf8f941e305a","c0HGkO0951a2f9159b86470742c0b5d0","c0MTeU0f77bd1c780b8b7509797bfd68","c0HGkO0951a2f9159b86470742c0b5d0","c0RSKL05e95414cec64d48b54f2e943e"]

bot.sendMessage(Group_Guid,"""سین زن 𝚈𝚊𝚜𝚒𝚗 𝙱𝚘𝚝 با موفقیت فعال شد🌚
برای دریافت راهنما کلمه (help) را ارسال کنید!""")
while 1:
	try:
		min_id = bot.getGroupInfo(Group_Guid)["data"]["chat"]["last_message_id"]
		
		
		while 1:
			try:
				messages = bot.getMessages(Group_Guid,min_id)
				break
			except:
				continue

		for msg in messages:
			if msg['type'] == 'Text' :
					if msg.get('message_id') not in answered:
						answered.append(msg.get("message_id"))
						if msg.get("text").startswith("seen") :
								teedad_seen=msg.get("text").replace("seen ","")
								try:
									for i in bot.getMessagesInfo(Group_Guid, [msg.get("reply_to_message_id")]):
										if i.get("message_id")==msg.get("reply_to_message_id"):
											Bener__id=i['forwarded_from']['message_id']
											Baner_Guid=i['forwarded_from']['object_guid']
											for banner in bot.getMessagesInfo(Baner_Guid, [Bener__id]):
												if banner['message_id']==Bener__id:
													if int(teedad_seen) > int(banner['count_seen']) :
														teedad_seen1=teedad_seen
														azab=int(teedad_seen) - int(banner['count_seen'])
														bot.sendMessage(Group_Guid,f"درخواست شما تایید شد!\n تغداد سین باقی مانده = {azab}",message_id=msg.get("message_id"))
														start_time = datetime.datetime.now()
														bot.sendMessage(Group_Guid,f"درحال دریافت لینک گروه!",message_id=msg.get("message_id"))
														if int(teedad_seen) > int(banner['count_seen']):
															open("Group_Link.txt","w").write("Yasin_Bot")
															tedad_link=0
															for Linkdooni___Guid in Linkdooni_Guid:
																try:
																	File=open("Group_Link.txt","a")
																	bot.joinChannel(Linkdooni___Guid)
																	Channel_Message_Id = bot.getChannelInfo(Linkdooni___Guid)["data"]["chat"]["last_message_id"]
																	for Channel_Message in bot.getMessages(Linkdooni___Guid,Channel_Message_Id) :
																		for Group_Link in findall(r"https://rubika.ir/joing/\w{32}", Channel_Message.get("text")):
																			tedad_link+=1
																			File.write("\n"+Group_Link)
																except:pass
																		
														bot.sendMessage(Group_Guid,f"تعداد لینک های دریافت شده={tedad_link}",message_id=msg.get("message_id"))
													bot.sendMessage(Group_Guid,f"سین زدن شروع شد!!!")
													ajibe=0
													while True:
														
														if int(teedad_seen) < int(banner['count_seen']):
															bot.sendMessage(Group_Guid,f"""‼️سین زدن به پایان رسید!!!
❕تعداد فوروارد : {forMsg}
❕تعداد گروه های بسته : {errFor}""",message_id=msg.get("message_id"))
															break
														try:
															for banner in bot.getMessagesInfo(Baner_Guid, [Bener__id]):
																if banner['message_id']==Bener__id:
																	if int(teedad_seen) > int(banner['count_seen']):
																			try:
																			
																				link=choice(open("Group_Link.txt","r").read().split("\n"))
																				Namad=bot.joinGroup(link)["data"]['chat_update']
																				if "SendMessages" in Namad["chat"]['access']:
																					ajibe+=1
																					if int(ajibe)==int(alarm):
																						ajibe=0
																						aaal=int(teedad_seen1) - int(banner['count_seen'])
																						bot.sendMessage(Group_Guid,f"""کاربر گرامی
پست شما به {alarm} گروه ارسال شد!🌚
تعداد سین فعلی بنر شما:{banner['count_seen']}
تعداد سین باقی مانده: {aaal}""",message_id=msg.get("message_id"))
																						bot = Robot_Rubika(choice(auths))
																					Join_Guid=Namad['object_guid']
																					bot.forwardMessages(Baner_Guid,[Bener__id],Join_Guid)
																					bot.leaveGroup(Join_Guid)
																					forMsg+=1
																					time.sleep(int(TImeeSleep))
																				else:
																					bot.leaveGroup(Join_Guid)
																					errFor+=1
																			except:pass
														except:pass

								except:pass
						elif msg.get("text").startswith("ادیت اعلان") :
							try:
								adite_eelane=msg.get("text").replace("ادیت اعلان ","")
								if int(adite_eelane) != int(alarm) and int(adite_eelane) > 0:
									bot.sendMessage(Group_Guid,f"""❕درخاست شما با موفقیت انجام شد

اعلان از {alarm} به {adite_eelane} تغییر کرد""",message_id=msg.get("message_id"))
									alarm=int(adite_eelane)
								else:
									if int(adite_eelane) > 0:
										bot.sendMessage(Group_Guid,f"""کاربر گرامی
سقف اعلان از قبل {alarm} بود❗️""",message_id=msg.get("message_id"))
									else:
										bot.sendMessage(Group_Guid,f"""❗️کاربر گرامی اعلان نمیتوان صفر و یا منفی باشد!
لطفا یک عدد از 0 بیشتر انتخاب کنید!""",message_id=msg.get("message_id"))
							except:
								bot.sendMessage(Group_Guid,f"خطا در تغییر سقف اعلان!",message_id=msg.get("message_id"))
						elif msg.get("text").startswith("help") :
							try:
								bot.sendMessage(Group_Guid,f"""دستورات 💢

به بخش دستورات بات خش آمدید!

❗️برای شروع سین زنی رویه بنر خود ریپلای کنید  و کلمه seen را بفرستید

برای تعداد سین جلویه کلمه seen یک عدد بزارید!(از تعداد سین فعلی بنر بیشتر باشه)

برای مثال:

seen 100
بات سین زنی زو شروع میکنه

هروقت تمون شد میگه سین زدن به پایان رسید!

❗️بات در حالت عادی وقتی یه پیام رو به ده تا گروه فوروارد کنه اطلاع میده

میتونید با دستور ادیت اعلان سقفشو تغییر بدید

مثال:

ادیت اعلان 50

از این به بعد وقتی ربات بنر شمارو به 50
 گروه فوروارد کنه بهتون اطلاع میده

❗️ ادیت تایم
این دستور برای اینکه فاصله بین دوتا فوروارد رو تغییر بدی(time sleep)
برای مثال:
ادیت تایم 5
از این به بعد هر پنج ثانیه فوروارد میکنه🌚
(درحالت عادی این تایم رویه 4 ثانیس)

𝙿𝚛𝚘𝚐𝚛𝚊𝚖𝚖𝚎𝚛 : @yasin_2216""",message_id=msg.get("message_id"))
							except:pass
						elif msg.get("text").startswith("ادیت تایم") :
							try:
								adite_TImeeSleep=msg.get("text").replace("ادیت تایم ","")
								TImeeSleep=int(adite_TImeeSleep)
								bot.sendMessage(Group_Guid,f"تایم با موفقیت به {adite_TImeeSleep} تغییر یافت \n از این به بعد هر {adite_TImeeSleep} ثانیه یک فوروارد انجام میشود",message_id=msg.get("message_id"))
							except:
								bot.sendMessage(Group_Guid,f"خطا در تغییر تایم",message_id=msg.get("message_id"))
	except:pass