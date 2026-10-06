
import html
import zlib

import pandas as pd
import streamlit as st
import psycopg2


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Trending - Top Videos",
    page_icon="▶️",
    layout="wide"
)

CATEGORIES = {
    "1": "Film & Animation",
    "2": "Autos",
    "10": "Music",
    "15": "Pets",
    "17": "Sports",
    "19": "Travel",
    "20": "Gaming",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News",
    "26": "How-to",
    "27": "Education",
    "28": "Science & Tech",
}

AVATARS = [
    "#c0392b",
    "#2874a6",
    "#1e8449",
    "#7d3c98",
    "#b9770e",
    "#117a8b",
    "#34495e",
    "#a93226",
]

DEVELOPER = "Vadlakonda Achyuth Sai"


# ============================================================
# STYLING
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

:root{
    --ink:#0f0f0f;
    --sub:#606060;
    --chip:#f2f2f2;
    --chip-hover:#e5e5e5;
    --line:#e5e5e5;
    --red:#ff0000;
    --blue:#065fd4;
    --green:#0d652d;
}

.stApp{
    background:#fff;
    color:var(--ink);
    font-family:Roboto,Arial,sans-serif;
}

.block-container{
    max-width:1700px;
    padding:.6rem 1.6rem 3rem;
}

header[data-testid="stHeader"]{
    display:none;
}

[data-testid="stWidgetLabel"] p{
    color:var(--ink);
    font-weight:500;
    font-size:.85rem;
}

[data-testid="stTextInput"] input{
    border-radius:40px 0 0 40px;
    padding:.55rem 1.1rem;
    border:1px solid #ccc;
    background:#fff;
    font-size:.95rem;
}

[data-testid="stTextInput"] input:focus{
    border-color:var(--blue);
}

[data-testid="stTextInput"] div[data-baseweb="input"],
[data-testid="stTextInput"] div[data-baseweb="base-input"]{
    border-radius:40px 0 0 40px;
    border:none;
    background:#fff;
}

[data-testid="stSelectbox"] div[data-baseweb="select"]>div{
    border-radius:10px;
    background:var(--chip);
    border:none;
}

.stButton button{
    border-radius:18px;
    background:var(--chip);
    border:none;
    color:var(--ink);
    font-weight:500;
}

.stButton button:hover{
    background:var(--chip-hover);
    color:var(--ink);
}

[data-testid="stPills"] button{
    border-radius:8px;
    font-weight:500;
    background:var(--chip);
    border:none;
    color:var(--ink);
}

[data-testid="stPills"] button:hover{
    background:var(--chip-hover);
}

[data-testid="stPills"] button[aria-checked="true"],
[data-testid="stPills"] button[aria-pressed="true"]{
    background:var(--ink);
    color:#fff;
}

[data-testid="stVideo"] iframe,
[data-testid="stVideo"] video{
    border-radius:12px;
}

.topbar{
    display:flex;
    align-items:center;
    gap:.9rem;
}

.burger{
    display:flex;
    flex-direction:column;
    gap:4px;
    padding:8px;
}

.burger i{
    display:block;
    width:18px;
    height:2px;
    background:var(--ink);
    border-radius:2px;
}

.logo-icon{
    width:32px;
    height:22px;
    background:var(--red);
    border-radius:6px;
    position:relative;
    flex:none;
}

.logo-icon:after{
    content:"";
    position:absolute;
    left:12px;
    top:5.5px;
    border-left:9px solid #fff;
    border-top:5.5px solid transparent;
    border-bottom:5.5px solid transparent;
}

.logo-text{
    font-size:1.3rem;
    font-weight:700;
    letter-spacing:-.05em;
    margin-left:-.4rem;
}

.logo-country{
    color:var(--sub);
    font-size:.6rem;
    align-self:flex-start;
    margin:.2rem 0 0 -.5rem;
}

.dev{
    display:flex;
    align-items:center;
    justify-content:flex-end;
    gap:10px;
}

.dev .who{
    text-align:right;
    line-height:1.25;
}

.dev .who small{
    display:block;
    color:var(--sub);
    font-size:.7rem;
}

.dev .who b{
    font-size:.85rem;
    font-weight:500;
}

.me{
    width:34px;
    height:34px;
    border-radius:50%;
    background:#8e44ad;
    color:#fff;
    font-weight:500;
    font-size:.8rem;
    display:flex;
    align-items:center;
    justify-content:center;
    flex:none;
}

