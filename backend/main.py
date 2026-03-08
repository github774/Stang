from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import math

app = FastAPI()

# Enable CORS so the local frontend (port 3000) can communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    narrative: str
    audience: str

@app.post("/api/simulate")
async def simulate_spread(req: SimulationRequest):
    text_length = len(req.narrative)
    words = req.narrative.lower().split()
    
    # 1. Procedural generation seeds based on the text
    # A longer text or certain keywords makes the topic seem more "complex"
    complexity_score = min(2.0, max(0.5, text_length / 200.0))
    
    # Check for polarizing keywords
    polarizing_words = ['hate', 'fake', 'destroy', 'truth', 'lie', 'they', 'them', 'us', 'never', 'always', 'shocking', 'banned']
    polarization_factor = sum(1 for w in words if w in polarizing_words) * 0.15
    polarization_factor = min(1.0, polarization_factor)
    
    # Audience multipliers
    aud = req.audience
    if aud == "echo":
        base_shares = 3500
        polar_shift = 0.4
    elif aud == "skeptics":
        base_shares = 800
        polar_shift = -0.2
    elif aud == "youth":
        base_shares = 4500
        polar_shift = 0.1
    elif aud == "professionals":
        base_shares = 1200
        polar_shift = -0.1
    else:
        base_shares = 2000
        polar_shift = 0.0

    # 2. Generate Core Metrics
    m_shares = int(base_shares * complexity_score * (1.0 + random.random() * 0.5))
    m_impressions = int(m_shares * (5.0 + random.random() * 8.0))
    if polarization_factor > 0.5:
        m_likes = int(m_impressions * 0.15)
        m_dislikes = int(m_impressions * 0.20)
        m_comments = int(m_shares * 1.5)
    else:
        m_likes = int(m_impressions * 0.3)
        m_dislikes = int(m_impressions * 0.05)
        m_comments = int(m_shares * 0.5)

    # 3. Generate Reaction Bar Percentages (Must sum to 100)
    total_eng = m_likes + m_dislikes + m_shares + m_comments
    # Assume 30-50% 'none' (saw it, didn't react)
    none_pct = random.randint(30, 50)
    rem = 100 - none_pct
    
    if total_eng == 0:
        total_eng = 1 # prevent div/0
        
    liked_pct = int(rem * (m_likes / total_eng))
    disliked_pct = int(rem * (m_dislikes / total_eng))
    shared_pct = int(rem * (m_shares / total_eng))
    comment_pct = rem - (liked_pct + disliked_pct + shared_pct) # Assign remainder to comments
    
    if comment_pct < 0:
        comment_pct = 0
        liked_pct -= 1

    # 4. Generate Belief Shift Chart Data over 5 time periods (T=0, T=5, T=10, Correction, T=60)
    def gen_curve(start, end, volatility):
        curve = [start]
        curr = start
        for i in range(3):
            # random walk towards end
            curr += (end - curr) * 0.3 + (random.random() * volatility - volatility/2)
            curve.append(int(curr))
        curve.append(end)
        return curve

    # T=0 baselines
    n_start, s_start, p_start = 60, 25, 15
    
    # T=60 Endpoints depending on polarization calculation
    if polarization_factor > 0.4:
        n_end = random.randint(20, 35) # Neutrals drop
        s_end = random.randint(20, 35)
        p_end = 100 - (n_end + s_end)   # Polarized spikes
    else:
        n_end = random.randint(45, 65) # Neutrals stay stable
        p_end = random.randint(10, 20)
        s_end = 100 - (n_end + p_end)
        
    neutral_curve = gen_curve(n_start, n_end, 15)
    skeptic_curve = gen_curve(s_start, s_end, 10)
    polar_curve = gen_curve(p_start, p_end, 20)

    # 5. Determine the AI Analysis Text
    words_count = len(words)
    tone = "highly polarized" if polarization_factor > 0.5 else "balanced"
    
    if words_count < 10:
        analysis = f"The payload is extremely concise ({words_count} words). Because it lacks detail, it propagates quickly through rapid emotional sharing, causing a fast spike in {tone} reactions before burning out."
    elif words_count > 150:
        analysis = f"The payload is dense and detailed. It faces high initial friction from inattentive users, but achieves deep penetration within network clusters that align with its {tone} messaging. The correction phase shows strong resilience."
    else:
        analysis = f"The payload exhibits standard meme-kinetic behavior. Its {tone} framing causes moderate boundary friction between clusters, but it eventually stabilizes, resulting in a {abs(n_start - n_end)}% net shift in the neutral baseline."

    return {
        "metrics": {
            "impressions": m_impressions,
            "likes": m_likes,
            "dislikes": m_dislikes,
            "shares": m_shares,
            "comments": m_comments
        },
        "reactions": {
            "liked": liked_pct,
            "disliked": disliked_pct,
            "shared": shared_pct,
            "comment": comment_pct,
            "none": none_pct
        },
        "charts": {
            "neutral": neutral_curve,
            "skeptic": skeptic_curve,
            "polar": polar_curve
        },
        "analysis": analysis
    }
