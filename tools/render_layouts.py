"""Render original schematic scrapbook wireframes. Requires Pillow; no photo inputs.

Usage: python tools/render_layouts.py --font /path/to/CJK-font.ttf
"""
from pathlib import Path
import argparse
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
S = 2
W, H = 900, 1200
PAPER, INK, MUTED = '#f1ebdf', '#33342f', '#7f847f'
GRAY, EDGE, OCHRE = '#d8ddd9', '#c2c8c3', '#bb9756'
TITLES = ['情绪主图＋片段浮贴', '日常碎片拼贴', '周末小报', '小型时间轴', '主题中心＋周边细节', '主角抠图＋照片卡']
DESCS = ['小图跨接无框主图 · 图间标题与细旁白', '照片与局部底板 · 大小、形状、材料变化', '报头与分栏 · 图组、抠图和细线分区', '弯曲路径串节点 · 日期、说明有层级', '偏心主题主体 · 周边细节与局部小字', '人物轮廓跨照片 · 场景、物件各有角色']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, required=True)
    args = parser.parse_args()

    @lru_cache(None)
    def font(size):
        return ImageFont.truetype(str(args.font), int(size*S))

    class Page:
        def __init__(self):
            self.im = Image.new('RGB', (W*S, H*S), PAPER)
            self.d = ImageDraw.Draw(self.im)

        def line(self, points, color=INK, width=1):
            self.d.line([(int(x*S), int(y*S)) for x,y in points], fill=color, width=max(1,int(width*S)), joint='curve')

        def text(self, x, y, text, size=22, color=INK, align='left'):
            for i, line in enumerate(text.split('\n')):
                self.d.text((int(x*S), int((y+i*size*1.42)*S)), line, font=font(size), fill=color, anchor={'left':'lt','center':'mt','right':'rt'}[align])

        def rect(self, xy, fill, outline=None, radius=0, width=1):
            box=tuple(int(v*S) for v in xy)
            self.d.rounded_rectangle(box, radius=int(radius*S), fill=fill, outline=outline, width=max(1,int(width*S)))

        def photo(self, x, y, w, h, label, angle=0, border=8, caption=None):
            # Independent pristine schematic, no source image editing.
            t=Image.new('RGBA',(int(w*S),int(h*S)), '#fffdf7' if border else GRAY)
            d=ImageDraw.Draw(t); b=border*S
            d.rectangle((b,b,w*S-b-1,h*S-b-1),fill=GRAY,outline=EDGE,width=S)
            # Small image glyph and clear source/role label.
            cx,cy=w*S/2,h*S*.42
            d.ellipse((cx-18*S,cy-36*S,cx-5*S,cy-23*S),outline=MUTED,width=S)
            d.line([(cx-28*S,cy+1*S),(cx-8*S,cy-15*S),(cx+4*S,cy-3*S),(cx+16*S,cy-12*S),(cx+30*S,cy+1*S)],fill=MUTED,width=S)
            for i,tx in enumerate(label.split('\n')):
                d.text((cx,cy+17*S+i*27*S),tx,font=font(21),fill='#68726d',anchor='mt')
            if caption:
                d.text((w*S/2,(h-27)*S),caption,font=font(17),fill=INK,anchor='mt')
            if angle:
                t=t.rotate(angle,Image.Resampling.BICUBIC,expand=True)
            # Rotation is around the card's center.
            xx=int((x+w/2)*S-t.width/2); yy=int((y+h/2)*S-t.height/2)
            self.im.paste(t,(xx,yy),t)

        def stars(self, x,y,scale=1):
            for dx,dy,r in [(0,0,13),(24,20,7)]:
                self.line([(x+dx,y+dy-r*scale),(x+dx+5*scale,y+dy),(x+dx,y+dy+r*scale),(x+dx-5*scale,y+dy),(x+dx,y+dy-r*scale)],width=1.3)

        def arrow(self,x,y,dx,dy):
            self.line([(x,y),(x+dx*.2,y+dy*.65),(x+dx*.6,y+dy*.9),(x+dx,y+dy)],width=1.2)
            a=math.atan2(dy,dx)
            self.line([(x+dx-9*math.cos(a-.5),y+dy-9*math.sin(a-.5)),(x+dx,y+dy),(x+dx-9*math.cos(a+.5),y+dy-9*math.sin(a+.5))],width=1.2)

        def cloud(self,x,y,w,h,text):
            pts=[]
            for i in range(181):
                a=i*2*math.pi/180
                ripple=1+.055*math.cos(12*a)
                pts.append((x+w/2+math.cos(a)*w/2*ripple,y+h/2+math.sin(a)*h/2*ripple))
            self.d.polygon([(int(a*S),int(b*S)) for a,b in pts],fill='#f7f3e9')
            self.line(pts,width=1.35)
            lines=text.split('\n'); yy=y+h/2-len(lines)*24*1.42/2
            self.text(x+w/2,yy,text,24,align='center')

        def bag(self,x,y,s=1):
            self.rect((x,y+12*s,x+39*s,y+55*s),None,INK,7*s)
            self.line([(x+10*s,y+12*s),(x+12*s,y+2*s),(x+26*s,y+2*s),(x+29*s,y+12*s)],width=1.1)
            self.rect((x+7*s,y+31*s,x+32*s,y+45*s),None,INK,3*s)

        def person(self,x,y,w,h,label):
            cx=x+w/2
            self.d.ellipse((int((cx-w*.16)*S),int(y*S),int((cx+w*.16)*S),int((y+h*.21)*S)), fill='#e0e3df',outline=MUTED,width=S)
            pts=[(cx-w*.18,y+h*.24),(x+w*.08,y+h*.34),(x,y+h*.66),(x+w*.14,y+h*.69),(x+w*.22,y+h*.49),(x+w*.2,y+h*.82),(cx-w*.15,y+h*.82),(cx-w*.16,y+h),(cx-w*.02,y+h),(cx,y+h*.83),(cx+w*.06,y+h),(cx+w*.2,y+h),(cx+w*.15,y+h*.82),(x+w*.8,y+h*.82),(x+w*.78,y+h*.49),(x+w*.86,y+h*.69),(x+w,y+h*.66),(x+w*.92,y+h*.34),(cx+w*.18,y+h*.24)]
            self.d.polygon([(int(a*S),int(b*S)) for a,b in pts],fill='#e0e3df')
            self.line(pts+[pts[0]],MUTED)
            self.text(cx,y+h*.46,label,22,align='center')

        def save(self,p):
            self.im.resize((W,H),Image.Resampling.LANCZOS).save(p)

    out=ROOT/'assets/layouts';out.mkdir(parents=True,exist_ok=True)
    pages=[]
    # A: a real bridge and unframed hero, not an equal card wall.
    p=Page();p.photo(0,720,900,480,'P1 · 情绪主图\n完整场景 / 无框',border=0)
    p.photo(65,110,325,260,'P2 · 片段',angle=4,caption='图旁主要短句')
    p.text(455,72,'日常的小记',37);p.text(489,130,'随手记两句',24);p.bag(742,117,.65)
    p.photo(463,240,350,245,'P3 · 场景',angle=-3)
    p.text(520,497,'就近的一句批注',25);p.text(81,408,'小段补充字\n自然断行，不必等长',18)
    p.photo(88,535,172,190,'P5 · 细节',angle=2,border=0)
    p.photo(365,599,340,245,'P4 · 过渡图',angle=-5,caption='跨接上下的片段')
    p.stars(94,489,.8);p.text(739,589,'次级旁白\n在空隙里',18)
    p.cloud(585,1065,260,90,'主图边的小旁白\n轻线条气泡')
    pages.append(p)
    # B: varied fragments + one backing; circle crop and source-object silhouette.
    p=Page();p.text(65,72,'生活碎片',41);p.text(68,132,'几件小事，凑成一页',21)
    p.photo(66,215,290,350,'P1 · 竖场景',angle=3,border=0)
    p.photo(452,150,352,230,'P2 · 横片段',angle=-4)
    p.text(470,398,'一句图注',26);p.text(83,581,'片段旁的小字\n不占一整列',18)
    p.rect((360,514,825,990),'#ded2bc',INK,22)
    p.photo(401,548,275,238,'P3 · 同组内容',angle=-3)
    p.d.ellipse((int(608*S),int(788*S),int(802*S),int(982*S)), fill=GRAY,outline=EDGE,width=S)
    p.text(705,848,'P4\n圆形细节',20,align='center');p.text(402,822,'一组内容\n放在一起',23)
    p.text(395,1009,'底板只组织这一组',18)
    p.bag(129,804,2.6);p.text(180,976,'P5 · 物件抠图',20,align='center');p.stars(296,725)
    p.text(70,1100,'有些地方不加图案，留一点空白。',21)
    pages.append(p)
    # C: a small newspaper with genuine column hierarchy.
    p=Page();p.rect((55,62,845,1135),'#fcfbf6')
    p.text(98,100,'WEEKEND\n小小记录',14);p.text(450,91,'周末小报',47,align='center');p.text(786,112,'栏目示意\n不编日期',15,align='right')
    p.line([(95,180),(806,180)],width=1.8)
    p.photo(99,225,195,230,'P1',border=0);p.photo(313,225,195,230,'P2',border=0)
    p.text(550,226,'活动这一栏',27);p.text(550,279,'正文按图组组织\n长短随内容变化\n留出列与列的间隔',19)
    p.person(600,393,125,200,'P3')
    p.text(98,481,'图组的一句说明',22);p.stars(770,403,.7)
    p.line([(93,630),(805,604)],width=1.8)
    p.text(102,669,'餐食 / 第二组',28)
    p.photo(100,730,329,260,'P4 · 场景',border=0)
    p.photo(509,700,260,210,'P5 · 照片',border=0)
    p.d.ellipse((int(510*S),int(935*S),int(738*S),int(1070*S)),fill=GRAY,outline=MUTED,width=S)
    p.text(624,978,'P6 · 物件轮廓',18,align='center')
    p.text(101,1017,'这组内容的短批注',22);p.text(107,1061,'补充小字放在自己的栏目里',17)
    pages.append(p)
    # D: flexible curved time path with non-uniform nodes.
    p=Page();p.text(76,65,'把几个瞬间串起来',41,color='#a36c69');p.text(79,130,'只使用用户确认的先后或日期',19)
    path=[(424,215),(454,350),(410,500),(467,682),(422,870),(458,1065)]
    smooth=[]
    for j in range(len(path)-1):
        a,b,c,e=path[max(0,j-1)],path[j],path[j+1],path[min(len(path)-1,j+2)]
        for k in range(21):
            t=k/20
            smooth.append(tuple(.5*((2*b[z])+(-a[z]+c[z])*t+(2*a[z]-5*b[z]+4*c[z]-e[z])*t*t+(-a[z]+3*b[z]-3*c[z]+e[z])*t*t*t) for z in (0,1)))
    p.line(smooth,'#bc8985',5)
    nodes=[(70,215,280,174,'P1',3),(519,322,296,219,'P2',-3),(66,588,285,180,'P3',1),(522,772,270,179,'P4',-5),(99,941,259,153,'P5',3)]
    labels=[(381,255,'节点一'),(471,383,'节点二'),(374,630,'节点三'),(463,835,'节点四'),(378,1005,'节点五')]
    for (x,y,w,h,lab,a),(tx,ty,seq) in zip(nodes,labels):
        p.rect((x-13,y-12,x+w+13,y+h+58),'#e0c1ba',radius=25)
        p.photo(x,y,w,h,lab,angle=a,border=5)
        p.text(x+6,y+h+17,'较小的节点说明',18)
        p.text(tx,ty,seq,22,color='#986664')
    p.stars(748,624,.9);p.text(570,1114,'路径会转弯，图也有疏密',20)
    pages.append(p)
    # E: off-center object protagonist, not another human-photo-card page.
    p=Page();p.text(84,68,'围绕一个主题',40);p.text(88,132,'先看主体，再看细节',21)
    p.photo(70,235,270,205,'P2 · 相关场景',angle=3)
    p.photo(568,191,220,278,'P3 · 局部',angle=-4,border=0)
    p.text(82,469,'一段主要记录',25);p.text(90,516,'小字补充材料或动作\n跟着内容走',18)
    p.rect((268,599,590,875),GRAY,MUTED,20)
    p.d.arc((int(529*S),int(641*S),int(689*S),int(820*S)),270,90,fill=MUTED,width=3*S)
    p.text(429,690,'P1 · 主题主体\n物件 / 宠物等轮廓',24,align='center')
    p.photo(65,924,282,182,'P4 · 细节',angle=-3)
    p.photo(608,885,194,223,'P5 · 细节',angle=4)
    p.arrow(309,565,49,66);p.arrow(624,517,-30,92)
    p.stars(725,672,.8);p.text(674,723,'关键词',28);p.text(676,773,'局部补充',18)
    p.text(382,1030,'主体偏心\n周边不均分',21)
    pages.append(p)
    # F: one expressive human silhouette bridging scenes + a small actual-object slot.
    p=Page();p.text(82,69,'成长的一小页',39);p.text(88,132,'标题嵌在图与轮廓之间',20)
    p.photo(72,235,346,250,'P2 · 场景',angle=4)
    p.text(91,511,'照片边的主要短句',25)
    p.photo(83,636,460,218,'P3 · 动作',angle=-4,border=0)
    p.text(101,883,'补充小字\n可以写得更轻一点',18)
    p.photo(545,165,234,184,'P4 · 小片段',angle=-3)
    p.person(468,417,330,626,'P1\n人物抠图')
    p.text(573,1116,'轮廓跨过图组边缘',18)
    p.bag(159,994,1.8);p.text(263,1024,'P5\n物件小抠图',19)
    p.cloud(573,346,223,83,'一小句旁白');p.stars(422,563,.8)
    pages.append(p)

    for i,p in enumerate(pages):
        p.save(out/f'{chr(97+i)}.png')
    # Overview is a technical contact sheet of the newly drawn schematics.
    ov=Image.new('RGB',(1920,2070),'#faf8f2');d=ImageDraw.Draw(ov)
    def ot(x,y,text,size,color=INK):
        f=ImageFont.truetype(str(args.font),size)
        d.text((x,y),text,font=f,fill=color,anchor='lt')
    ot(55,40,'手账式 Plog · 六套新版白模',43)
    ot(58,102,'看结构、字号层级与局部巧思；照片均为占位，不含真实人物',22,MUTED)
    for i in range(6):
        x=55+(i%3)*625;y=170+(i//3)*880
        ot(x,y,f'{chr(65+i)}  {TITLES[i]}',25)
        img=Image.open(out/f'{chr(97+i)}.png').resize((570,760),Image.Resampling.LANCZOS)
        ov.paste(img,(x,y+49))
        ot(x,y+827,DESCS[i],17,MUTED)
    ot(58,1962,'浅灰块＝照片 / 白模轮廓＝抠图；字句只说明层级，实际内容随用户素材调整。',23)
    ot(58,2010,'A—F 沿用技能库编号，与参考六联图的字母不同；不按占位坐标机械套版。',21,MUTED)
    ov.save(out/'overview.png')
    print(f'Rendered six pages and overview in {out}')


if __name__ == '__main__':
    main()
