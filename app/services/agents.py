import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class ResearchAgents:
    def __init__(self, groq_api_key: str, tavily_api_key: str):
        if not groq_api_key or not tavily_api_key:
            raise ValueError("API keys not found in environment variables")
        self.groq_api_key = groq_api_key
        self.tavily_api_key = tavily_api_key
        self.llm = ChatGroq(
            api_key=self.groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=4000,
        )

    def research_agent(self, query: str, search_results: str) -> str:
        prompt = PromptTemplate(
            input_variables=["query", "search_results"],
            template="""You are an Expert Research Agent. Analyze this search data about: {query}

SEARCH RESULTS:
{search_results}

Extract:
1. Specific company names, funding amounts, recent developments
2. Key market players and leaders
3. Concrete statistics and growth data
4. Expert quotes and industry insights
5. Recent news and technological breakthroughs

Focus on factual, recent information. Prioritize Indian companies and current developments.""",
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"query": query, "search_results": search_results})

    def summarizer_agent(self, research_content: str) -> str:
        prompt = PromptTemplate(
            input_variables=["research_content"],
            template="""Process this research content:
{research_content}

Create structured summary:

## Company Profiles
- Company name, founding year, headquarters
- Core AI technology and healthcare focus
- Key products/services and recent funding

## Market Intelligence
- Market size, growth statistics
- Investment trends, key partnerships
- Technology applications and innovations

## Recent Developments
- Latest news, product launches
- Awards, recognitions, expansions

Include specific numbers, dates, and company names.""",
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"research_content": research_content})

    def critic_agent(self, summary_content: str) -> str:
        prompt = PromptTemplate(
            input_variables=["summary_content"],
            template="""Evaluate this content for accuracy:
{summary_content}

Analyze:
- Information consistency and conflicts
- Data completeness and currency
- Source credibility and reliability
- Missing critical information

Provide reliability score (1-10) and improvement recommendations.""",
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"summary_content": summary_content})

    def writer_agent(self, research_data: str, summary: str, critique: str) -> str:
        prompt = PromptTemplate(
            input_variables=["research_data", "summary", "critique"],
            template="""Create a comprehensive research report using:

RESEARCH: {research_data}
SUMMARY: {summary}
CRITIQUE: {critique}

Structure:

# Executive Summary
Brief overview of Indian AI healthcare startup ecosystem, key insights, and top performers.

# Top AI Healthcare Startups in India
For each company:
## [Company Name]
- **Founded:** Year, Location
- **Focus Area:** Healthcare AI application
- **Technology:** Core AI technologies
- **Funding:** Latest rounds, total raised, valuation
- **Products:** Main offerings
- **Recent News:** Latest developments

# Market Analysis
- **Market Size:** Current and projected figures
- **Growth Trends:** Investment patterns and statistics
- **Key Technologies:** Popular AI applications
- **Challenges:** Market obstacles and opportunities

# Investment Landscape
- **Funding Trends:** Recent investment patterns
- **Key Investors:** Major VCs and sources
- **Success Stories:** Notable achievements

# Future Outlook
- **Emerging Trends:** Next-gen technologies
- **Predictions:** Market forecasts
- **Opportunities:** Development areas

# References and Sources
List sources with clickable URLs and publication dates.

Use professional tone with specific data, figures, and company details.""",
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke(
            {"research_data": research_data, "summary": summary, "critique": critique}
        )
