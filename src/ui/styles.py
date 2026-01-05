import streamlit as st

def inject_global_styles():
    st.markdown(
        """
<style>
:root{
  --oi-purple:#6A35FF;
  --oi-bg:#0B0F19;
  --oi-card:#111827;
  --oi-border:#1F2937;
  --oi-text:#E5E7EB;
  --oi-sub:#9CA3AF;
}
.oi-card{
  background: linear-gradient(180deg, rgba(106,53,255,0.12), rgba(17,24,39,1));
  border:1px solid var(--oi-border);
  border-radius:16px;
  padding:16px 18px;
  margin: 10px 0 18px 0;
}
.oi-card-title{
  font-size:18px;
  font-weight:800;
  color: var(--oi-text);
  margin-bottom:8px;
}
.oi-section{
  border:1px solid var(--oi-border);
  border-radius:14px;
  padding:14px 16px;
  margin: 12px 0;
  background: rgba(17,24,39,0.65);
}
.oi-section h3{
  margin: 0 0 8px 0;
  font-size:16px;
  font-weight:800;
  color: var(--oi-purple);
}
.oi-section p{
  margin: 0.25rem 0;
}
.oi-section ul, .oi-section ol{
  margin: 0.35rem 0 0.35rem 1.1rem;
}
.oi-section li{
  margin: 0.2rem 0;
}
.oi-muted{ color: var(--oi-sub); font-size: 13px; }
.oi-pill{
  display:inline-block;
  border:1px solid var(--oi-border);
  background: rgba(106,53,255,0.10);
  color: var(--oi-text);
  padding: 4px 10px;
  border-radius:999px;
  font-size:12px;
  margin-right:6px;
}
pre code { white-space: pre-wrap !important; }
</style>
        """,
        unsafe_allow_html=True,
    )
