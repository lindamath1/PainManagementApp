#%%
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

def create_plot(pain_entries):
    df = pd.DataFrame.from_records([(pain.date_time, pain.pain_level, pain.is_active) for pain in pain_entries],
                               columns=['date_time', 'pain_level', 'is_active'])

    traces = []
    traces.append(go.Scatter(x=df['date_time'], 
                             y=df['pain_level'], 
                             name='pain', 
                             visible=True, 
                             marker_color='blue',
                             hovertemplate = '<br>'.join(["%{x}", 
                                                          "pain %{y}"]) + "<extra></extra>",)) 
    fig = go.Figure(data=traces)
    print(traces)

    # Update layout and add title
    fig.update_layout(
        title_text='Pain Entries Over Time',
        xaxis_title='date',
        yaxis_title='pain'
    )

    
    #fig.show()

    return fig.to_html(full_html=False)

if __name__ == "__main__":
    from crud import get_pain_entries, GetPainsEntriesIn
    from database import InitDBIn, get_session
    from utils.parameters import SQLALCHEMY_DATABASE_URL
    from models import Base

    init_params = InitDBIn(url=SQLALCHEMY_DATABASE_URL, base=Base)
    session = get_session(init_params)
    pain_entries = get_pain_entries(GetPainsEntriesIn(db=session))
    json = create_plot(pain_entries=pain_entries)
#%%
