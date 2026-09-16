from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
out=Path(__file__).resolve().parents[1]/'public'/'textures';out.mkdir(exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
mono='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def f(n,m=False):return ImageFont.truetype(mono if m else font,n)
im=Image.new('RGB',(1024,640),'#10151e');d=ImageDraw.Draw(im)
d.rectangle((0,0,1024,45),fill='#202733');d.text((25,12),'benish.py   ×',font=f(19),fill='#bac5d7');d.text((785,12),'WORKSPACE',font=f(16),fill='#8293ad')
d.rectangle((0,45,210,605),fill='#151c28');d.text((22,70),'EXPLORER',font=f(15),fill='#8192a9')
for i,t in enumerate(['⌄ portfolio','   src','   components','   benish.py','   projects.py','   README.md']):d.text((18,115+i*39),t,font=f(17),fill='#9baec7')
lines=[('# A little about me','#74869e'),('class Developer:','#c5a4e9'),('    name = "Benish M."','#a3c6fa'),('    focus = [','#a3c6fa'),('        "Python",','#b8d5b9'),('        "Odoo",','#b8d5b9'),('        "Frontend"','#b8d5b9'),('    ]','#a3c6fa'),('','#fff'),('    def build(self):','#c5a4e9'),('        return "Something useful."','#b8d5b9')]
for i,(t,c) in enumerate(lines):
 y=90+i*40;d.text((225,y),str(i+1),font=f(17,True),fill='#506075');d.text((275,y),t,font=f(22,True),fill=c)
d.rectangle((0,605,1024,640),fill='#283b58');d.text((20,614),'main  ✓     Python 3    •    Ready to build',font=f(15),fill='#c2d4ee');im.save(out/'code-screen.png')
im=Image.new('RGB',(1024,640),'#111514');d=ImageDraw.Draw(im)
d.rectangle((0,0,195,555),fill='#0c0f0e');d.ellipse((22,26,56,60),fill='#1ed760')
for j in range(3):d.arc((27,34+j*5,51,48+j*5),195,340,fill='#111',width=2)
d.text((65,31),'Spotify',font=f(23),fill='#f4f5f4')
for i,t in enumerate(['Home','Search','Your Library','','Made for you','Focus sessions','Late-night code']):d.text((24,100+44*i),t,font=f(17),fill='#a4aaa6')
for y in range(270):
 c=(int(41-y*.06),int(73-y*.11),int(59-y*.08));d.line((195,y,1024,y),fill=c)
d.text((234,31),'YOUR DAILY SOUNDTRACK',font=f(16),fill='#b5cbbd')
d.rounded_rectangle((238,91,445,298),radius=7,fill='#b8c8ae')
for k in range(7):d.arc((260+k*10,105+k*13,431-k*9,280-k*7),30,320,fill='#4c725e',width=5)
d.text((474,104),'PLAYLIST',font=f(14),fill='#c4d3c8');d.text((468,139),'Deep focus.',font=f(49),fill='white');d.text((474,216),'Less noise. More flow.',font=f(20),fill='#b7c7be');d.text((474,258),'Benish  •  Workspace mix',font=f(16),fill='#d1dad4')
d.ellipse((240,327,293,380),fill='#1ed760');d.polygon([(261,342),(261,366),(279,354)],fill='#0b2013')
for i,t in enumerate(['Quiet mornings','In the flow','After hours']):
 y=407+i*45;d.text((242,y),str(i+1),font=f(17),fill='#909a94');d.text((283,y),t,font=f(19),fill='#dde3df');d.text((914,y),'3:42',font=f(16),fill='#8e9b94')
d.rectangle((0,557,1024,640),fill='#1c231f');d.text((28,582),'Quiet mornings',font=f(18),fill='white');d.text((29,609),'Workspace mix',font=f(12),fill='#879b8e');d.rectangle((506,576,512,593),fill='white');d.rectangle((521,576,527,593),fill='white');d.line((328,615,742,615),fill='#4c5850',width=4);d.line((328,615,490,615),fill='#1ed760',width=4);im.save(out/'music-screen.png')
