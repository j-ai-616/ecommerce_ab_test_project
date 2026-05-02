"""
Streamlit dashboard for the E-commerce A/B Test Techbook project.

Run:
    python -m streamlit run app/streamlit_app.py

v3 UI goals:
- White main page background.
- Cleaner card-based UX with better readability.
- More beginner-friendly explanation of why A/B testing matters in e-commerce.
- Every chart/table includes a reading guide and interpretation.
- Does not load raw data directly.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st


# ============================================================
# 1. Path Setting
# ============================================================

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from utils import (  # noqa: E402
    get_chart_dir,
    load_dashboard_tables,
    read_project_table,
)


# ============================================================
# 2. Page Config & CSS
# ============================================================

st.set_page_config(
    page_title="E-commerce A/B Test Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#E94B22"
PRIMARY_DARK = "#C73D19"
YELLOW = "#FAC000"
TEXT = "#202632"
MUTED = "#667085"
SOFT = "#FFF3EE"
SOFT_YELLOW = "#FFF9DB"
LINE = "#F1D8CF"

CUSTOM_CSS = f"""
<style>
    .stApp {{
        background-color: #FFFFFF;
    }}

    .block-container {{
        max-width: 1120px;
        padding-top: 3.2rem;
        padding-bottom: 4rem;
    }}

    h1 {{
        color: {TEXT};
        font-size: 2.35rem !important;
        letter-spacing: -0.045em;
        margin-bottom: 0.7rem;
    }}

    h2 {{
        color: {TEXT};
        letter-spacing: -0.035em;
        margin-top: 2.2rem;
        margin-bottom: 0.9rem;
    }}

    h3 {{
        color: {TEXT};
        letter-spacing: -0.025em;
    }}

    p, li, div {{
        line-height: 1.7;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF7F3 100%);
        border-right: 1px solid {LINE};
    }}

    section[data-testid="stSidebar"] * {{
        font-size: 0.94rem;
    }}

    div[data-testid="stMetric"] {{
        background-color: #FFFFFF;
        border: 1px solid {LINE};
        padding: 18px 18px 14px 18px;
        border-radius: 18px;
        box-shadow: 0 5px 18px rgba(31, 41, 51, 0.035);
    }}

    div[data-testid="stMetricValue"] {{
        color: {PRIMARY};
        font-weight: 800;
    }}

    .hero-card {{
        background: linear-gradient(135deg, {PRIMARY} 0%, #FF6A3A 100%);
        color: white;
        padding: 34px 36px;
        border-radius: 26px;
        box-shadow: 0 14px 34px rgba(233, 75, 34, 0.20);
        margin-bottom: 26px;
    }}

    .hero-card h1 {{
        color: white;
        margin-bottom: 10px;
        font-size: 2.25rem !important;
    }}

    .hero-card p {{
        color: #FFF4EE;
        font-size: 1.07rem;
        margin-bottom: 0;
        max-width: 880px;
    }}

    .tag {{
        display: inline-block;
        background-color: {YELLOW};
        color: #271800;
        padding: 5px 11px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 0.8rem;
        margin-right: 6px;
        margin-bottom: 12px;
    }}

    .concept-card {{
        background-color: #FFFFFF;
        border: 1px solid {LINE};
        border-radius: 20px;
        padding: 22px 24px;
        box-shadow: 0 7px 22px rgba(31, 41, 51, 0.04);
        min-height: 180px;
        margin-bottom: 16px;
    }}

    .concept-title {{
        font-size: 1.08rem;
        font-weight: 850;
        color: {TEXT};
        margin-bottom: 8px;
    }}

    .concept-body {{
        color: #344054;
        font-size: 0.98rem;
    }}

    .simple-box {{
        background-color: #FFFFFF;
        border: 1px solid {LINE};
        border-radius: 20px;
        padding: 22px 24px;
        box-shadow: 0 7px 22px rgba(31, 41, 51, 0.035);
        margin-bottom: 18px;
    }}

    .story-box {{
        background-color: {SOFT};
        border: 1px solid #FFD9CB;
        border-radius: 20px;
        padding: 22px 24px;
        margin: 16px 0 24px 0;
    }}

    .story-title {{
        font-weight: 850;
        color: {PRIMARY_DARK};
        margin-bottom: 8px;
        font-size: 1.05rem;
    }}

    .read-box {{
        border-left: 5px solid {YELLOW};
        background-color: {SOFT_YELLOW};
        padding: 14px 18px;
        border-radius: 13px;
        margin: 12px 0 14px 0;
        color: {TEXT};
        font-size: 0.96rem;
    }}

    .insight-box {{
        border-left: 6px solid {PRIMARY};
        background-color: {SOFT};
        padding: 16px 18px;
        border-radius: 14px;
        margin: 12px 0 26px 0;
        color: {TEXT};
        font-size: 0.98rem;
    }}

    .muted {{
        color: {MUTED};
        font-size: 0.92rem;
    }}

    .orange {{
        color: {PRIMARY};
        font-weight: 850;
    }}

    .step-number {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 999px;
        background: {PRIMARY};
        color: white;
        font-weight: 900;
        margin-right: 8px;
    }}

    .stDataFrame {{
        border: 1px solid #F0F2F5;
        border-radius: 14px;
    }}

    hr {{
        margin-top: 2rem;
        margin-bottom: 2rem;
    }}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# 3. Cached Loaders
# ============================================================

@st.cache_data(show_spinner=False)
def load_tables_cached() -> dict[str, pd.DataFrame]:
    return load_dashboard_tables(PROJECT_ROOT)


@st.cache_data(show_spinner=False)
def load_table_cached(filename: str, required: bool = False) -> pd.DataFrame:
    return read_project_table(filename, project_root=PROJECT_ROOT, required=required)


