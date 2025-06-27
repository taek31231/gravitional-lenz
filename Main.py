import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# 중력렌즈 파라미터 설정

theta\_E = 1.0  # 아인슈타인 반경
image\_size = 300  # 출력 이미지 크기

# 배경광원 분포 생성 (가우시안 별)

x = np.linspace(-2, 2, image\_size)
y = np.linspace(-2, 2, image\_size)
X, Y = np.meshgrid(x, y)
source = np.exp(- (X**2 + Y**2) / 0.02)

# 렌즈 매핑 함수 정의

def lens\_mapping(xi, yi, lens\_x, lens\_y, theta\_E=theta\_E):
dx = xi - lens\_x
dy = yi - lens\_y
r2 = dx**2 + dy**2
beta\_x = xi - theta\_E**2 \* dx / np.maximum(r2, 1e-6)
beta\_y = yi - theta\_E**2 \* dy / np.maximum(r2, 1e-6)
return beta\_x, beta\_y

# 렌즈 이미지 계산 함수

def compute\_lensed\_image(lens\_x):
lens\_y = 0.0
xi, yi = np.meshgrid(x, y)
bx, by = lens\_mapping(xi, yi, lens\_x, lens\_y)
ix = ((bx - x.min()) / x.ptp() \* (image\_size - 1)).astype(int)
iy = ((by - y.min()) / y.ptp() \* (image\_size - 1)).astype(int)
ix = np.clip(ix, 0, image\_size - 1)
iy = np.clip(iy, 0, image\_size - 1)
return source\[iy, ix]

# 광도(light curve) 계산 함수

def compute\_lightcurve(positions):
brightness = \[]
for pos in positions:
img = compute\_lensed\_image(pos)
brightness.append(np.sum(img))
return np.array(brightness)

# Streamlit 인터페이스 구축

st.title("인터랙티브 중력렌즈 시뮬레이션")

# 렌즈 위치 슬라이더 설정

lens\_positions = np.linspace(-1.5, 1.5, 200)
lens\_x = st.slider("렌즈 위치 (x 좌표)", float(lens\_positions.min()), float(lens\_positions.max()), 0.0, step=0.01)

# 렌즈 왜곡 이미지 표시

lensed\_img = compute\_lensed\_image(lens\_x)
fig, ax = plt.subplots()
ax.imshow(lensed\_img, origin="lower", norm=LogNorm(), extent=\[x.min(), x.max(), y.min(), y.max()])
ax.set\_title(f"렌즈 위치: x = {lens\_x:.2f}")
ax.axis("off")
st.pyplot(fig)

# 광도 곡선 표시 옵션\ if st.checkbox("전체 광도 곡선 표시"):

```
curve = compute_lightcurve(lens_positions)
st.line_chart(curve, use_container_width=True)
```

# 설명 추가

st.markdown("---")
st.markdown(
"이 시뮬레이션은 단순한 점질량 렌즈 모델을 사용하며, 슬라이더로 렌즈 위치를 조절하면서 광원 이미지 왜곡과 광도 변화를 관측할 수 있습니다."
)
