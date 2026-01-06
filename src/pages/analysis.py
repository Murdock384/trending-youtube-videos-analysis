"""Analysis Page for YouTube Trending Videos Dashboard"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database import db_utils as db

def show():
    """Display the Analysis page with all 12 sections and local filters."""
    
    # Add custom CSS for styling
    st.markdown("""
        <style>
        /* Style selectbox to be shorter and have black background */
        div[data-baseweb="select"] {
            max-width: 300px;
        }
        
        div[data-baseweb="select"] > div {
            background-color: #000000;
            border: 1px solid #444444;
        }
        
        /* Dropdown menu styling */
        div[data-baseweb="popover"] {
            background-color: #000000;
        }
        
        ul[role="listbox"] {
            background-color: #000000;
        }
        
        li[role="option"] {
            background-color: #000000;
            color: #ffffff;
        }
        
        li[role="option"]:hover {
            background-color: #333333;
        }
        
        /* Round edges for all Plotly charts */
        .js-plotly-plot, .plotly {
            border-radius: 25px;
            overflow: hidden;
        }
        
        div[data-testid="stPlotlyChart"] {
            border-radius: 25px;
            overflow: hidden;
        }
        
        /* Insights content styling */
        .insight-content {
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        .insight-content p {
            font-size: 1.1rem;
        }
        
        .insight-content ul, .insight-content li {
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(""" # <svg xmlns="http://www.w3.org/2000/svg" width="45" height="45" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chart-no-axes-combined-icon lucide-chart-no-axes-combined" style="vertical-align: -5px;"><path d="M12 16v5"/><path d="M16 14v7"/><path d="M20 10v11"/><path d="m22 3-8.646 8.646a.5.5 0 0 1-.708 0L9.354 8.354a.5.5 0 0 0-.707 0L2 15"/><path d="M4 18v3"/><path d="M8 14v7"/></svg> Analysis and Findings""", unsafe_allow_html=True)
    
    # ============================================================================
    # SECTION 1: COUNTRY COMPARISON (WITH LOCAL COUNTRY FILTER)
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-earth" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><path d="M21.54 15H17a2 2 0 0 0-2 2v4.54"/><path d="M7 3.34V5a3 3 0 0 0 3 3a2 2 0 0 1 2 2c0 1.1.9 2 2 2a2 2 0 0 0 2-2c0-1.1.9-2 2-2h3.17"/><path d="M11 21.95V18a2 2 0 0 0-2-2a2 2 0 0 1-2-2v-1a2 2 0 0 0-2-2H2.05"/><circle cx="12" cy="12" r="10"/></svg> Cross-Country Performance </div>', unsafe_allow_html=True)
    
    # Local country filter for this section only
    country_options = ["All Countries", "United States", "Canada", "Great Britain"]
    selected_country = st.segmented_control(
        "Filter by Country:",
        country_options,
        default="All Countries",
        key="country_filter_section1"
    )
    
    # Map selection to filter value
    if selected_country == "All Countries":
        countries_filter = None
    elif selected_country == "United States":
        countries_filter = ["US"]
    elif selected_country == "Canada":
        countries_filter = ["CA"]
    elif selected_country == "Great Britain":
        countries_filter = ["GB"]
    
    country_stats = db.get_country_stats(countries_filter)

    if not country_stats.empty:

        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=(
                'Average Views by Country',
                'Average Engagement Rate by Country',
                'Average Days to Trending by Country'
            ),
            horizontal_spacing=0.1
        )
        
        # Plot 1: Average views
        fig.add_trace(
            go.Bar(
                x=country_stats['country'],
                y=country_stats['avg_views'],
                marker_color='coral',
                name='Avg Views',
                showlegend=False,
                text=country_stats['avg_views'].apply(lambda x: f'{int(x):,}'),
                textposition='outside'
            ),
            row=1, col=1
        )
        
        # Plot 2: Average engagement
        fig.add_trace(
            go.Bar(
                x=country_stats['country'],
                y=country_stats['avg_engagement'],
                marker_color='seagreen',
                name='Avg Engagement',
                showlegend=False,
                text=country_stats['avg_engagement'].apply(lambda x: f'{x:.2f}%'),
                textposition='outside'
            ),
            row=1, col=2
        )
        
        # Plot 3: Days to trending
        fig.add_trace(
            go.Bar(
                x=country_stats['country'],
                y=country_stats['avg_days_to_trending'],
                marker_color='mediumpurple',
                name='Days to Trending',
                showlegend=False,
                text=country_stats['avg_days_to_trending'].apply(lambda x: f'{x:.1f}'),
                textposition='outside'
            ),
            row=1, col=3
        )
        
        # Update layout
        fig.update_layout(
            height=500,
            title_text="Country Comparison Dashboard",
            title_font_size=20,
            title_x=0.5,
            showlegend=False
        )
        
        fig.update_yaxes(title_text="Average Views", row=1, col=1)
        fig.update_yaxes(title_text="Engagement Rate (%)", row=1, col=2)
        fig.update_yaxes(title_text="Days", row=1, col=3)
        
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            st.markdown("""
            <div class="insight-content">
            
            ### Cross-Country Patterns
            
            **Engagement Consistency:**
            - Average engagement rates are nearly identical across all three countries (~4%)
                        
            - The US Market seems to be the benchmark for engagement behavior and having a good middle ground 
              between the two other countries in terms of views and days to trending.
            
            **The Britain Paradox:**
            - GB achieves highest average views (5.8M) - 7x more than Canada
            - But takes 43.4 days to trend vs 3.0 days for Canada
            - Suggests more competitive market with higher barrier to trending
            - Once videos break through in GB, they achieve massive reach
            
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # SECTION 3: CATEGORY ANALYSIS (WITH LOCAL CATEGORY FILTER)
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-boxes" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><path d="M2.97 12.92A2 2 0 0 0 2 14.63v3.24a2 2 0 0 0 .97 1.71l3 1.8a2 2 0 0 0 2.06 0L12 19v-5.5l-5-3-4.03 2.42Z"/><path d="m7 16.5-4.74-2.85"/><path d="m7 16.5 5-3"/><path d="M7 16.5v5.17"/><path d="M12 13.5V19l3.97 2.38a2 2 0 0 0 2.06 0l3-1.8a2 2 0 0 0 .97-1.71v-3.24a2 2 0 0 0-.97-1.71L17 10.5l-5 3Z"/><path d="m17 16.5-5-3"/><path d="m17 16.5 4.74-2.85"/><path d="M17 16.5v5.17"/><path d="M7.97 4.42A2 2 0 0 0 7 6.13v4.37l5 3 5-3V6.13a2 2 0 0 0-.97-1.71l-3-1.8a2 2 0 0 0-2.06 0l-3 1.8Z"/><path d="M12 8 7.26 5.15"/><path d="m12 8 4.74-2.85"/><path d="M12 13.5V8"/></svg> Category Performance </div>', unsafe_allow_html=True)
    
    # Get category options from database
    categories_df = db.get_all_categories()
    category_options = ["All Categories"] + sorted(categories_df['category_name'].tolist())
    
    selected_category = st.selectbox(
        "Filter by Category:",
        category_options,
        key="category_filter_section3"
    )
    
    # Map selection to filter value
    if selected_category == "All Categories":
        categories_filter = None
    else:
        # Pass the category name to the filter
        categories_filter = [selected_category]
    
    category_stats = db.get_category_stats(None, categories_filter)

    if not category_stats.empty:
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            # Average views by category
            fig = px.bar(
                category_stats.sort_values('avg_views', ascending=True),
                y='category_name',
                x='avg_views',
                orientation='h',
                title='Average Views by Video Category',
                labels={'avg_views': 'Average Views', 'category_name': 'Category'},
                color='avg_views',
                color_continuous_scale='Viridis',
                text='avg_views'
            )
            
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(
                height=600,
                showlegend=False,
                xaxis_title="Average Views",
                yaxis_title="Category"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            top_category = category_stats.iloc[0]
            st.markdown(f"""
            <div class="insight-content">
            
            ### Category Performance Insights
            
            **Category Leader:**
            - **{top_category['category_name']}** dominates with {int(top_category['avg_views']):,} average views
            - Music benefits from shareability, repeat viewing, and playlist inclusion
            
            **Performance Spread:**
            - Wide variation in average views across categories
            - Top categories achieve 2-3x more views than bottom categories
            
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # ALL OTHER SECTIONS USE None FOR BOTH FILTERS
    # ============================================================================
    countries_filter = None
    categories_filter = None

    # ============================================================================
    # SECTION 4: CORRELATION ANALYSIS
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-link-icon lucide-link"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg> Correlation of Video Metrics</div>', unsafe_allow_html=True)

    corr_data = db.get_correlation_data(countries_filter)

    if not corr_data.empty:
        correlation_matrix = corr_data.corr()
        
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            fig = px.imshow(
                correlation_matrix,
                text_auto='.2f',
                aspect='auto',
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0,
                title='Correlation Matrix: Key Video Metrics',
                labels=dict(color="Correlation")
            )
            
            fig.update_layout(
                height=600,
                xaxis_title="",
                yaxis_title=""
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            views_corr = correlation_matrix['views'].sort_values(ascending=False)
            st.markdown(f"""
            <div class="insight-content">
            
            ### Metric Relationships
            
            **Strongest Correlations with Views:**
            - **Likes:** {views_corr['likes']:.2f} - Strongest Correlation to Views
            - **Comments:** {views_corr['comment_count']:.2f} - Comments also have a positive influence on Views
            - **Dislikes:** {views_corr['dislikes']:.2f} - Controversy drives views
            
            **Surprising Finding:**
            - **Engagement Rate:** {views_corr['engagement_rate']:.2f} - Negative correlation!
               where engagement rate was a new feature introduced during EDA as **(total likes + comments + dislikes) / views * 100**.
            - The ratio of likes to total reactions **(likes / (likes + dislikes))** has almost no real effect on views which we can see from 
              the value of correlation matrix: {correlation_matrix.loc['views', 'like_ratio']:.2f}.
            
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # SECTION 5: PUBLISHING STRATEGY
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-alarm-clock-check" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><circle cx="12" cy="13" r="8"/><path d="M5 3 2 6"/><path d="m22 6-3-3"/><path d="M6.38 18.7 4 21"/><path d="M17.64 18.67 20 21"/><path d="m9 13 2 2 4-4"/></svg> Optimal Publishing Time </div>', unsafe_allow_html=True)

    time_data = db.get_publishing_time_heatmap(countries_filter)

    if not time_data.empty:
        # Create pivot table for heatmap
        heatmap_pivot = time_data.pivot(
            index='publish_day_of_week',
            columns='publish_hour',
            values='avg_views'
        )
        
        # Map day numbers to names
        day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            fig = px.imshow(
                heatmap_pivot,
                labels=dict(x="Hour of Day (UTC)", y="Day of Week", color="Average Views"),
                y=day_labels,
                color_continuous_scale='YlOrRd',
                title='Best Times to Publish Videos (Average Views by Publish Time)',
                aspect='auto'
            )
            
            fig.update_layout(height=500)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            # Find best time
            best_idx = time_data['avg_views'].idxmax()
            best_day = int(time_data.loc[best_idx, 'publish_day_of_week'])
            best_hour = int(time_data.loc[best_idx, 'publish_hour'])
            best_views = int(time_data.loc[best_idx, 'avg_views'])
            
            st.markdown(f"""
            <div class="insight-content">
            
            ### Publishing Time Strategy
            
            **Optimal Publishing Time:**
            - **{day_labels[best_day]}** at **{best_hour}:00 AM UTC** with average views of **{best_views:,}**
            - Sunday **4:00 AM UTC** is a worthy alternative with very high average views indicating that videos published over 
              the weekend have higher potential to trend and reach larger audiences.
        
            
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # SECTION 6: VIEWS VS ENGAGEMENT
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-eye" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/></svg> Views vs Engagement: Performance Classification</div>', unsafe_allow_html=True)

    scatter_data = db.get_views_engagement_scatter(countries_filter, sample_size=4000)

    if not scatter_data.empty:
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            # Define colors for performance classes
            color_map = {
                'Explosive': '#FF0000',
                'High-Performing': '#FFA500',
                'Standard Trending': '#87CEEB'
            }
            
            fig = px.scatter(
                scatter_data,
                x='views',
                y='engagement_rate',
                color='performance_class',
                color_discrete_map=color_map,
                title='Relationship Between Views and Engagement',
                labels={
                    'views': 'Views (log scale)',
                    'engagement_rate': 'Engagement Rate (%)',
                    'performance_class': 'Performance Class'
                },
                opacity=0.6,
                hover_data={'views': ':,.0f', 'engagement_rate': ':.2f'}
            )
            
            fig.update_xaxes(type='log')
            fig.update_layout(height=600)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            st.markdown("""
            <div class="insight-content">
            
            ### Video View Performance Tiers Explained
            
            **Performance Classifications:**
            Here the objective was to categorize these trending videos into three distinct performance tiers based on their views and how quickly they rose to 
            popularity.
                        
            **Explosive Trending Videos** (Red)
            - Top 10% views AND in the Top 25% days to trending
            - True viral breakout hits
            - Massive reach achieved QUICKLY
            
            **High-Performing Trending Videos** (Orange)
            - Top 25% views OR top 50% speed
            - Excel in at least one dimension
            
            **Standard Trending Videos** (Blue)
            - Typical trending performance
            
            **The Paradox:**
            No strong correlation between views and engagement rate - many high-view videos have low engagement which is consistent with correlation matrix.
            
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # SECTION 7: ENGAGEMENT DISTRIBUTION
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-smile-plus" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><path d="M22 11v1a10 10 0 1 1-9-10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/><path d="M16 5h6"/><path d="M19 2v6"/></svg> Engagement Distribution by Category</div>', unsafe_allow_html=True)

    engagement_data = db.get_engagement_by_category(countries_filter, top_n=10)

    if not engagement_data.empty:
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            # Get top categories by count for ordering
            category_order = engagement_data.groupby('category_name').size().sort_values(ascending=False).index.tolist()
            
            fig = px.box(
                engagement_data,
                y='category_name',
                x='engagement_rate',
                category_orders={'category_name': category_order},
                title='Engagement Rate Distribution by Category (Top 10)',
                labels={
                    'engagement_rate': 'Engagement Rate (%)',
                    'category_name': 'Category'
                },
                color='category_name',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            fig.update_layout(
                height=600,
                showlegend=False,
                xaxis_title="Engagement Rate (%)",
                yaxis_title="Category"
            )
            
            # Limit x-axis to remove extreme outliers
            fig.update_xaxes(range=[0, engagement_data['engagement_rate'].quantile(0.95)])
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            st.markdown("""
            <div class="insight-content">
            
            ### Category Engagement Patterns
            
            **Consistency vs Variability:**
            - **Sports** shows narrow box = consistent engagement
            - **Comedy, Gaming** show wide spread = high variability
            - Creator skill matters more in variable categories
            
            **Median Performance:**
            - **Comedy & Gaming:** 4-5% engagement
            - **Music & Sports:** 2-3% engagement
            - High views ≠ high engagement
            
            **Outliers:**
            - **News & Politics** has extreme outliers (10%+) as controversial content spikes engagement,
              this is similar to **Science & Technology** category as there could be some new developments or breakthroughs that can drive sudden interest.
            
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # SECTION 8: TOP CHANNELS
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trophy" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><path d="M10 14.66v1.626a2 2 0 0 1-.976 1.696A5 5 0 0 0 7 21.978"/><path d="M14 14.66v1.626a2 2 0 0 0 .976 1.696A5 5 0 0 1 17 21.978"/><path d="M18 9h1.5a1 1 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M6 9a6 6 0 0 0 12 0V3a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1z"/><path d="M6 9H4.5a1 1 0 0 1 0-5H6"/></svg> Top Performing Channels</div>', unsafe_allow_html=True)

    channel_data = db.get_top_channels(countries_filter, top_n=20)

    if not channel_data.empty:
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            fig = px.bar(
                channel_data.sort_values('total_views'),
                y='channel_title',
                x='total_views',
                orientation='h',
                title='Top 20 Channels by Total Views',
                labels={'total_views': 'Total Views', 'channel_title': 'Channel'},
                color='total_views',
                color_continuous_scale='Plasma',
                text='total_views'
            )
            
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(
                height=700,
                showlegend=False,
                xaxis_title="Total Views",
                yaxis_title="Channel"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            top_channel = channel_data.iloc[0]
            st.markdown(f"""
            <div class="insight-content">
            
            ### Channel Dominance
            
            **Top Performer:**
            - **{top_channel['channel_title']}**
            - Total views: **{int(top_channel['total_views']):,}**
            
            **Dominance Pattern:**
            - Top channels appear repeatedly on trending
            - Established presence builds momentum
            - Brand recognition drives consistent performance
            
            **Scale Difference:**
            - Massive gap between #1 and #20
            - Winner-take-most dynamics
            - Platform favors established creators
            
            
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # SECTION 9: DAYS TO TRENDING
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-fast-forward" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><path d="M12 6a2 2 0 0 1 3.414-1.414l6 6a2 2 0 0 1 0 2.828l-6 6A2 2 0 0 1 12 18z"/><path d="M2 6a2 2 0 0 1 3.414-1.414l6 6a2 2 0 0 1 0 2.828l-6 6A2 2 0 0 1 2 18z"/></svg> How Long Does it Take to Go Viral?</div>', unsafe_allow_html=True)

    days_data = db.get_days_to_trending(countries_filter)

    if not days_data.empty:
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            median_days = days_data['days_to_trending'].median()
            mean_days = days_data['days_to_trending'].mean()
            
            fig = go.Figure()
            
            # Histogram
            fig.add_trace(go.Histogram(
                x=days_data['days_to_trending'],
                nbinsx=50,
                name='Frequency',
                marker_color='skyblue',
                marker_line_color='black',
                marker_line_width=1,
                opacity=0.7
            ))
            
            # Add median line
            fig.add_vline(
                x=median_days,
                line_dash="dash",
                line_color="red",
                line_width=2,
                annotation_text=f"Median: {median_days:.1f} days",
                annotation_position="top"
            )
            
            # Add mean line
            fig.add_vline(
                x=mean_days,
                line_dash="dash",
                line_color="orange",
                line_width=2,
                annotation_text=f"Mean: {mean_days:.1f} days",
                annotation_position="top"
            )
            
            fig.update_layout(
                title='Distribution of Days from Publish to Trending',
                xaxis_title='Days from Publish to Trending',
                yaxis_title='Frequency',
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            st.markdown(f"""
            <div class="insight-content">
            
            ### Viral Timing Insights
            
            **Trending Window:**
            - **Median:** {median_days:.1f} days
            - **Mean:** {mean_days:.1f} days
            - Most videos trend within first week
            
            **The Golden Window:**
            - **0-7 days:** Prime trending period
            - **First 48 hours:** Critical momentum period
            - **After 2 weeks:** Viral potential drops significantly
            
            
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # SECTION 10: TITLE LENGTH IMPACT
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-notebook-pen" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><path d="M13.4 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7.4"/><path d="M2 6h4"/><path d="M2 10h4"/><path d="M2 14h4"/><path d="M2 18h4"/><path d="M21.378 5.626a1 1 0 1 0-3.004-3.004l-5.01 5.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"/></svg> Does Title Length Affect Success?</div>', unsafe_allow_html=True)

    title_data = db.get_title_length_analysis(countries_filter)

    if not title_data.empty:
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            fig = px.bar(
                title_data,
                x='title_category',
                y='avg_views',
                title='Average Views by Title Length in Number of Characters',
                labels={
                    'title_category': 'Title Length Category',
                    'avg_views': 'Average Views'
                },
                color='avg_views',
                color_continuous_scale='Blues',
                text='avg_views'
            )
            
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(
                height=500,
                showlegend=False,
                xaxis_title="Title Length Category",
                yaxis_title="Average Views"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            best_category = title_data.loc[title_data['avg_views'].idxmax()]
            
            st.markdown(f"""
            <div class="insight-content">
            
            ### Title Length Strategy
            
            **Optimal Length:**
            - **{best_category['title_category']}** performs best
            - Average views: **{int(best_category['avg_views']):,}**
            
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-content">
            
            **Why Medium length titles is the best:**
            - It performs almost as well as short titles but allows you to add more to pique interest.
            - Balances curiosity and clarity
            
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # SECTION 11: TAG ANALYSIS
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-tags" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><path d="M13.172 2a2 2 0 0 1 1.414.586l6.71 6.71a2.4 2.4 0 0 1 0 3.408l-4.592 4.592a2.4 2.4 0 0 1-3.408 0l-6.71-6.71A2 2 0 0 1 6 9.172V3a1 1 0 0 1 1-1z"/><path d="M2 7v6.172a2 2 0 0 0 .586 1.414l6.71 6.71a2.4 2.4 0 0 0 3.191.193"/><circle cx="10.5" cy="6.5" r=".5" fill="currentColor"/></svg> Impact of Tag Count on Performance</div>', unsafe_allow_html=True)

    tag_data = db.get_tag_analysis(countries_filter)

    if not tag_data.empty:
        chart_col, insight_col = st.columns([2, 1])
        
        with chart_col:
            # Create dual-axis plot
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add views trace
            fig.add_trace(
                go.Scatter(
                    x=tag_data['tag_count'],
                    y=tag_data['avg_views'],
                    mode='lines+markers',
                    name='Avg Views',
                    line=dict(color='blue', width=2),
                    marker=dict(size=6)
                ),
                secondary_y=False
            )
            
            # Add engagement trace
            fig.add_trace(
                go.Scatter(
                    x=tag_data['tag_count'],
                    y=tag_data['avg_engagement'],
                    mode='lines+markers',
                    name='Avg Engagement',
                    line=dict(color='red', width=2),
                    marker=dict(size=6, symbol='square')
                ),
                secondary_y=True
            )
            
            fig.update_layout(
                title='Impact of Tag Count on Video Performance',
                xaxis_title='Number of Tags',
                height=500,
                hovermode='x unified'
            )
            
            fig.update_yaxes(title_text="Average Views", secondary_y=False, color='blue')
            fig.update_yaxes(title_text="Average Engagement Rate (%)", secondary_y=True, color='red')
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            optimal_views_idx = tag_data['avg_views'].idxmax()
            optimal_eng_idx = tag_data['avg_engagement'].idxmax()
            optimal_views_count = int(tag_data.loc[optimal_views_idx, 'tag_count'])
            optimal_eng_count = int(tag_data.loc[optimal_eng_idx, 'tag_count'])
            
            st.markdown(f"""
            <div class="insight-content">
            
            ### Tag Strategy Insights
            
            **Optimal Tag Count:**
            - **For Views:** {optimal_views_count} tags
            - **For Engagement:** {optimal_eng_count} tags
            
            **Overall Correlation:**
            - Weak negative correlation (-0.025)
            - More tags ≠ better performance
            - Diminishing returns after ~20-30 tags
        
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================================
    # SECTION 12: KEY FINDINGS
    # ============================================================================
    st.markdown('<div class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f0f0f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-brain" style="display: inline-block; vertical-align: middle; margin-right: 8px;"><path d="M12 18V5"/><path d="M15 13a4.17 4.17 0 0 1-3-4 4.17 4.17 0 0 1-3 4"/><path d="M17.598 6.5A3 3 0 1 0 12 5a3 3 0 1 0-5.598 1.5"/><path d="M17.997 5.125a4 4 0 0 1 2.526 5.77"/><path d="M18 18a4 4 0 0 0 2-7.464"/><path d="M19.967 17.483A4 4 0 1 1 12 18a4 4 0 1 1-7.967-.517"/><path d="M6 18a4 4 0 0 1-2-7.464"/><path d="M6.003 5.125a4 4 0 0 0-2.526 5.77"/></svg> Key Findings: What Makes a YouTube Video Successful?</div>', unsafe_allow_html=True)

    st.markdown("""
    Based on analysis of trending videos from the United States, Canada, and Great Britain, here are the data-driven insights:
    """)

    # Finding 1
    with st.expander("**1. Music Dominates Trending Content**", expanded=True):
        st.markdown("""
        **Finding:** Music videos achieve the highest average views across all categories.
        
        **What This Means:**
        - Music content has inherent viral potential due to shareability and repeat viewing
        - The category benefits from embedded plays, social sharing, and playlist inclusion
        """)

    # Finding 2
    with st.expander("**2. High Views Don't Guarantee High Engagement Rate**"):
        st.markdown("""
        **Finding:** Engagement rate shows a **negative correlation (-0.08)** with views.
        
        **What This Means:**
        - Videos with massive view counts often have **lower engagement rates**
        - Creator needs to additionally put effort to drive likes/comments/shares.
        """)

    # Finding 3
    with st.expander("**3. Likes Are the Strongest Predictor of High View Performance**"):
        st.markdown("""
        **Finding:** Likes show the **strongest positive correlation** with views among all engagement metrics.
        
        **What This Means:**
        - Videos that receive high like counts consistently achieve high view counts
        - Likes are a more reliable success indicator than comments or shares
        - The like button is the easiest engagement action, making it a key algorithmic signal
        
        **Strategy:** This explains why content creators encourage viewers to like videos through CTAs (calls-to-action) at strategic moments - content that prompts likes early can snowball into viral reach.
        """)

    # Finding 4
    with st.expander("**4. Early Morning Weekend Publishing Shows Highest Average Views**"):
        st.markdown("""
        **Finding:** Videos published at around **5:00 AM** (UTC timezone) on weekends show highest average views.
        
        **Strategy:** Schedule uploads for early morning UTC on weekends to maximize initial visibility.
        """)

    # Finding 5
    with st.expander("**5. Trending Window is Tight - 4 Days Median**"):
        st.markdown("""
        **Finding:** **Median time to trending is 4 days** after publication.
        
        **What This Means:**
        - Most successful videos gain traction within the first week
        - The "golden window" is 0-7 days post-publish
        - After 2 weeks without trending, viral potential drops significantly
        - Early momentum compounds through YouTube's recommendation algorithm
        
        **Critical Period:** First 48 hours determine if a video will trend.
        """)

    # Finding 6
    with st.expander("**6. Title Length and Tags Impact on Performance**"):
        st.markdown("""
        **Finding:** Short to medium titles (up to 60 characters) perform better, and tag count does not correspond to views.
        
        **What This Means:**
        - **Title Length:** Videos with titles under 60 characters achieve higher median and average views
          - Short (<30 chars) and Medium (30-60 chars) titles are more digestible and click-friendly
          - Long titles (60+ chars) may get truncated in search results and recommendations
          - Concise, punchy titles outperform verbose descriptions
          
        - **Tag Quality Over Quantity:** More tags ≠ better performance
          - 6-8 relevant, specific tags appears optimal (from visualization analysis)
          - Tag accuracy and relevance matter far more than exhaustive lists
        
        **Strategy:** Craft concise, compelling titles (aim for 30-60 characters) and focus on specific, accurate tags rather than exhaustive lists. Neither factor drives discovery alone.
        """)

    # Finding 7
    with st.expander("**7. Top Performing Channels keep having trending videos**"):
        st.markdown("""
        **Finding:** Once you get a few viral videos, you tend to keep getting more.
        
        **What This Means:**
        - Although it might be hard to get your first trending video, once you do, it gets easier to get more.
        - Youtube Rewards consistency and established presence.
        - Building a brand and audience over time compounds your success.
        """)


# Calling the show function to display the page
show()
