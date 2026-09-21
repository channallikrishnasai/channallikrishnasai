"""Small deterministic raster motion loops for the README."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]

def font(size: int, mono: bool = False):
    name = "C:/Windows/Fonts/consola.ttf" if mono else "C:/Windows/Fonts/segoeuib.ttf"
    return ImageFont.truetype(name, size)

def hero_loop() -> None:
    source = Image.open(ROOT / "assets/generated/nexus-hero.png").convert("RGB")
    frames=[]
    for index in range(14):
        zoom=1.00+index*.012
        crop_w,crop_h=int(source.width/zoom),int(source.height/zoom)
        left=(source.width-crop_w)//2; top=(source.height-crop_h)//2
        frame=source.crop((left,top,left+crop_w,top+crop_h)).resize((720,405),Image.Resampling.LANCZOS)
        frames.append(frame.quantize(colors=128,method=Image.Quantize.MEDIANCUT))
    path=ROOT/"assets/generated/nexus-hero.gif"
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=130,loop=0,optimize=True,disposal=2)

def terminal_loop() -> None:
    lines=[("$ whoami","Krishna Sai Channalli"),("$ focus","AI Systems · Agent Engineering · Automation"),("$ current_system","OPERO"),("$ status","ONLINE")]
    frames=[]
    for step in range(22):
        image=Image.new("RGB",(900,360),(5,10,17)); draw=ImageDraw.Draw(image)
        draw.rounded_rectangle((28,24,872,336),16,fill=(5,15,26),outline=(36,162,195),width=2)
        draw.text((62,54),"KRISHNA.SAI // TERMINAL",font=font(18,True),fill=(101,232,255))
        y=100; remaining=step
        for command,result in lines:
            command_count=len(command)//2+2; result_count=len(result)//3+2
            if remaining>0:
                visible=command[:min(len(command),remaining*2)]
                draw.text((62,y),visible,font=font(17,True),fill=(112,238,255)); remaining-=command_count
            if remaining>=0 and step>command_count:
                visible=result[:max(0,min(len(result),remaining*3))]
                draw.text((62,y+26),visible,font=font(15),fill=(220,247,255)); remaining-=result_count
            y+=57
        if step%4<3: draw.rectangle((62,min(y,307),73,min(y,307)+17),fill=(130,246,255))
        frames.append(image.quantize(colors=128,method=Image.Quantize.MEDIANCUT))
    path=ROOT/"assets/terminal/nexus-terminal.gif"
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=[80]*20+[700,700],loop=0,optimize=True,disposal=2)

def generate() -> None:
    hero_loop(); terminal_loop()

if __name__ == "__main__": generate()
