"""App to visualize scrapped legal data."""
import json
import os

import matplotlib.pylab as plt
import streamlit as st

import utils

DATADIR = "."

st.set_page_config(
    page_title="Digital forensics",
    page_icon="https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcRH8iuZXk0cdNE_Ix4RSJs2AuEzJerJUBHUwBk1NocX3W7X9BxSvCZ6KBw424HWvWd43EAhLiFYy80t1boaNlfVbnD1iG3hFyr4PQXTLVZnPtb5klZj0RWH4w&usqp=CAE"
)

@st.cache
def load_metadata():
    return utils.load_metadata_df(os.path.join(DATADIR, "metadata.json"))

@st.cache
def load_mentions():
    with open(os.path.join(DATADIR, "mentions.json")) as handle:
        return json.load(handle)

def get_tool_mentions(caselink):
    mention_map = load_mentions()
    if caselink in mention_map:
        return mention_map[caselink]["mentions"]
    return None

df = load_metadata()

st.write("""# Digital Forensic Tools""")

universe_size = df.groupby("tool").size()
universe_size.name = "Number of cases"
st.write(universe_size)

toolname = st.selectbox(
    "Select tool: ", sorted(df.tool.unique()), index=3)

df_tool = df[df.tool == toolname].reset_index()
df_tool = df_tool.sort_values("year", ascending=False)

# Appearance over time
st.write("#### Number of cases per year")
fig, ax = plt.subplots(figsize=(5, 1.5))
df_tool.year.value_counts().sort_index().plot(ax=ax)
ax.set_xlabel("Number of cases")
ax.set_ylabel("Year")
st.pyplot(fig)

st.write("#### Most common courts")
num_appearances = df_tool.court.value_counts().nlargest(10)
num_appearances.name = "Number of cases"
st.write(num_appearances)

st.write("### Tool mentions")
case_num = st.select_slider(
    "Select case (use arrows to toggle). Cases are sorted by year", 
    options=list(range(len(df_tool))))
case = df_tool.iloc[case_num:case_num + 1]
st.write(case[["casename", "court", "year"]])
mentions = get_tool_mentions(case.link.values[0])
st.write(f"Original url: https://scholar.google.com/{case.link.values[0]}")
if mentions:
    st.write(f"Found {len(mentions)} mentions of {toolname}: ")
    for mention in mentions:
        st.write(mention.replace(toolname, f"<span style='color:blue'>**{toolname}**</span>"), unsafe_allow_html=True)
else:
    st.write("Text associated with the case not found or failed to download.")
