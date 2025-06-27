import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# --- 중력렌즈 파라미터 ---

theta\_E = 1.0  # 아인슈타인 반경
image\_size = 300  # 출력 이미지 크기

# 배경천체(별) 밝기 분포 생성

x = np.linspace(-2, 2, image\_size)
y = np.linspace(-2, 2, image\_size)
X, Y = np.meshgrid(x, y)
source = np.exp(- (X**2 + Y**2) / 0.02)  # 가우시안 분포별

# 렌즈 맵핑 함수

def lens\_mapping(xi, yi, lens\_x, lens\_y, theta\_E=theta\_E):
dx = xi - lens\_x
dy = yi - lens\_y
r2 = dx**2 + dy**2
\# 단순 점질량 렌즈 방정식
beta\_x = xi - theta\_E**2 \* dx / np.maximum(r2, 1e-6)
beta\_y = yi - theta\_E**2 \* dy / np.maximum(r2, 1e-6)
return beta\_x, beta\_y

# 시뮬레이션 함수

def compute\_lensed\_image(lens\_x):
lens\_y = 0
xi, yi = np.meshgrid(x, y)
bx, by = lens\_mapping(xi, yi, lens\_x, lens\_y)
\# 배열 인덱스로 변환
ix = ((bx - x.min()) / x.ptp() \* (image\_size - 1)).astype(int)
iy = ((by - y.min()) / y.ptp() \* (image\_size - 1)).astype(int)
\# 범위 클리핑
ix = np.clip(ix, 0, image\_size - 1)
iy = np.clip(iy, 0, image\_size - 1)
return source\[iy, ix]

@st.cache
def compute\_lightcurve(positions):
brightness = \[]
for pos in positions:
img = compute\_lensed\_image(pos)
brightness.append(img.sum())
return np.array(brightness)

# Streamlit UI 설정

st.title("인터랙티브 중력렌즈 시뮬레이션")

lens\_range = np.linspace(-1.5, 1.5, 200)
lens\_pos = st.slider("렌즈 위치 (x)", float(lens\_range.min()), float(lens\_range.max()), 0.0, step=0.01)

# 렌즈 왜곡 이미지 표시

lensed = compute\_lensed\_image(lens\_pos)
fig, ax = plt.subplots()
ax.imshow(lensed, origin="lower", norm=LogNorm(), extent=\[x.min(), x.max(), y.min(), y.max()])
ax.set\_title(f"렌즈 위치: x = {lens\_pos:.2f}")
ax.axis("off")
st.pyplot(fig)

# 전체 광도 곡선 표시 옵션

if st.checkbox("전체 광도 곡선 보기"):
curve = compute\_lightcurve(lens\_range)
st.line\_chart({"Brightness": curve}, x=lens\_range)

st.markdown("---")
st.markdown(
"이 시뮬레이션은 단순 점질량 렌즈 모델로, 슬라이더로 렌즈 위치를 조절하며 실시간으로 광원 이미지 왜곡 및 광도 변화를 관측할 수 있습니다."
)