hr.navline{
    border:0;
    border-top:1px solid var(--line);
    margin:.5rem -1.6rem 0;
}

.page-title{
    font-size:1.6rem;
    font-weight:700;
    letter-spacing:-.02em;
    margin:1.2rem 0 .2rem;
}

.statline{
    color:var(--sub);
    font-size:.85rem;
    padding-bottom:.9rem;
}

.statline b{
    color:var(--ink);
    font-weight:500;
}

.statline i{
    margin:0 .5rem;
    font-style:normal;
}

.sec{
    font-size:1.25rem;
    font-weight:700;
    margin:1.6rem 0 .9rem;
}

hr.div{
    border:0;
    border-top:1px solid var(--line);
    margin:2rem -1.6rem 0;
}

.grid{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
    gap:32px 16px;
    margin-top:.6rem;
}

a.vc{
    text-decoration:none;
    color:inherit;
    display:block;
}

.thumb{
    position:relative;
    aspect-ratio:16/9;
    background:#e5e5e5;
    border-radius:12px;
    overflow:hidden;
    transition:border-radius .2s ease;
}

.thumb img{
    width:100%;
    height:100%;
    object-fit:cover;
    display:block;
    transition:transform .2s ease;
}

a.vc:hover .thumb{
    border-radius:0;
}

a.vc:hover .thumb img{
    transform:scale(1.02);
}

.badge{
    position:absolute;
    left:8px;
    bottom:8px;
    background:rgba(0,0,0,.8);
    color:#fff;
    font-size:1.05rem;
    font-weight:700;
    padding:3px 11px;
    border-radius:6px;
    line-height:1.3;
}

.badge.top{
    background:var(--red);
}

.meta{
    display:flex;
    gap:12px;
    margin-top:12px;
}

.av{
    width:36px;
    height:36px;
    border-radius:50%;
    flex:none;
    color:#fff;
    font-weight:500;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:.95rem;
}

.ct{
    font-size:1rem;
    font-weight:500;
    line-height:1.35;
    color:var(--ink);
    display:-webkit-box;
    -webkit-line-clamp:2;
    -webkit-box-orient:vertical;
    overflow:hidden;
}

.cc{
    font-size:.82rem;
    color:var(--sub);
    margin-top:3px;
}

.vc:hover .cc.ch{
    color:var(--ink);
}

.wtitle{
    font-size:1.25rem;
    font-weight:700;
    line-height:1.4;
    margin:.8rem 0 .7rem;
}

.wchan{
    display:flex;
    align-items:center;
    gap:12px;
    flex-wrap:wrap;
}

.wchan .nm{
    font-weight:500;
}

.wchan .sb{
    color:var(--sub);
    font-size:.8rem;
}

.pills{
    margin-left:auto;
    display:flex;
    gap:8px;
    flex-wrap:wrap;
}

.pill{
    background:var(--chip);
    border-radius:18px;
    padding:.45rem 1rem;
    font-size:.88rem;
    font-weight:500;
}

a.btn{
    background:var(--ink);
    color:#fff !important;
    text-decoration:none;
    padding:.5rem 1rem;
    border-radius:18px;
    font-weight:500;
    font-size:.88rem;
}

a.btn:hover{
    background:#272727;
}

.desc{
    background:var(--chip);
    border-radius:12px;
    padding:.9rem 1rem;
    margin-top:1rem;
    font-size:.9rem;
    line-height:1.5;
}

.desc b{
    font-weight:500;
}

.upnext-title{
    font-size:1.05rem;
    font-weight:700;
    margin:.8rem 0 12px;
}

.row{
    display:flex;
    gap:8px;
    margin-bottom:12px;
}

.row .thumb{
    width:168px;
    flex:none;
    border-radius:8px;
}

.row .ct{
    font-size:.92rem;
}

.match{
    color:var(--green);
    font-weight:500;
}

.footer{
    margin-top:3rem;
    padding-top:1.2rem;
    border-top:1px solid var(--line);
    color:var(--sub);
    font-size:.8rem;
    text-align:center;
    line-height:1.7;
}

.footer b{
    color:var(--ink);
    font-weight:500;
}

:focus-visible{
    outline:2px solid var(--blue);
    outline-offset:2px;
}

@media (max-width:900px){
    .block-container{
        padding:.6rem 1rem 2rem;
    }

    .dev .who{
        display:none;
    }

    .pills{
        margin-left:0;
    }
}