@st.cache_data(show_spinner=False)
def load_chart_paths_cached() -> dict[str, Path]:
    chart_dir = get_chart_dir(PROJECT_ROOT)
    if not chart_dir.exists():
        return {}
    return {path.stem: path for path in sorted(chart_dir.glob("*.png"))}


tables = load_tables_cached()
charts = load_chart_paths_cached()


# ============================================================
# 4. Helpers
# ============================================================

def is_empty(df: Optional[pd.DataFrame]) -> bool:
    return df is None or df.empty


def show_dataframe(df: pd.DataFrame, *, height: int = 300) -> None:
    if is_empty(df):
        st.info("표시할 데이터가 없습니다. 관련 노트북 실행 결과 CSV를 확인해 주세요.")
    else:
        st.dataframe(df, height=height, use_container_width=True, hide_index=True)


def show_table_with_guide(
    title: str,
    df: pd.DataFrame,
    guide: str,
    interpretation: str,
    *,
    height: int = 300,
) -> None:
    st.subheader(title)
    st.markdown(f"<div class='read-box'><b>읽는 방법</b><br>{guide}</div>", unsafe_allow_html=True)
    show_dataframe(df, height=height)
    st.markdown(f"<div class='insight-box'><b>해석</b><br>{interpretation}</div>", unsafe_allow_html=True)


def show_chart_with_guide(
    title: str,
    chart_stem: str,
    guide: str,
    interpretation: str,
) -> None:
    st.subheader(title)
    path = charts.get(chart_stem)
    if path and path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"차트 파일을 찾을 수 없습니다: `{chart_stem}.png`")
    st.markdown(f"<div class='read-box'><b>읽는 방법</b><br>{guide}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight-box'><b>해석</b><br>{interpretation}</div>", unsafe_allow_html=True)


def get_conversion_rate(step: str) -> Optional[float]:
    df = tables.get("conversion_summary", pd.DataFrame())
    if is_empty(df) or "conversion_step" not in df.columns:
        return None
    row = df.loc[df["conversion_step"] == step]
    if row.empty:
        return None
    return float(row["conversion_rate"].iloc[0])


def fmt_rate(value: Optional[float]) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value * 100:.2f}%"


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <span class="tag">E-commerce</span>
            <span class="tag">A/B Test</span>
            <span class="tag">Conversion Optimization</span>
            <h1>A/B Test 기반 이커머스 전환율 개선 프로젝트</h1>
            <p>
            “어떤 화면이 더 잘 팔리게 만드는가?”라는 질문을 데이터로 검증하기 위해,
            이커머스 행동 로그를 분석하고 A/B Test 설계까지 연결한 프로젝트입니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_strip() -> None:
    view_to_cart = get_conversion_rate("View → Add to Cart")
    cart_to_purchase = get_conversion_rate("Add to Cart → Purchase")
    view_to_purchase = get_conversion_rate("View → Purchase")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("상품조회 → 장바구니", fmt_rate(view_to_cart), help="Primary metric")
    with c2:
        st.metric("장바구니 → 구매", fmt_rate(cart_to_purchase), help="Secondary metric")
    with c3:
        st.metric("상품조회 → 구매", fmt_rate(view_to_purchase), help="Guardrail / business metric")


def candidate_category_fallback() -> pd.DataFrame:
    candidate = tables.get("optimization_categories", pd.DataFrame())
    if is_empty(candidate):
        return pd.DataFrame()

    cols = [
        col for col in [
            "categoryid",
            "view_users",
            "cart_users",
            "purchase_users",
            "view_to_cart_rate",
            "view_to_purchase_rate",
            "items_in_category",
        ]
        if col in candidate.columns
    ]

    return candidate[cols].copy()


