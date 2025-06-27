import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# --- 중력렌즈 파라미터 ---
theta_E = 1.0  # 아인슈타인 반경
image_size = 300  # 출력 이미지 크기

# 배경천체(별) 밝기 분포 생성
x = np.linspace(-2, 2, image_size)
y = np.linspace(-2, 2, image_size)
X, Y = np.meshgrid(x, y)
source = np.exp(- (X**2 + Y**2) / 0.02)  # 가우시안 분포별

# 렌즈 맵핑 함수
def lens_mapping(xi, yi, lens_x, lens_y, theta_E=theta_E):
    dx = xi - lens_x
    dy = yi - lens_y
    r2 = dx**2 + dy**2
n    # 단순 점질량 렌즈 방정식
    beta_x = xi - theta_E**2 * dx / np.maximum(r2, 1e-6)
    beta_y = yi - theta_E**2 * dy / np.maximum(r2, 1e-6)
    return beta_x, beta_y

# 시뮬레이션 함수
def compute_lensed_image(lens_x):
    # 렌즈 위치 (lens_x, 0)
    lens_y = 0
    xi, yi = np.meshgrid(x, y)
    bx, by = lens_mapping(xi, yi, lens_x, lens_y)
    # 좌표를 배열 인덱스로
    ix = ((bx - x.min()) / (x.ptp()) * (image_size - 1)).astype(int)
    iy = ((by - y.min()) / (y.ptp()) * (image_size - 1)).astype(int)
    # 범위 클리핑
    ix = np.clip(ix, 0, image_size-1)
    iy = np.clip(iy, 0, image_size-1)
    # 렌즈 왜곡된 이미지
    return source[iy, ix]

# 광도(light curve) 계산
@st.cache
def compute_lightcurve(positions):
    brightness = []
    for pos in positions:
        img = compute_lensed_image(pos)
        brightness.append(img.sum())
    return np.array(brightness)

# Streamlit UI 설정
st.title("인터랙티브 중력렌즈 시뮬레이션")

# 행성(렌즈)이 움직일 x 위치 선택 슬라이더
lens_range = np.linspace(-1.5, 1.5, 200)
lens_pos = st.slider("렌즈 위치 (x)", float(lens_range.min()), float(lens_range.max()), 0.0, step=0.01)

# 왜곡 이미지 계산 및 표시
lensed = compute_lensed_image(lens_pos)
fig, ax = plt.subplots()
ax.imshow(lensed, origin='lower', norm=LogNorm(), extent=[x.min(), x.max(), y.min(), y.max()])
ax.set_title(f"렌즈 위치: x = {lens_pos:.2f}")
ax.axis('off')
st.pyplot(fig)

# 전체 위치 범위에 대한 광도 곡선 계산 및 표시
if st.checkbox("전체 광도 곡선 보기"):
    curve = compute_lightcurve(lens_range)
    st.line_chart({"Brightness": curve}, x=lens_range)

st.markdown("---")
st.markdown(
    "이 시뮬레이션은 단순 점질량 렌즈 모델로, 슬라이더로 렌즈 위치를 조절하며 실시간으로 광원 이미지 왜곡 및 광도 변화를 관측할 수 있습니다."
)