@media (prefers-reduced-motion:reduce){
    .thumb,
    .thumb img{
        transition:none;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================

def h(markup):
    """Render HTML without markdown turning indented lines into code."""
    st.markdown(
        "\n".join(
            line.strip()
            for line in markup.splitlines()
            if line.strip()
        ),
        unsafe_allow_html=True
    )


def esc(value, limit=90):
    return html.escape(
        " ".join(
            str(value if pd.notna(value) else "").split()
        )[:limit]
    )


def compact(n):
    try:
        n = float(n)
    except Exception:
        return "0"

    for div, suffix in (
        (1e9, "B"),
        (1e6, "M"),
        (1e3, "K")
    ):
        if n >= div:
            return f"{n / div:.1f}{suffix}".replace(".0", "")

    return str(int(n))


def url(video_id):
    return "https://www.youtube.com/watch?v=" + html.escape(str(video_id))


def thumb(src, badge="", badge_class="", chip=""):
    img = (
        f'<img src="{html.escape(str(src))}" loading="lazy" alt="">'
        if pd.notna(src) and str(src).strip()
        else ""
    )

    tag = (
        f'<span class="badge {badge_class}">{badge}</span>'
        if badge else ""
    )

    chip_html = (
        f'<span class="catchip">{html.escape(chip)}</span>'
        if chip else ""
    )

    return f'<div class="thumb">{img}{tag}{chip_html}</div>'


def avatar(channel, small=False):
    name = str(
        channel if pd.notna(channel) else "?"
    ).strip() or "?"

    color = AVATARS[
        zlib.crc32(name.encode()) % len(AVATARS)
    ]

    size = " sm" if small else ""

    return (
        f'<div class="av{size}" style="background:{color}">'
        f'{html.escape(name[0].upper())}'
        f'</div>'
    )


# ============================================================
# NEON POSTGRESQL CONNECTION
# ============================================================

@st.cache_resource(ttl=3600)
@st.cache_resource(ttl=3600)
def get_connection():
    return psycopg2.connect(
        host=st.secrets["neon"]["host"],
        database=st.secrets["neon"]["database"],
        user=st.secrets["neon"]["user"],
        password=st.secrets["neon"]["password"],
        port=5432,
        sslmode="require"
    )

def _execute(conn, query, params=None):
    with conn.cursor() as cur:
        cur.execute(
            query,
            params if params else ()
        )

        if cur.description is None:
            return pd.DataFrame()

        columns = [d[0] for d in cur.description]
        rows = cur.fetchall()

    return pd.DataFrame(rows, columns=columns)


def run_query(query, params=None):
    conn = get_connection()

    try:
        return _execute(conn, query, params)

    except Exception:
        try:
            conn.close()
        except Exception:
            pass

        get_connection.clear()

        return _execute(
            get_connection(),
            query,
            params
        )


# ============================================================
# DATA LOADERS
# ============================================================

@st.cache_data(ttl=60)
def load_trending():
    return run_query("""
        WITH latest_date AS (
            SELECT MAX(collection_date) AS max_date
            FROM trending_videos
        ),

        latest_videos AS (
            SELECT
                video_id,
                title,
                channel_name,
                category_id,
                view_count,
                like_count,
                comment_count,
                thumbnail_url,
                video_url,
                collection_date,
                collected_at,
                rank,

                ROW_NUMBER() OVER (
                    PARTITION BY video_id
                    ORDER BY collected_at DESC
                ) AS video_rn

            FROM trending_videos

            WHERE collection_date = (
                SELECT max_date
                FROM latest_date
            )
        )

        SELECT
            video_id,
            title,
            channel_name,
            category_id,
            view_count,
            like_count,
            comment_count,
            thumbnail_url,
            video_url,
            collection_date,
            collected_at,
            rank

        FROM latest_videos

        WHERE video_rn = 1

        ORDER BY view_count DESC

        LIMIT 100
    """)


@st.cache_data(ttl=300)
def load_recommendations():
    return run_query("""
        SELECT
            video_id,
            recommended_video_id,
            similarity_score,
            rank

        FROM video_recommendations

        ORDER BY video_id, rank
    """)


@st.cache_data(ttl=300)
def load_video_catalog():
    return run_query("""
        SELECT DISTINCT ON (video_id)
            video_id,
            title,
            channel_name,
            category_id,
            thumbnail_url

        FROM trending_videos

        ORDER BY
            video_id,
            collection_date DESC,
            collected_at DESC
    """)


# ============================================================
# HEADER
# ============================================================

search_col, dev_col, refresh_col = st.columns(
    [4, 2.4, 1.2],
    vertical_alignment="center"
)

with search_col:
    query = st.text_input(
        "Search",
        placeholder="Search videos or channels",
        label_visibility="collapsed"
    ).strip()

with dev_col:
    h(
        '<div class="dev">'
        '<div class="who">'
        '<small>Developed by</small>'
        f'<b>{DEVELOPER}</b>'
        '</div>'
        '<div class="me">VA</div>'
        '</div>'
    )

with refresh_col:
    if st.button(
        "Refresh",
        width="stretch"
    ):
        st.cache_data.clear()
        st.rerun()

h('<hr class="navline">')


# ============================================================
# LOAD TRENDING DATA
# ============================================================

try:
    trending = load_trending()

except Exception as e:
    st.error(
        "Could not connect to the Neon PostgreSQL database."
    )

    st.code(str(e))

    st.stop()


if trending.empty:
    st.warning(
        "No trending videos are available yet. "
        "Run the data pipeline and refresh."
    )

    st.stop()


for col in (
    "view_count",
    "like_count",
    "comment_count"
):
    trending[col] = pd.to_numeric(
        trending[col],
        errors="coerce"
    ).fillna(0)


trending["category"] = (
    trending["category_id"]
    .astype(str)
    .map(CATEGORIES)
    .fillna("Other")
)


try:
    updated = (
        pd.to_datetime(
            trending["collected_at"]
        )
        .max()
        .strftime("%d %b %Y, %H:%M")
    )

except Exception:
    updated = str(
        trending["collected_at"].max()
    )[:16]


# ============================================================
# PAGE HEADING
# ============================================================

h(f"""
<div class="page-title">Top Trending Videos</div>

<div class="statline">
    <b>{trending["video_id"].nunique():,}</b> videos
    <i>•</i>
    <b>{compact(trending["view_count"].sum())}</b> views
    <i>•</i>
    <b>{compact(trending["like_count"].sum())}</b> likes
    <i>•</i>
    <b>{trending["category"].nunique()}</b> categories
    <i>•</i>
    Updated {html.escape(updated)}
</div>
""")


# ============================================================
# CATEGORY CHIPS
# ============================================================

options = (
    ["All"]
    + trending["category"]
    .value_counts()
    .index
    .tolist()
)

choice = st.pills(
    "Category",
    options,
    default="All",
    label_visibility="collapsed"
) or "All"


shown = (
    trending
    if choice == "All"
    else trending[
        trending["category"] == choice
    ]
)


if query:
    hay = (
        shown["title"].fillna("")
        + " "
        + shown["channel_name"].fillna("")
    )

    shown = shown[
        hay.str.contains(
            query,
            case=False,
            regex=False
        )
    ]


# ============================================================
# TRENDING GRID
# ============================================================

if shown.empty:

    st.info(
        "No trending videos match your search "
        "or category. Try a different keyword."
    )

else:

    cards = ""

    for rank, v in enumerate(
        shown.head(12).itertuples(index=False),
        start=1
    ):

        row = v._asdict()

        cards += f"""
        <a class="vc"
           href="{url(row['video_id'])}"
           target="_blank"
           rel="noopener">

            {thumb(
                row['thumbnail_url'],
                f'#{rank}',
                'top' if rank <= 3 else ''
            )}

            <div class="meta">

                {avatar(row['channel_name'])}

                <div>

                    <div class="ct">
                        {esc(row['title'], 100)}
                    </div>

                    <div class="cc ch">
                        {esc(row['channel_name'])}
                    </div>

                    <div class="cc">
                        {compact(row['view_count'])} views
                        •
                        {compact(row['like_count'])} likes
                        •
                        {esc(row['category'])}
                    </div>

                </div>

            </div>

        </a>
        """

    h(
        f'<div class="grid">{cards}</div>'
    )


# ============================================================
# WATCH + RECOMMENDATIONS
# ============================================================

h(
    '<hr class="div">'
    '<div class="sec">Watch and discover</div>'
)


try:

    rec_links = load_recommendations()
    catalog = load_video_catalog()

except Exception as e:

    rec_links = pd.DataFrame()
    catalog = pd.DataFrame()

    st.warning(
        "Recommendation data could not be loaded."
    )

    st.code(str(e))


if rec_links.empty or catalog.empty:

    st.info(
        "No recommendation data available yet."
    )

else:

    rec_links["video_id"] = (
        rec_links["video_id"].astype(str)
    )

    rec_links["recommended_video_id"] = (
        rec_links["recommended_video_id"]
        .astype(str)
    )

    catalog["video_id"] = (
        catalog["video_id"].astype(str)
    )


    rec_links = rec_links.merge(
        catalog.add_prefix("rec_"),
        left_on="recommended_video_id",
        right_on="rec_video_id",
        how="left"
    )


    haystack = (
        catalog["title"].fillna("")
        + " "
        + catalog["channel_name"].fillna("")
    )


    matches = (
        catalog[
            haystack.str.contains(
                query,
                case=False,
                regex=False
            )
        ]
        if query
        else catalog
    ).head(100)


    if matches.empty:

        st.warning(
            "No videos match that search. "
            "Try a shorter word or a channel name."
        )

    else:

        labels = {
            r.video_id:
                f"{str(r.title)[:90]} - {r.channel_name}"
            for r in matches.itertuples()
        }


        chosen = st.selectbox(
            "Choose a video to watch"
            + (
                f" (results for “{query}”)"
                if query
                else ""
            ),

            list(labels),

            format_func=labels.get
        )


        sel = catalog[
            catalog["video_id"] == chosen
        ].iloc[0]


        category = CATEGORIES.get(
            str(sel["category_id"]),
            "Other"
        )


        stats = trending[
            trending["video_id"].astype(str)
            == chosen
        ]


        pills = ""


        if not stats.empty:

            s = stats.iloc[0]

            pills = (
                f'<div class="pill">'
                f'👍 {compact(s["like_count"])}'
                f'</div>'

                f'<div class="pill">'
                f'💬 {compact(s["comment_count"])}'
                f'</div>'

                f'<div class="pill">'
                f'👁 {compact(s["view_count"])} views'
                f'</div>'
            )


        recs = rec_links[
            rec_links["video_id"] == chosen
        ].copy()


        if not recs.empty:

            recs = (
                recs
                .sort_values(
                    "rank",
                    ascending=True
                )
                .head(8)
            )


        main_col, side_col = st.columns(
            [2.3, 1],
            gap="large"
        )


        # ====================================================
        # MAIN VIDEO
        # ====================================================

        with main_col:

            st.video(
                url(chosen)
            )


            h(f"""
            <div class="wtitle">
                {esc(sel['title'], 150)}
            </div>

            <div class="wchan">

                {avatar(sel['channel_name'])}

                <div>

                    <div class="nm">
                        {esc(sel['channel_name'])}
                    </div>

                    <div class="sb">
                        {html.escape(category)}
                    </div>

                </div>

                <div class="pills">

                    {pills}

                    <a class="btn"
                       href="{url(chosen)}"
                       target="_blank"
                       rel="noopener">

                       Watch on YouTube

                    </a>

                </div>

            </div>
            """)


        # ====================================================
        # UP NEXT
        # ====================================================

        with side_col:

            h(
                '<div class="upnext-title">'
                'Up next'
                '</div>'
            )


            if recs.empty:

                st.info(
                    "No recommendations found "
                    "for this video."
                )

            else:

                rows = ""


                for _, r in recs.iterrows():

                    similarity = pd.to_numeric(
                        r.get("similarity_score"),
                        errors="coerce"
                    )


                    similarity = (
                        0
                        if pd.isna(similarity)
                        else similarity
                    )


                    similarity = max(
                        0.0,
                        min(
                            float(similarity),
                            1.0
                        )
                    )


                    rows += f"""
                    <a class="vc row"
                       href="{url(r['recommended_video_id'])}"
                       target="_blank"
                       rel="noopener">

                        {thumb(
                            r.get("rec_thumbnail_url")
                        )}

                        <div>

                            <div class="ct">
                                {esc(
                                    r.get("rec_title", ""),
                                    80
                                )}
                            </div>

                            <div class="cc ch">
                                {esc(
                                    r.get(
                                        "rec_channel_name",
                                        ""
                                    )
                                )}
                            </div>

                            <div class="cc">
                                <span class="match">
                                    {similarity:.0%} match
                                </span>
                            </div>

                        </div>

                    </a>
                    """


                h(rows)


# ============================================================
# FOOTER
# ============================================================

h(
    '<div class="footer">'
    f'Designed and developed by '
    f'<b>{DEVELOPER}</b><br>'
    'Built with Kafka, Databricks, PySpark, SBERT, '
    'PostgreSQL and Streamlit.'
    '</div>'
)