def render_business_action_summary() -> None:
    """Render a clear top-level business action plan summary."""
    view_to_cart = get_conversion_rate("View → Add to Cart")
    view_to_purchase = get_conversion_rate("View → Purchase")

    opt = tables.get("optimization_categories", pd.DataFrame())
    exp = tables.get("expansion_categories", pd.DataFrame())

    opt_category_text = "고트래픽 저전환 카테고리"
    if not is_empty(opt) and "categoryid" in opt.columns:
        top_opt = opt.iloc[0]
        opt_category_text = f"Category {int(top_opt['categoryid'])}"
        if "view_users" in opt.columns and "view_to_purchase_rate" in opt.columns:
            opt_category_text += f" · view users {int(top_opt['view_users']):,}명 · purchase CVR {top_opt['view_to_purchase_rate'] * 100:.2f}%"

    exp_category_text = "저트래픽 고전환 카테고리"
    if not is_empty(exp) and "categoryid" in exp.columns:
        top_exp = exp.iloc[0]
        exp_category_text = f"Category {int(top_exp['categoryid'])}"
        if "view_users" in exp.columns and "view_to_purchase_rate" in exp.columns:
            exp_category_text += f" · view users {int(top_exp['view_users']):,}명 · purchase CVR {top_exp['view_to_purchase_rate'] * 100:.2f}%"

    st.markdown("## 최종 비즈니스 액션 플랜")

    st.markdown(
        f"""
        <div class="story-box">
            <div class="story-title">핵심 제안</div>
            이 프로젝트의 최종 제안은 <b>“고트래픽 저전환 상품·카테고리를 대상으로
            상품 상세페이지와 장바구니 진입 경험을 A/B Test로 개선하자”</b>입니다.  
            현재 가장 큰 병목은 상품을 본 뒤 장바구니에 담기 전 단계이며,
            <b>View → Add to Cart 전환율은 {fmt_rate(view_to_cart)}</b>입니다.
            따라서 첫 번째 실험은 결제 화면보다 <b>상품 상세페이지, CTA 버튼, 혜택 메시지,
            리뷰·신뢰 정보, 추천 영역</b>을 우선 대상으로 삼는 것이 합리적입니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="concept-card">
                <div class="concept-title">Action 1. 전환 병목 먼저 개선</div>
                <div class="concept-body">
                <b>대상</b>: 고트래픽 저전환 상품·카테고리<br>
                <b>실험</b>: CTA 문구·위치, 혜택 메시지, 리뷰/배송/반품 정보 강화<br>
                <b>근거</b>: View → Add to Cart 전환율이 {fmt_rate(view_to_cart)}로 가장 낮은 병목 구간입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="concept-card">
                <div class="concept-title">Action 2. 잘 팔리는 숨은 영역 노출 확대</div>
                <div class="concept-body">
                <b>대상</b>: 저트래픽 고전환 카테고리<br>
                <b>실험</b>: 추천 슬롯, 검색 결과, 프로모션 배너 노출 확대<br>
                <b>근거</b>: 전환율은 높지만 노출이 적은 영역은 추가 트래픽을 받을 때 성과가 커질 수 있습니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="concept-card">
                <div class="concept-title">Action 3. 구매 전환율을 함께 감시</div>
                <div class="concept-body">
                <b>Primary</b>: View → Add to Cart<br>
                <b>Guardrail</b>: View → Purchase ({fmt_rate(view_to_purchase)})<br>
                <b>근거</b>: 장바구니 클릭만 늘고 구매가 줄면 좋은 실험이 아니므로 최종 구매 지표를 함께 봐야 합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="read-box">
            <b>우선 실험 후보 예시</b><br>
            <b>Optimization 후보</b>: {opt_category_text}<br>
            <b>Expansion 후보</b>: {exp_category_text}<br><br>
            Optimization 후보는 “사람들이 이미 많이 보지만 잘 사지 않는 영역”입니다.
            Expansion 후보는 “사람들이 많이 보지는 않지만 본 사람은 잘 사는 영역”입니다.
            두 영역은 서로 다른 액션이 필요합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_page_key_message(
    title: str,
    core_message: str,
    why_it_matters: str,
    next_action: str,
) -> None:
    """Render a clear top-of-page key message block."""
    st.markdown(
        f"""
        <div class="story-box">
            <div class="story-title">{title}</div>
            <b>핵심 메시지</b><br>
            {core_message}<br><br>
            <b>왜 중요한가</b><br>
            {why_it_matters}<br><br>
            <b>다음 액션</b><br>
            {next_action}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_beginner_story() -> None:
    st.markdown("## 왜 이커머스에서 A/B Test가 중요할까?")

    st.markdown(
        """
        <div class="story-box">
            <div class="story-title">쉬운 예시</div>
            온라인 쇼핑몰에서 같은 상품을 팔고 있다고 생각해 봅니다.  
            A 화면은 버튼 문구가 <b>“장바구니”</b>이고, B 화면은 <b>“지금 담고 혜택 확인하기”</b>입니다.  
            둘 중 어떤 화면이 더 많은 사람을 장바구니로 움직이게 할까요?  
            느낌으로 결정하면 위험합니다. 그래서 사용자를 두 그룹으로 나누어 실제 행동 데이터를 비교합니다.  
            이것이 A/B Test입니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">1. 작은 차이가 큰 매출 차이</div>
                <div class="concept-body">
                버튼 위치, 문구, 추천 상품 배치처럼 작아 보이는 차이도
                방문자가 수십만 명이면 큰 전환 차이로 이어질 수 있습니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">2. 감이 아니라 실험으로 판단</div>
                <div class="concept-body">
                “이 디자인이 더 예뻐 보여요”가 아니라
                실제로 더 많은 사용자가 장바구니와 구매로 이동했는지를 봅니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">3. 실패 비용을 줄임</div>
                <div class="concept-body">
                전체 사이트를 바꾸기 전에 일부 사용자에게만 실험해 보면
                나쁜 변경을 전체 고객에게 적용하는 위험을 줄일 수 있습니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_abtest_concepts() -> None:
    st.markdown("## 이 프로젝트를 이해하기 위한 핵심 개념 지도")

    st.markdown(
        """
        <div class="story-box">
            <div class="story-title">먼저 큰 흐름부터 보기</div>
            이 프로젝트는 A/B Test 하나만 다루는 것이 아닙니다.  
            <b>사용자 행동 로그</b>를 읽고, <b>전환 퍼널</b>에서 병목을 찾고,
            <b>상품·카테고리별 기회 영역</b>을 구분한 뒤,
            마지막으로 <b>A/B Test 설계</b>와 <b>비즈니스 실행안</b>까지 연결합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">1. Event Log</div>
                <div class="concept-body">
                사용자가 남긴 행동 기록입니다.  
                이 데이터에서는 <b>view</b>, <b>addtocart</b>, <b>transaction</b>이 핵심 이벤트입니다.
                즉 “상품을 봤다 → 장바구니에 담았다 → 구매했다”의 흔적입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">2. Funnel</div>
                <div class="concept-body">
                퍼널은 사용자가 목표 행동까지 가는 단계입니다.  
                이 프로젝트의 퍼널은 <b>View → Add to Cart → Purchase</b>입니다.
                어느 단계에서 사람이 많이 빠져나가는지 찾는 것이 첫 번째 목표입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">3. Conversion</div>
                <div class="concept-body">
                Conversion은 사용자가 원하는 다음 행동으로 넘어가는 것입니다.  
                예를 들어 상품을 본 사람이 장바구니에 담으면
                <b>View → Add to Cart 전환</b>이 일어난 것입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">4. Conversion Rate</div>
                <div class="concept-body">
                전환율은 “대상자 중 몇 %가 다음 행동을 했는가”입니다.  
                예: 상품을 본 100명 중 3명이 장바구니에 담으면 전환율은 3%입니다.
                본 프로젝트의 핵심 전환율은 <b>View → Add to Cart</b>입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">5. Bottleneck</div>
                <div class="concept-body">
                병목은 사용자가 많이 이탈하는 구간입니다.  
                데이터상 가장 큰 병목은 상품을 본 뒤 장바구니에 담기 전 단계입니다.
                그래서 상품 상세페이지와 CTA 개선이 중요해집니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">6. Opportunity Matrix</div>
                <div class="concept-body">
                상품·카테고리를 <b>조회량</b>과 <b>전환율</b> 기준으로 나누는 방법입니다.  
                조회는 많은데 전환이 낮은 영역은 개선 대상,
                조회는 적지만 전환이 높은 영역은 노출 확대 대상입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">7. A/B Test</div>
                <div class="concept-body">
                사용자를 두 그룹으로 나누어 기존안과 개선안을 비교하는 실험입니다.  
                이 프로젝트에서는 “개선된 상품 화면이 장바구니 전환율을 높이는가?”를 검증하는 상황을 설계합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">8. Primary / Guardrail Metric</div>
                <div class="concept-body">
                Primary metric은 실험 성공 판단 기준입니다. 여기서는 <b>View → Add to Cart</b>입니다.  
                Guardrail metric은 부작용 감시 지표입니다. 여기서는 <b>View → Purchase</b>입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="concept-card">
                <div class="concept-title">9. Uplift & Sample Size</div>
                <div class="concept-body">
                Uplift는 개선안이 기존안보다 얼마나 좋아졌는지입니다.  
                Sample size는 그 차이가 우연이 아닌지 확인하기 위해 필요한 사용자 수입니다.
                작은 차이를 검증하려면 더 많은 사용자가 필요합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("## 이 프로젝트에서 사용한 분석·통계 기법")

    methods = pd.DataFrame(
        [
            ["Raw Data Audit", "원본 데이터의 행 수, 기간, 결측치, 컬럼 구조를 점검합니다.", "분석 결과를 믿을 수 있는지 확인하기 위해 필요합니다."],
            ["Funnel Analysis", "View → Add to Cart → Purchase 단계별 사용자 수와 전환율을 계산합니다.", "어디서 사용자가 가장 많이 이탈하는지 찾습니다."],
            ["Item & Category Analysis", "상품과 카테고리별 조회, 장바구니, 구매 성과를 비교합니다.", "개선할 영역과 노출을 늘릴 영역을 구분합니다."],
            ["Opportunity Matrix", "조회량과 전환율을 기준으로 Star, Optimization, Expansion, Long-tail을 나눕니다.", "실험 우선순위를 정할 수 있습니다."],
            ["Sample Size Estimation", "목표 uplift를 검증하려면 몇 명의 사용자가 필요한지 계산합니다.", "너무 작은 실험으로 잘못된 결론을 내리는 것을 막습니다."],
            ["Two-Proportion Z-Test", "Control과 Treatment의 전환율 차이가 통계적으로 의미 있는지 검정합니다.", "개선안이 우연히 좋아 보이는 것인지 판단합니다."],
            ["Monte Carlo Simulation", "가상의 실험을 여러 번 반복해 p-value와 lift의 변동성을 봅니다.", "실험 결과가 확률적으로 흔들릴 수 있음을 이해합니다."],
            ["Business Impact Simulation", "전환율 개선이 실제 추가 장바구니 사용자 수로 얼마나 이어지는지 계산합니다.", "통계 결과를 비즈니스 가치로 바꿉니다."],
        ],
        columns=["Technique", "What it does", "Why it matters"],
    )

    show_table_with_guide(
        "Analysis & Statistical Methods",
        methods,
        "각 행은 이 프로젝트에서 사용한 분석 또는 통계 기법과 그 역할을 설명합니다.",
        "이 프로젝트의 강점은 하나의 기법만 사용한 것이 아니라, 데이터 점검부터 실험 설계와 비즈니스 의사결정까지 이어지는 전체 흐름을 구성했다는 점입니다.",
        height=360,
    )


# ============================================================
# 5. Sidebar
# ============================================================

with st.sidebar:
    st.markdown("## 🛒 E-commerce A/B Test")
    st.caption("A/B Test 기반 이커머스 전환율 개선 프로젝트 기술서")

    page = st.radio(
        "Dashboard Pages",
        [
            "Project Guide",
            "Executive Summary",
            "Funnel Analysis",
            "Item & Category Insights",
            "A/B Test Simulation",
            "Business Action Plan",
            "Data & Repository Notes",
        ],
    )

    st.divider()
    st.markdown("### Project Flow")
    st.markdown(
        """
        1. Raw Data Audit  
        2. Funnel Analysis  
        3. Item & Category Analysis  
        4. A/B Test Simulation  
        5. Business Recommendation
        """
    )

    st.divider()
    st.caption("Author: Ji-Eun Son")


# ============================================================
# 6. Pages
# ============================================================

if page == "Project Guide":
    render_hero()
    render_page_key_message(
        "이 페이지의 핵심 메시지",
        "이 프로젝트는 단순히 A/B Test 계산을 하는 것이 아니라, <b>행동 로그 → 퍼널 병목 → 상품·카테고리 기회 → 실험 설계 → 비즈니스 액션</b>으로 이어지는 전체 분석 흐름을 보여줍니다.",
        "A/B Test는 실험 하나만 잘한다고 되는 것이 아닙니다. 먼저 어디가 문제인지 찾아야 하고, 그 문제를 어떤 지표로 검증할지 정해야 합니다.",
        "먼저 Event Log, Funnel, Conversion, Uplift, Sample Size 개념을 이해한 뒤 Executive Summary부터 순서대로 읽으면 됩니다.",
    )
    render_beginner_story()
    render_abtest_concepts()

    st.markdown("## 이 프로젝트의 분석 흐름")
    flow = pd.DataFrame(
        [
            ["1. Raw Data Audit", "데이터가 어떤 구조인지, 빠진 값이나 이상한 값은 없는지 점검합니다."],
            ["2. Funnel Analysis", "사용자가 상품을 보고 장바구니에 담고 구매하기까지 어디서 이탈하는지 봅니다."],
            ["3. Item & Category Analysis", "어떤 상품과 카테고리가 잘 전환되고, 어디를 개선해야 하는지 찾습니다."],
            ["4. A/B Test Simulation", "전환율을 얼마나 올리면 의미 있는지, 몇 명의 사용자가 필요한지 계산합니다."],
            ["5. Business Recommendation", "분석 결과를 실제 실행 가능한 실험 로드맵으로 정리합니다."],
        ],
        columns=["Step", "What we do"],
    )
    show_table_with_guide(
        "Project Flow",
        flow,
        "왼쪽은 분석 단계, 오른쪽은 각 단계에서 하는 일을 쉽게 설명한 것입니다.",
        "이 프로젝트는 단순히 그래프를 그리는 것이 아니라, 데이터에서 문제를 찾고 그 문제를 실험으로 개선하는 전체 과정을 보여줍니다.",
        height=230,
    )

    render_metric_strip()

    st.markdown(
        """
        <div class="story-box">
            <div class="story-title">한 문장으로 요약</div>
            이 프로젝트는 <b>“사람들이 상품을 보긴 보는데, 왜 장바구니에 잘 담지 않을까?”</b>라는 질문에서 출발합니다.
            그리고 그 문제를 해결하기 위해 어떤 화면을 실험해야 하는지 데이터로 결정합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


elif page == "Executive Summary":
    st.title("Executive Summary")
    st.markdown("프로젝트의 결론을 먼저 보고 싶은 사람을 위한 페이지입니다.")
    render_page_key_message(
        "이 페이지의 핵심 메시지",
        "가장 큰 병목은 <b>상품조회 후 장바구니 진입 전</b>입니다. 따라서 첫 실험은 결제 화면보다 상품 상세페이지, CTA, 추천 영역을 우선 개선하는 방향이 적절합니다.",
        "전환율이 낮다는 사실만으로는 액션이 나오지 않습니다. 어느 단계에서, 어떤 상품·카테고리에서 문제가 발생하는지 알아야 실험 설계가 가능합니다.",
        "Primary metric은 <b>View → Add to Cart</b>, guardrail metric은 <b>View → Purchase</b>로 두고 실험을 설계합니다.",
    )
    render_metric_strip()

    show_table_with_guide(
        "Executive Summary",
        tables.get("executive_summary", pd.DataFrame()),
        "각 행은 핵심 발견, 비즈니스 기회, 실험 전략, 표본 수, 기대효과를 요약합니다.",
        "가장 중요한 메시지는 상품조회 후 장바구니 진입 전 단계가 핵심 병목이라는 점입니다. 따라서 첫 실험은 결제 화면보다 상품 상세페이지, CTA, 추천 영역을 겨냥해야 합니다.",
        height=280,
    )

    show_table_with_guide(
        "Final A/B Test Insight",
        tables.get("final_abtest_insight", pd.DataFrame()),
        "A/B Test 설계에 필요한 핵심 의사결정 요소를 요약한 표입니다.",
        "전환율 개선은 단순히 좋아 보이는 화면을 고르는 일이 아니라, primary metric, 표본 수, expected impact, guardrail metric을 함께 판단하는 일입니다.",
        height=280,
    )

    show_table_with_guide(
        "Dashboard Storyline",
        tables.get("streamlit_storyline", pd.DataFrame()),
        "대시보드 각 페이지가 어떤 질문에 답하는지 보여줍니다.",
        "결과 나열이 아니라 문제 진단 → 개선 후보 → 실험 설계 → 실행 제안의 흐름으로 읽어야 합니다.",
        height=280,
    )


elif page == "Funnel Analysis":
    st.title("Funnel Analysis")
    st.markdown("사용자가 상품을 보고, 장바구니에 담고, 구매하는 과정에서 어디서 가장 많이 이탈하는지 확인합니다.")
    render_page_key_message(
        "이 페이지의 핵심 메시지",
        "퍼널 분석 결과, 사용자 대부분은 상품을 본 뒤 장바구니에 담기 전에 이탈합니다.",
        "이커머스에서 구매 전환을 높이려면 결제 단계만 볼 것이 아니라, 사용자가 상품을 보고 ‘담아볼 만하다’고 느끼는 순간을 만들어야 합니다.",
        "A/B Test의 첫 번째 타깃을 상품 상세페이지 CTA, 혜택 메시지, 리뷰·신뢰 정보, 추천 영역으로 설정합니다.",
    )

    c1, c2 = st.columns(2)
    with c1:
        show_chart_with_guide(
            "User-Level Funnel",
            "02_user_level_funnel",
            "각 막대는 해당 단계까지 도달한 고유 사용자 수입니다. 막대가 급격히 작아지는 곳이 가장 큰 병목입니다.",
            "상품을 본 사람은 많지만 장바구니에 담은 사람은 매우 적습니다. 즉 상품 상세페이지에서 사용자를 설득하지 못하고 있을 가능성이 있습니다.",
        )
    with c2:
        show_chart_with_guide(
            "Conversion Rates",
            "02_user_level_conversion_rates",
            "각 단계 사이에서 몇 %의 사용자가 다음 행동으로 넘어갔는지 보여줍니다.",
            "View → Add to Cart 전환율이 낮기 때문에, A/B Test의 첫 목표는 장바구니 진입률을 높이는 것입니다.",
        )

    show_table_with_guide(
        "Conversion Summary",
        tables.get("conversion_summary", pd.DataFrame()),
        "numerator는 성공 사용자 수, denominator는 전환 대상 사용자 수입니다. conversion_rate는 numerator / denominator입니다.",
        "View → Add to Cart 전환율이 약 2.69%로 낮습니다. 사용자가 구매까지 가지 않는 이유는 이미 장바구니 이후가 아니라 그 전 단계에서 시작됩니다.",
        height=220,
    )

    c1, c2 = st.columns(2)
    with c1:
        show_chart_with_guide(
            "Daily Funnel Users",
            "02_daily_funnel_users",
            "일자별 view, cart, purchase 사용자 수 추이를 보여줍니다.",
            "날짜별 트래픽은 변하지만, 전체적으로 view 사용자에 비해 cart와 purchase 사용자는 낮은 수준입니다.",
        )
    with c2:
        show_chart_with_guide(
            "Daily Conversion Rate Trend",
            "02_daily_conversion_rate_trend",
            "일자별 전환율 변화를 보여줍니다. 너무 작은 일별 변동보다 전체 패턴을 봐야 합니다.",
            "Cart → Purchase는 상대적으로 높은 수준이지만, View → Cart는 낮은 수준에 머뭅니다. 실험 타깃이 명확해집니다.",
        )

    show_chart_with_guide(
        "Monthly Conversion Rate Trend",
        "02_monthly_conversion_rate_trend",
        "월별 전환율을 비교하여 구조적 흐름을 확인합니다.",
        "월별로 병목 구조가 크게 바뀌지 않으므로, 특정 이벤트 문제가 아니라 상품 경험 전반의 개선 문제로 볼 수 있습니다.",
    )

    show_table_with_guide(
        "Problem Diagnosis",
        tables.get("problem_diagnosis", pd.DataFrame()),
        "각 단계의 전환율과 이탈률을 함께 보여줍니다.",
        "View → Add to Cart가 primary bottleneck입니다. View → Purchase는 최종 성과를 감시하는 guardrail metric으로 사용합니다.",
        height=280,
    )


elif page == "Item & Category Insights":
    st.title("Item & Category Insights")
    st.markdown("어떤 상품과 카테고리가 전환을 잘 만들고, 어떤 영역을 먼저 개선해야 하는지 확인합니다.")
    render_page_key_message(
        "이 페이지의 핵심 메시지",
        "모든 상품을 똑같이 개선할 필요는 없습니다. <b>조회는 많은데 전환이 낮은 영역</b>과 <b>조회는 적지만 전환이 높은 영역</b>을 구분해야 합니다.",
        "트래픽이 많은 저전환 영역은 UX 개선 실험 후보이고, 트래픽이 적은 고전환 영역은 노출 확대 실험 후보입니다.",
        "Optimization 후보에는 상세페이지·CTA 개선 실험을, Expansion 후보에는 추천·검색 노출 확대 실험을 제안합니다.",
    )

    show_chart_with_guide(
        "Category Opportunity Matrix",
        "03_category_opportunity_matrix",
        "X축은 조회 사용자 수, Y축은 View → Purchase 전환율입니다. 오른쪽 아래는 고트래픽 저전환, 왼쪽 위는 저트래픽 고전환 후보입니다.",
        "조회가 많은데 구매 전환율이 낮은 카테고리는 첫 A/B Test 후보입니다. 조회는 적지만 전환율이 높은 카테고리는 노출 확대 후보입니다.",
    )

    c1, c2 = st.columns(2)
    with c1:
        show_chart_with_guide(
            "Top Categories by View Users",
            "03_top_categories_by_view_users",
            "조회 사용자 수가 많은 카테고리를 보여줍니다.",
            "트래픽이 집중된 카테고리는 개선 실험을 했을 때 impact가 클 가능성이 높습니다.",
        )
    with c2:
        show_chart_with_guide(
            "Top Categories by Purchase Users",
            "03_top_categories_by_purchase_users",
            "구매 사용자가 많은 카테고리를 보여줍니다.",
            "많이 조회되는 카테고리와 많이 구매되는 카테고리가 다를 수 있습니다. 그 차이가 최적화 기회입니다.",
        )

    c1, c2 = st.columns(2)
    with c1:
        show_chart_with_guide(
            "Top Categories by View → Add to Cart Rate",
            "03_top_categories_by_cart_conversion_rate",
            "조회 대비 장바구니 전환율이 높은 카테고리입니다.",
            "이 카테고리들은 CTA, 상품 구성, 가격, 신뢰 정보가 상대적으로 잘 작동하고 있을 수 있습니다.",
        )
    with c2:
        show_chart_with_guide(
            "Top Categories by View → Purchase Rate",
            "03_top_categories_by_purchase_conversion_rate",
            "조회 대비 구매 전환율이 높은 카테고리입니다.",
            "전환율이 높은데 조회가 적은 카테고리는 추천 영역이나 검색 노출 확대 실험 후보입니다.",
        )

    show_table_with_guide(
        "Category Opportunity Summary",
        tables.get("category_opportunity", pd.DataFrame()),
        "카테고리를 Star, Optimization, Expansion, Long-tail 네 유형으로 구분한 요약입니다.",
        "Optimization은 고트래픽 저전환 영역으로 첫 A/B Test 후보이고, Expansion은 저트래픽 고전환 영역으로 노출 확대 후보입니다.",
        height=260,
    )

    show_table_with_guide(
        "Optimization Candidate Categories",
        tables.get("optimization_categories", pd.DataFrame()),
        "조회는 많지만 전환율이 낮은 카테고리 목록입니다.",
        "이미 트래픽이 있으므로 상세페이지 CTA, 혜택 메시지, 리뷰 신뢰 정보 개선 실험의 우선 대상입니다.",
        height=340,
    )

    show_table_with_guide(
        "Expansion Candidate Categories",
        tables.get("expansion_categories", pd.DataFrame()),
        "조회는 적지만 전환율이 높은 카테고리 목록입니다.",
        "상품 경쟁력이 있을 가능성이 있으므로 추천 영역, 검색 랭킹, 프로모션 노출 확대를 테스트할 수 있습니다.",
        height=340,
    )


elif page == "A/B Test Simulation":
    st.title("A/B Test Simulation")
    st.markdown("현재 baseline 전환율을 기준으로 uplift, 표본 수, 통계적 검정, business impact를 시뮬레이션합니다.")
    render_page_key_message(
        "이 페이지의 핵심 메시지",
        "A/B Test는 ‘개선안이 좋아 보인다’가 아니라, 충분한 표본에서 전환율 차이가 통계적으로 의미 있는지 확인하는 과정입니다.",
        "전환율이 낮은 지표일수록 작은 uplift를 검출하려면 많은 사용자가 필요합니다. 그래서 실험 전 sample size 계산이 중요합니다.",
        "View → Add to Cart를 primary metric으로 두고, uplift별 필요 표본 수와 100,000명 기준 기대 추가 장바구니 사용자를 함께 확인합니다.",
    )

    show_table_with_guide(
        "Experiment Baseline",
        tables.get("abtest_baseline", pd.DataFrame()),
        "실험에서 사용할 primary metric과 guardrail metric의 baseline을 보여줍니다.",
        "Primary metric은 View → Add to Cart이고, View → Purchase는 downstream guardrail metric입니다.",
        height=220,
    )

    c1, c2 = st.columns(2)
    with c1:
        show_table_with_guide(
            "Sample Size by Uplift Scenario",
            tables.get("sample_size", pd.DataFrame()),
            "relative uplift별로 필요한 그룹당 표본 수를 보여줍니다.",
            "작은 uplift를 탐지하려면 훨씬 많은 표본이 필요합니다. 실험은 충분한 트래픽이 있는 영역에서 해야 합니다.",
            height=300,
        )
    with c2:
        show_chart_with_guide(
            "Required Sample Size by Uplift",
            "04_required_sample_size_by_uplift",
            "X축은 기대 uplift, Y축은 그룹당 필요 표본 수입니다.",
            "uplift가 작을수록 필요한 표본 수가 급격히 증가합니다. 그래서 실험 전에 sample size를 계산해야 합니다.",
        )

    c1, c2 = st.columns(2)
    with c1:
        show_chart_with_guide(
            "Monte Carlo p-value Distribution",
            "04_monte_carlo_p_value_distribution",
            "같은 조건의 실험을 여러 번 반복했을 때 p-value가 어떻게 분포하는지 보여줍니다.",
            "실험 결과는 우연의 영향을 받습니다. 한 번의 p-value보다 실험 설계와 표본 수가 중요합니다.",
        )
    with c2:
        show_chart_with_guide(
            "Estimated Lift Distribution",
            "04_monte_carlo_absolute_lift_distribution",
            "반복 실험에서 추정된 absolute lift의 분포입니다.",
            "같은 효과가 있어도 관측된 lift는 매번 달라집니다. confidence interval과 power를 함께 봐야 합니다.",
        )

    c1, c2 = st.columns(2)
    with c1:
        show_table_with_guide(
            "Business Impact Scenario",
            tables.get("business_impact", pd.DataFrame()).head(30),
            "노출 사용자 수와 uplift별 예상 추가 장바구니 사용자를 보여줍니다.",
            "전환율의 작은 변화도 트래픽 규모가 크면 의미 있는 추가 행동으로 이어질 수 있습니다.",
            height=300,
        )
    with c2:
        show_chart_with_guide(
            "Expected Incremental Cart Users per 100,000 Views",
            "04_expected_incremental_cart_users_per_100k",
            "100,000 view users 기준 uplift별 추가 장바구니 사용자 수입니다.",
            "비즈니스 의사결정에서는 p-value뿐 아니라 실제 증가 사용자 수를 함께 봐야 합니다.",
        )

    st.subheader("Candidate Category Simulation")
    candidate_simulation = load_table_cached("04_category_abtest_simulation.csv", required=False)

    if is_empty(candidate_simulation):
        fallback = candidate_category_fallback()
        st.markdown(
            """
            <div class="read-box">
            <b>데이터 안내</b><br>
            04번 노트북에서 category-level simulation 파일이 생성되지 않았습니다.
            대신 03번 노트북의 <b>Optimization Candidate Categories</b>를 실험 후보군으로 표시합니다.
            </div>
            """,
            unsafe_allow_html=True,
        )
        show_dataframe(fallback, height=320)
        st.markdown(
            """
            <div class="insight-box">
            <b>해석</b><br>
            이 후보군은 조회 사용자가 많지만 전환율이 낮은 카테고리입니다.
            첫 A/B Test는 이 카테고리들의 상품 상세페이지 CTA, 혜택 메시지, 추천 영역을 대상으로 설계하는 것이 합리적입니다.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        show_table_with_guide(
            "Category-Level A/B Test Candidate Simulation",
            candidate_simulation,
            "카테고리별 baseline, uplift, 필요 표본 수, 예상 추가 장바구니 사용자를 보여줍니다.",
            "현재 트래픽으로 실험 가능한 카테고리와 추가 impact가 큰 카테고리를 함께 고려해야 합니다.",
            height=320,
        )
        show_chart_with_guide(
            "Candidate Category Incremental Cart Users",
            "04_candidate_category_incremental_cart_users",
            "후보 카테고리별 예상 추가 장바구니 사용자를 비교합니다.",
            "impact가 큰 카테고리를 우선 실험 대상으로 선정할 수 있습니다.",
        )


elif page == "Business Action Plan":
    st.title("Business Action Plan")
    st.markdown("분석 결과를 실행 우선순위, 실험 로드맵, 최종 의사결정 기준으로 정리합니다.")

    render_business_action_summary()

    show_table_with_guide(
        "Opportunity Prioritization",
        tables.get("opportunity_prioritization", pd.DataFrame()),
        "대상 영역을 impact, 실험 가능성, 리스크 기준으로 우선순위화합니다.",
        "첫 번째 우선순위는 고트래픽 저전환 상품·카테고리입니다. 이미 트래픽이 있기 때문에 개선 효과가 빠르게 나타날 수 있습니다.",
        height=260,
    )

    show_table_with_guide(
        "A/B Test Roadmap",
        tables.get("abtest_roadmap", pd.DataFrame()),
        "실험 순서, 대상, control, treatment, primary metric, guardrail metric을 제안합니다.",
        "첫 실험은 Product Detail CTA Optimization으로 시작하고, 이후 신뢰 정보 강화와 추천 노출 확대 실험으로 확장하는 흐름이 적절합니다.",
        height=340,
    )

    c1, c2 = st.columns(2)
    with c1:
        show_table_with_guide(
            "Business Impact per 100,000 View Users",
            tables.get("impact_100k", pd.DataFrame()),
            "100,000 view users 기준 uplift별 예상 추가 장바구니 사용자입니다.",
            "비율 개선이 작아도 트래픽이 크면 실제 추가 행동 수는 커집니다.",
            height=260,
        )
    with c2:
        show_chart_with_guide(
            "Business Impact Chart",
            "05_business_impact_per_100k",
            "uplift별 예상 추가 장바구니 사용자 수를 막대그래프로 비교합니다.",
            "실험 우선순위는 통계적 유의성과 함께 예상 impact를 기준으로 결정해야 합니다.",
        )

    show_table_with_guide(
        "Final Recommendation",
        tables.get("final_recommendation", pd.DataFrame()),
        "최종 제안, 근거, 기대효과, 우선순위를 정리한 표입니다.",
        "본 프로젝트의 최종 제안은 고트래픽 저전환 영역에서 View → Add to Cart 전환율을 개선하는 실험을 먼저 수행하는 것입니다.",
        height=320,
    )

    show_table_with_guide(
        "Experiment Decision Rule",
        tables.get("decision_rule", pd.DataFrame()),
        "실험 결과를 배포할지 판단하는 기준입니다.",
        "Treatment는 primary metric을 유의하게 개선하고, guardrail metric을 악화시키지 않아야 합니다.",
        height=300,
    )


elif page == "Data & Repository Notes":
    st.title("Data & Repository Notes")
    st.markdown("데이터 관리 방식과 재현 가능한 프로젝트 구조를 정리합니다.")
    render_page_key_message(
        "이 페이지의 핵심 메시지",
        "이 프로젝트는 대용량 raw data를 GitHub에 올리지 않고, 분석에 필요한 processed CSV와 outputs summary를 기반으로 재현되도록 구성했습니다.",
        "실무에서는 원본 데이터와 분석 산출물을 구분해 관리해야 합니다. 특히 대용량 로그 데이터는 raw layer, processed layer, reporting layer로 나누는 것이 중요합니다.",
        "재현하려면 Kaggle 원본 데이터를 data/raw에 두고 01~05 노트북을 순서대로 실행한 뒤 Streamlit을 실행하면 됩니다.",
    )

    show_table_with_guide(
        "Raw Audit Summary",
        tables.get("raw_audit_summary", pd.DataFrame()),
        "원천 데이터의 row 수, 기간, 주요 엔티티 수를 요약합니다.",
        "행동 로그는 유지하고, 대용량 item_properties는 분석에 필요한 category mapping 중심으로 요약했습니다.",
        height=320,
    )

    st.subheader("Repository Policy")
    st.markdown(
        """
        Raw data files are excluded from the repository due to file size.

        Expected local structure:

        ```text
        data/raw/
        ├── category_tree.csv
        ├── events.csv
        ├── item_properties_part1.csv
        └── item_properties_part2.csv
        ```

        Streamlit does not directly load raw data.  
        It uses processed CSV files and summary result tables generated by notebooks.
        """
    )

    show_table_with_guide(
        "README / WikiDocs Summary",
        tables.get("readme_wikidocs_summary", pd.DataFrame()),
        "README와 WikiDocs 기술서에 사용할 요약 문장입니다.",
        "프로젝트 설명은 데이터 출처보다 문제 진단, 실험 설계, 비즈니스 제안 흐름을 강조하는 것이 좋습니다.",
        height=280,
    )

    st.subheader("Available Charts")
    chart_list = pd.DataFrame(
        [{"chart_name": key, "path": str(path.relative_to(PROJECT_ROOT))} for key, path in charts.items()]
    )
    show_dataframe(chart_list, height=420)


# ============================================================
# 7. Footer
# ============================================================

st.divider()
st.caption("E-commerce A/B Test Techbook · Ji-Eun Son")
