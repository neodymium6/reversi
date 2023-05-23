
import time
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_image_coordinates import streamlit_image_coordinates
import osero_lib
import load_model
from PIL import Image, ImageDraw 

if "turn" not in st.session_state:
    st.session_state.turn = 1

if "ban" not in st.session_state:
    st.session_state.ban=[
                            0,0,0,0,0,0,0,0,
                            0,0,0,0,0,0,0,0,
                            0,0,0,0,0,0,0,0,
                            0,0,0,2,1,0,0,0,
                            0,0,0,1,2,0,0,0,
                            0,0,0,0,0,0,0,0,
                            0,0,0,0,0,0,0,0,
                            0,0,0,0,0,0,0,0
                        ]

if "dpi" not in st.session_state:
    st.session_state.dpi = 100
if "frame" not in st.session_state:
    st.session_state.frame = 0
st.session_state.frame+=1

def Centerize(x1,y1,x2,y2,magnif):
    width=x2-x1
    height=y2-y1
    x1_n=x1+(1-magnif)*width/2
    x2_n=x2-(1-magnif)*width/2
    y1_n=y1+(1-magnif)*height/2
    y2_n=y2-(1-magnif)*height/2
    return x1_n,y1_n,x2_n,y2_n


#st component

st.header("オセロ")
if st.button(label="大きく"):
    st.session_state.dpi+=5
    st.experimental_rerun()
if st.button(label="小さく"):
    st.session_state.dpi-=5
    st.experimental_rerun()


def DrawBan(ban,draw):
    pixel_x=st.session_state.dpi/100
    for i in range(64):
        x=i%8
        y=i//8
        if ban[i]==1:
            draw.ellipse(Centerize(16+x*42,16+y*42,16+(x+1)*42,16+(y+1)*42,0.7),fill=(0,0,0))
        if ban[i]==2:
            draw.ellipse(Centerize(16+x*42,16+y*42,16+(x+1)*42,16+(y+1)*42,0.7),fill=(255,255,255))



im=Image.open("img.jpeg")
draw=ImageDraw.Draw(im)

#draw ban
DrawBan(st.session_state.ban,draw)

im=im.resize((
    384*st.session_state.dpi//100,
    384*st.session_state.dpi//100)
    )

#拡大
value = streamlit_image_coordinates(im)

#GAMEEND
can_put_flag=False
for i in range(64):
    can_put_flag=can_put_flag or osero_lib.CanPut(st.session_state.ban,i,st.session_state.turn)
    can_put_flag=can_put_flag or osero_lib.CanPut(st.session_state.ban,i,3-st.session_state.turn)
if not can_put_flag:
    st.text("GAMEEND")
    black_num=0
    white_num=0
    for i in range(64):
        if st.session_state.ban[i]==1:
            black_num+=1
        elif st.session_state.ban[i]==2:
            white_num+=1
    st.text("黒は"+str(black_num)+"枚、白は"+str(white_num)+"枚")
else:
    #PASS
    can_put_flag=False
    for i in range(64):
        can_put_flag=can_put_flag or osero_lib.CanPut(st.session_state.ban,i,st.session_state.turn)
    if not can_put_flag:
        #st.warning(str(st.session_state.turn)+"はパスです")
        if st.session_state.turn==1:
            st.warning("黒はパスです")
        else:
            st.warning("白はパスです")
        st.session_state.turn=3-st.session_state.turn
        if st.session_state.turn==2:
            time.sleep(0.5)

    #COMPUT
    if st.session_state.turn==2:
        pos=load_model.Predict(st.session_state.ban)
        st.session_state.ban[pos]=st.session_state.turn
        osero_lib.Reverse(st.session_state.ban,pos,st.session_state.turn)
        st.session_state.turn=3-st.session_state.turn
        time.sleep(0.1)
        st.experimental_rerun()

        # put first pos putable
        for i in range(64):
            if osero_lib.CanPut(st.session_state.ban,i,st.session_state.turn):
                st.session_state.ban[i]=st.session_state.turn
                osero_lib.Reverse(st.session_state.ban,i,st.session_state.turn)
                st.session_state.turn=3-st.session_state.turn
                time.sleep(0.5)
                st.experimental_rerun()


    if value is not None:
        pixel_x=st.session_state.dpi/100
        if 16<=(value["x"]/pixel_x)<352 and 16<=(value["y"]/pixel_x)<352:
            pos=int((value["x"]/pixel_x-16)//(42)+((value["y"]/pixel_x-16)//(42))*8)
            #st.session_state.ban[0]=1
            if osero_lib.CanPut(st.session_state.ban,pos,st.session_state.turn):
                st.session_state.ban[pos]=st.session_state.turn
                osero_lib.Reverse(st.session_state.ban,pos,st.session_state.turn)
                st.session_state.turn=3-st.session_state.turn
                st.experimental_rerun()
            else:
                st.markdown(":red[置けません！]")

    
#/Users/noharadaisuke/free/program/python/tensorflow_osero/env/bin/python -m streamlit run streamlit/app.py
